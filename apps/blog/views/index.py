from blog.views import BlogViewMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from djpjax import PJAXResponseMixin
from haystack.models import SearchResult
from haystack.query import SearchQuerySet
from tagging.models import Tag, TaggedItem


class Index(BlogViewMixin, PJAXResponseMixin, TemplateView):

    template_name = "blog/index.html"
    pjax_template_name = "blog/include/entries-list.html"
    search = False
    POSTS_PER_PAGE = 5

    def get_context_data(self, **kwargs):
        data = super(Index, self).get_context_data(**kwargs)

        search = getattr(self, "search", False)
        search_term = self.request.REQUEST.get("q", u"").strip()
        tag = kwargs.get("tag")

        if search:
            if not search_term:
                raise Http404()
            entries = SearchQuerySet().narrow("published:true").narrow("blog:%i" % self.blog.id)
            entries = entries.filter(content=search_term).load_all()
        else:
            entries = self.blog.published_entries()
            if tag:
                tag = get_object_or_404(Tag, name=tag)
                entries = TaggedItem.objects.get_by_model(entries, tag)

            if not entries.exists():
                raise Http404()

        paginator = Paginator(entries, self.POSTS_PER_PAGE)
        page_number = kwargs.get("page", 1) or 1
        page_number = int(page_number)
        next_page = ""
        prev_page = ""
        try:
            current_page = paginator.page(page_number)
        except (EmptyPage, InvalidPage):
            raise Http404()


        if search:
            view_name = "blog:search"
        else:
            view_name = "blog:index"

        if current_page.has_next():
            if tag:
                next_page = reverse(view_name, kwargs=dict(page=page_number+1,
                                                              tag=tag.name))
            else:
                next_page = reverse(view_name, kwargs=dict(page=page_number+1))
        if page_number == 2:
            if tag:
                prev_page = reverse(view_name, kwargs=dict(tag=tag.name))
            else:
                prev_page = reverse(view_name)
        elif current_page.has_previous():
            if tag:
                prev_page = reverse(view_name, kwargs=dict(page=page_number-1,
                                                              tag=tag.name))
            else:
                prev_page = reverse(view_name, kwargs=dict(page=page_number-1))

        if next_page and search:
            next_page = u"%s?q=%s" % (next_page, search_term)
        if prev_page and search:
            prev_page = u"%s?q=%s" % (prev_page, search_term)

        is_frontpage = page_number == 1 and not tag and not search

        page_title_parts = []
        if search:
            page_title_parts.append(_("Search: %(search_term)s") % dict(search_term=search_term))
        elif tag:
            page_title_parts.append(_("Tag: %(tag)s") % dict(tag=tag.name))
        if page_number != 1:
            page_title_parts.append(_("Page %(number)i") % dict(number=page_number))

        page_title = u" | ".join(page_title_parts)

        if tag:
            addthis_title = None
            addthis_url = reverse("blog:index", kwargs=dict(tag=tag.name))
        else:
            addthis_title = self.blog.title
            addthis_url = self.blog.get_absolute_url()


        entries = map(lambda o: isinstance(o, SearchResult) and o.object or o,
                      current_page.object_list)

        data.update(
            dict(page_title=page_title,
                 entries=entries,
                 prev_page=prev_page,
                 next_page=next_page,
                 is_frontpage=is_frontpage,
                 tag=tag,
                 search=search,
                 search_term=search_term,
                 addthis_title=addthis_title,
                 addthis_url=self.request.build_absolute_uri(addthis_url),
            )
        )

        return data
