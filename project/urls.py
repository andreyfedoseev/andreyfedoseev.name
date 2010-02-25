from django.conf.urls.defaults import patterns, include, handler500, url
from django.conf import settings
from django.contrib import admin
from blog.sitemap import BlogSitemap
admin.autodiscover()

handler500 # Pyflakes

sitemaps = {
    'blog': BlogSitemap,            
}

urlpatterns = patterns(
    '',
    url(r'^$', 'project.views.frontpage', name='frontpage'),
    url(r'^blog/', include('blog.urls', namespace="blog", app_name='blog')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.auth_urls')),
    url(r'^robots.txt$', include('robots.urls')),
    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),                            
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
