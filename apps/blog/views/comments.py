from annoying.decorators import JsonResponse, ajax_request
from blog.forms import CommentForm, BlogAuthorCommentForm
from blog.models import Entry, Comment
from blog.views import BlogViewMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import View


AUTHOR_NAME_COOKIE = "comment_author_name"
AUTHOR_EMAIL_COOKIE = "comment_author_email"
AUTHOR_URL_COOKIE = "comment_author_url"
COOKIE_MAX_AGE = 60 * 60 * 24 * 30


class AddComment(BlogViewMixin, View):

    def post(self, request, *args, **kwargs):
        entry_id = kwargs["entry_id"]
        entry = get_object_or_404(Entry, id=entry_id, published=True)
        if self.is_author:
            form = BlogAuthorCommentForm(request.POST,
                                        instance=Comment(entry=entry,
                                                         by_blog_author=True))
        else:
            form = CommentForm(request.POST, instance=Comment(entry=entry))
        cookies = {}
        response = {}

        if form.is_valid():
            comment = form.save()
            context = self.get_context_data(**kwargs)
            context["comment"] = comment
            response = dict(status="success", message=form.success_message,
                            comment=render_to_string("blog/include/comment.html",
                                                     Context(context)))

            if not self.is_author:
                cookies[AUTHOR_NAME_COOKIE] = form.cleaned_data['author_name']
                cookies[AUTHOR_EMAIL_COOKIE] = form.cleaned_data['author_email']
                cookies[AUTHOR_URL_COOKIE] = form.cleaned_data['author_url']

        else:
            errors = {}
            for field_name, errors_list in form.errors.items():
                errors[field_name] = errors_list[0]
            response = dict(status="error", errors=errors,
                            message=form.error_message)

        response = JsonResponse(response)
        if cookies:
            for k, v in cookies.items():
                response.set_cookie(k, v.encode('utf-8'), COOKIE_MAX_AGE)

        return response


class DeleteComment(BlogViewMixin, View):

    @method_decorator(ajax_request)
    def post(self, request, *args, **kwargs):
        if not self.is_author:
            return HttpResponseForbidden()
        comment_id = kwargs["comment_id"]
        comment = get_object_or_404(Comment, id=int(comment_id))
        comment.delete()
        return dict(status="success")