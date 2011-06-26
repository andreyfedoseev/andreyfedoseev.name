from django.conf.urls.defaults import patterns, url, include


urlpatterns = patterns(
    '',
    url(r'^$', 'project.views.frontpage', name='frontpage'),
    url(r'^login$', 'django.contrib.auth.views.login', name="auth_login"),
    url(r'^blog/', include('blog.urls', namespace="blog", app_name="blog")),
    url(r'^about/$', 'django.views.generic.simple.direct_to_template', {'template': 'blog/include/about.html'}, name="about"),
    url(r'^cv/$', 'django.views.generic.simple.direct_to_template', {'template': 'cv.html'}, name="cv"),
)

