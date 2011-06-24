from blog.models import Blog
from django.contrib.sitemaps import Sitemap


# TODO: fix this. It should export all blogs
class BlogSitemap(Sitemap):
    
    changefreq = "weekly"
    priority = 0.5
    
    def items(self):
        blog = Blog.objects.all()[0]
        return blog.published_entries()

    def lastmod(self, obj):
        return obj.publication_timestamp