from django.conf import settings
from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin
from blog.sitemap import BlogSitemap


admin.autodiscover()


handler500 = "project.views.server_error"


sitemaps = {
    'blog': BlogSitemap,
}

common_patterns = patterns(
    "",
    url(r'^robots.txt$', include('robots.urls')),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^logout/?', "django.contrib.auth.views.logout", name="logout"),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns = common_patterns + patterns(
    "",
    url(r"^", include("project.local_urls")),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
