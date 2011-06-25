from blog.forms import CommentForm, BlogAuthorCommentForm
from blog.models import Entry as EntryModel
from blog.views import BlogViewMixin
from blog.views.comments import AUTHOR_NAME_COOKIE, AUTHOR_EMAIL_COOKIE, AUTHOR_URL_COOKIE
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import TemplateView


class Entry(BlogViewMixin, TemplateView):

    template_name = "blog/entry.html"

    def get(self, request, *args, **kwargs):
        id = int(kwargs["id"])
        slug = kwargs.get("slug")
        filters = dict(id=id, blog=self.blog)
        if slug:
            filters["slug"] = slug
        entry = get_object_or_404(EntryModel, **filters)
        if entry.slug and slug != entry.slug:
            return redirect(entry, permanent=True)
        return super(Entry, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(Entry, self).get_context_data(**kwargs)
        id = int(kwargs["id"])
        slug = kwargs.get("slug")
        filters = dict(id=id, blog=self.blog)
        if slug:
            filters["slug"] = slug
        entry = get_object_or_404(EntryModel, **filters)
        page_title = entry.title

        if self.is_author:
            comment_form = BlogAuthorCommentForm()
        else:
            initial = {}
            if self.request.user.is_anonymous():
                initial['author_name'] = self.request.COOKIES.get(AUTHOR_NAME_COOKIE, "").decode('utf-8')
                initial['author_email'] = self.request.COOKIES.get(AUTHOR_EMAIL_COOKIE, "").decode('utf-8')
                initial['author_url'] = self.request.COOKIES.get(AUTHOR_URL_COOKIE, "").decode('utf-8')
            comment_form = CommentForm(initial=initial)

        data.update(dict(entry=entry, page_title=page_title,
                         comment_form=comment_form))
        return data
