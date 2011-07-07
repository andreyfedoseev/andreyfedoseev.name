from annoying.decorators import JsonResponse
from blog.models import Blog
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import login
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView, View


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