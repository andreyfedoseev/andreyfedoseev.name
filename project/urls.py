from django.conf.urls.defaults import patterns, include, handler500, url, \
    handler404
from django.conf import settings
from django.contrib import admin
from blog.sitemap import BlogSitemap


admin.autodiscover()


sitemaps = {
    'blog': BlogSitemap,
}

common_patterns = patterns(
    '',
    url(r'^robots.txt$', include('robots.urls')),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    url(r'^i18n.js$', 'django.views.i18n.javascript_catalog', {'packages': ("project")}, name="i18n.js"),
    url(r'^admin/', include(admin.site.urls)),
)


urlpatterns = common_patterns + patterns("",
    url(r"^", include("project.local_urls")),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
