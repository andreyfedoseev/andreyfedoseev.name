from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site
from blog.models import Blog, Entry, ENTRY_TYPES
from django.template.context import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
import datetime
from tagging.models import Tag, TaggedItem


POSTS_PER_PAGE = 9


def paginate(entries, view_name, args=(), kwargs={}, page=None):
    paginator = Paginator(entries, POSTS_PER_PAGE)
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1

    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    if page.has_next():
        kw = kwargs.copy()
        kw['page'] = page.next_page_number()
        next_page = reverse(view_name, args=args, kwargs=kw)
    else:
        next_page = None
    if page.has_previous():
        if page.previous_page_number() == 1:  
            prev_page = reverse(view_name, args=args, kwargs=kwargs)
        else:
            kw = kwargs.copy()
            kw['page'] = page.previous_page_number()
            prev_page = reverse(view_name, args=args, kwargs=kw)
    else:
        prev_page = None 

    return {'entries': page.object_list,
            'page': page,
            'next_page': next_page,
            'prev_page': prev_page,
            }


DISPLAY_TYPE_COOKE = 'blog_display_type'
COOKIE_MAX_AGE = 60 * 60 * 24 * 30
GRID_DISPLAY = 'grid'
LIST_DISPLAY = 'list'


def display_type(request):
    display_type = request.COOKIES.get(DISPLAY_TYPE_COOKE)
    if display_type not in (GRID_DISPLAY, LIST_DISPLAY):
        display_type = GRID_DISPLAY
    return display_type


def switch_display_type(request):
    if request.method != 'GET':
        raise Http404()
    type = display_type(request)
    if type == GRID_DISPLAY:
        type = LIST_DISPLAY
    else:
        type = GRID_DISPLAY
    next = request.GET.get('next', reverse('blog:index'))
    response = HttpResponseRedirect(next)
    response.set_cookie(DISPLAY_TYPE_COOKE, type, COOKIE_MAX_AGE)
    return response
    

def index(request, page=None):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    entries = blog.published_entries()

    data = {
        'blog': blog,
        'fixed_sidebar': True,
        'display_type': display_type(request)
    }
    data.update(paginate(entries, "blog:index", page=page))
    return render_to_response("blog/index.html", data,
                              context_instance=RequestContext(request))
    

