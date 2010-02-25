from django.contrib.syndication.feeds import Feed
from django.utils import feedgenerator
from django.contrib.sites.models import Site
from blog.models import Blog


class Recent(Feed):
    
    feed_type = feedgenerator.Rss201rev2Feed
    
    title_template = "blog/feeds/title.html"
    description_template = "blog/feeds/description.html"
    
    def get_object(self, bits):
        site = Site.objects.get_current()
        return Blog.objects.get(site=site)
    
    def title(self, obj):
        return unicode(obj)
    
    def link(self, obj):
        return obj.get_absolute_url()
    
    def description(self, obj):
        return u''
    
    def items(self, obj):
        return obj.published_entries().filter(include_in_rss=True)

    def item_link(self, item):
        return item.get_absolute_url()
    
    def item_pubdate(self, item):
        return item.publication_timestamp