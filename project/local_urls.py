from django.conf.urls.defaults import patterns, url, include
from project.views import Login, LoginBox, About


urlpatterns = patterns(
    '',
    url(r'^$', 'project.views.frontpage', name='frontpage'),
    url(r'^login/?$', Login.as_view(), name="auth_login"),
    url(r'^login/box/?$', LoginBox.as_view(), name="login_box"),
    url(r'^blog/', include('blog.urls', namespace="blog", app_name="blog")),
    url(r'^about/?$', About.as_view(), name="about"),
    url(r'^cv/$', 'django.views.generic.simple.direct_to_template', {'template': 'cv.html'}, name="cv"),
    url(r'^i18n.js$', 'django.views.i18n.javascript_catalog', {'packages': ("project")}, name="i18n.js"),
)

