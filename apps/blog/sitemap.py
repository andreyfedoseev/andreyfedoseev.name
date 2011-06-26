from blog.models import Entry
from django.contrib.sitemaps import Sitemap


class BlogSitemap(Sitemap):
    
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        return Entry.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.publication_timestamp