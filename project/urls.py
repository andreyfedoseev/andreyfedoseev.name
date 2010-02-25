from django.conf.urls.defaults import patterns, include, handler500, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns(
    '',
    url(r'^$', 'project.views.frontpage', name='frontpage'),
    url(r'^blog/', include('blog.urls', namespace="blog", app_name='blog')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.auth_urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'', include('staticfiles.urls')),                            
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
