from django.conf.urls.defaults import patterns, include, handler500, url,\
    handler404
from django.conf import settings
from django.contrib import admin
from blog.sitemap import BlogSitemap
admin.autodiscover()


sitemaps = {
    'blog': BlogSitemap,            
}

urlpatterns = patterns(
    '',
    url(r'^$', 'project.views.frontpage', name='frontpage'),
    url(r'^blog/', include('blog.urls', namespace="blog", app_name='blog')),
    url(r'^about/', 'django.views.generic.simple.direct_to_template', {'template': 'blog/about.html'}, name="about"),
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
