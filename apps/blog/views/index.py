from annoying.decorators import JsonResponse
from blog.views import BlogViewMixin
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView
from tagging.models import Tag, TaggedItem


class Index(BlogViewMixin, TemplateView):

    template_name = "blog/index.html"
    POSTS_PER_PAGE = 5

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = self.get_context_data(**kwargs)
            entries = render_to_string("blog/include/entries-list.html",
                                       dict(entries=data["entries"]))
            return JsonResponse(dict(
                entries=entries,
                page_title=data["page_title"],
                next_page=data["next_page"],
                prev_page=data["prev_page"]
            ))
        
        return super(Index, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(Index, self).get_context_data(**kwargs)

        entries = self.blog.published_entries()
        tag = kwargs.get("tag")
        if tag:
            tag = get_object_or_404(Tag, name=tag)
            entries = TaggedItem.objects.get_by_model(entries, tag)
        if not entries.exists():
            raise Http404()
        paginator = Paginator(entries, self.POSTS_PER_PAGE)
        page_number = kwargs.get("page", 1) or 1
        page_number = int(page_number)
        current_page = None
        next_page = ""
        prev_page = ""
        try:
            current_page = paginator.page(page_number)
        except (EmptyPage, InvalidPage):
            raise Http404()

        if current_page.has_next():
            if tag:
                next_page = reverse("blog:index", kwargs=dict(page=page_number+1,
                                                              tag=tag.name))
            else:
                next_page = reverse("blog:index", kwargs=dict(page=page_number+1))
        if page_number == 2:
            if tag:
                prev_page = reverse("blog:index", kwargs=dict(tag=tag.name))
            else:
                prev_page = reverse("blog:index")
        elif current_page.has_previous():
            if tag:
                prev_page = reverse("blog:index", kwargs=dict(page=page_number-1,
                                                              tag=tag.name))
            else:
                prev_page = reverse("blog:index", kwargs=dict(page=page_number-1))

        if next_page:
            next_page = self.request.build_absolute_uri(next_page)
        if prev_page:
            prev_page = self.request.build_absolute_uri(prev_page)


        is_frontpage = page_number == 1 and not tag

        page_title_parts = []
        if tag:
            page_title_parts.append(_("Tag: %(tag)s") % dict(tag=tag.name))
        if page_number != 1:
            page_title_parts.append(_("Page %(number)i") % dict(number=page_number))

        page_title = u" | ".join(page_title_parts)

        data.update(
            dict(page_title=page_title,
                 entries=current_page.object_list,
                 prev_page=prev_page,
                 next_page=next_page,
                 is_frontpage=is_frontpage,
                 tag=tag)
        )

        return data
