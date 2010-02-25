from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site
from blog.models import Blog, Entry
from django.template.context import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage


POSTS_PER_PAGE = 9


def index(request, page=1):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    paginator = Paginator(blog.published_entries().select_related(), POSTS_PER_PAGE)
    try:
        page = int(page)
    except ValueError:
        page = 1

    try:
        page = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)
            
    return render_to_response("blog/index.html", {
                              'blog': blog,
                              'page': page,
                              'entries': page.object_list,
                              }, context_instance=RequestContext(request))
    
    
def entry(request, id, slug=None):
    entry = get_object_or_404(Entry, id=id, slug=slug)
    return render_to_response("blog/entry.html", {
                              'entry': entry,
                              }, context_instance=RequestContext(request))
    