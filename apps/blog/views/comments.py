from annoying.decorators import JsonResponse
from blog.forms import CommentForm
from blog.models import Entry, Comment
from blog.views import BlogViewMixin
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import render_to_string
from django.views.generic import View


AUTHOR_NAME_COOKIE = "comment_author_name"
AUTHOR_EMAIL_COOKIE = "comment_author_email"
AUTHOR_URL_COOKIE = "comment_author_url"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30


class AddComment(BlogViewMixin, View):

    def post(self, request, *args, **kwargs):
        import time
        time.sleep(3)
        entry_id = kwargs["entry_id"]
        entry = get_object_or_404(Entry, id=entry_id, published=True)
        form = CommentForm(request.POST, instance=Comment(entry=entry))
        cookies = {}
        response = {}
        if form.is_valid():
            comment = form.save()
            response = dict(status="success", message=form.success_message,
                            comment=render_to_string("blog/include/comment.html",
                                                     Context(dict(comment=comment))))

            if request.user.is_anonymous():
                cookies[AUTHOR_NAME_COOKIE] = form.cleaned_data['author_name']
                cookies[AUTHOR_EMAIL_COOKIE] = form.cleaned_data['author_email']
                cookies[AUTHOR_URL_COOKIE] = form.cleaned_data['author_url']

        else:
            errors = {}
            for field_name, errors_list in form.errors.items():
                errors[field_name] = errors_list[0]
            response = dict(status="error", errors=errors,
                            message=form.error_message)

        print "!!!", response
        response = JsonResponse(response)
        if cookies:
            for k, v in cookies.items():
                response.set_cookie(k, v.encode('utf-8'), COOKIE_MAX_AGE)

        return response
