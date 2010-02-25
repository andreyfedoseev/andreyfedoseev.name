from django.contrib.sitemaps import Sitemap
from django.contrib.sites.models import Site
from blog.models import Blog


class BlogSitemap(Sitemap):
    
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        site = Site.objects.get_current()
        blog = Blog.objects.get(site=site)
        return blog.published_entries()

    def lastmod(self, obj):
        return obj.publication_timestamp