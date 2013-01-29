from annoying.decorators import JsonResponse
from annoying.functions import get_object_or_None
from django.http import HttpResponseServerError
from django.template import loader, RequestContext
from blog.models import Blog
from blog.views import BlogViewMixin
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView, View
from flatblocks.models import FlatBlock


def server_error(request):
    t = loader.get_template("500.html")
    return HttpResponseServerError(t.render(RequestContext(request)))


def frontpage(request):
    blog = get_object_or_404(Blog, language=request.LANGUAGE_CODE)
    return redirect(blog, permanent=True)


class LoginBox(TemplateView):

    template_name = "include/login-box.html"

    def get_context_data(self, **kwargs):
        form = AuthenticationForm()
        return dict(form=form)


class Login(View):

    def post(self, request, *args, **kwargs):

        if request.is_ajax():
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                auth_login(request, form.get_user())
                return JsonResponse(dict(status="success"))
            else:
                return JsonResponse(dict(status="error"))
        return login(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return login(request, *args, **kwargs)


class About(BlogViewMixin, TemplateView):

    template_name = "about.html"

    def get_context_data(self, **kwargs):
        data = super(About, self).get_context_data(**kwargs)
        flatblock = get_object_or_None(FlatBlock,
                                       slug="about-%s" % self.request.LANGUAGE_CODE)
        data["content"] = flatblock and flatblock.content or u""
        data["page_title"] = _("About me")
        data["is_about_page"] = True
        return data
