from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from blog.models import Blog
from tagging.models import Tag, TaggedItem
from django.utils.translation import ugettext as _


class RecentFeed(Feed):
    
    def get_object(self, request, *args, **kwargs):
        return get_object_or_404(Blog, language=request.LANGUAGE_CODE)
    
    def title(self, obj):
        return obj.title
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return obj.description

    def author_name(self, obj):
        return obj.author_name

    def items(self, obj):
        return obj.published_entries().filter(include_in_rss=True)[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.short_text

    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.publication_timestamp

    def item_categories(self, item):
        return item.tags.values_list("name", flat=True)


class TagFeed(RecentFeed):

    def get_object(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, language=request.LANGUAGE_CODE)
        return  get_object_or_404(Tag, name=kwargs["tag"])

    def title(self, obj):
        return u" - ".join([self.blog.title, _("Tag: %(tag)s") % dict(tag=obj.name)])

    def description(self, obj):
        return self.blog.description

    def author_name(self, obj):
        return self.blog.author_name

    def link(self, obj):
        return reverse("blog:index", kwargs=dict(tag=obj.name))

    def items(self, obj):
        return TaggedItem.objects.get_by_model(self.blog.published_entries().filter(
                                                    include_in_rss=True),
                                               obj)[:10]