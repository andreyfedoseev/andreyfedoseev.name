from blog.views import BlogViewMixin
from django.http import Http404
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from tagging.models import Tag


class Tags(BlogViewMixin, TemplateView):

    template_name = "blog/tags.html"

    def get_context_data(self, **kwargs):
        data = super(Tags, self).get_context_data(**kwargs)
        tags = Tag.objects.usage_for_queryset(self.blog.published_entries(),
                                              counts=True)
        tags.sort(key=lambda x: x.count, reverse=True)
        if not tags:
            raise Http404()
        mean_count = float(sum([tag.count for tag in tags])) / float(len(tags))

        main_tags = []
        other_tags = []
        for tag in tags:
            if tag.count >= mean_count:
                main_tags.append(tag)
            else:
                other_tags.append(tag)
        data["main_tags"] = main_tags
        data["other_tags"] = other_tags
        data["page_title"] = _(u"Tags")

        return data
