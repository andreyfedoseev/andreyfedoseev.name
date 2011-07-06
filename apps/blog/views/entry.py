from blog.forms import CommentForm, BlogAuthorCommentForm
from blog.models import Entry as EntryModel
from blog.views import BlogViewMixin
from blog.views.comments import AUTHOR_NAME_COOKIE, AUTHOR_EMAIL_COOKIE, AUTHOR_URL_COOKIE, NOTIFY_COOKIE
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
        if not self.is_author:
            filters["published"] = True
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
        if not self.is_author:
            filters["published"] = True
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
                initial['notify'] = bool(self.request.COOKIES.get(NOTIFY_COOKIE, "").decode('utf-8'))
            comment_form = CommentForm(initial=initial)

        entries = self.blog.published_entries().exclude(id=entry.id)
        prev_entries = entries.filter(publication_timestamp__lte=entry.publication_timestamp).order_by("-publication_timestamp")
        if prev_entries.exists():
            prev_entry = prev_entries[0]
        else:
            prev_entry = None

        next_entries = entries.filter(publication_timestamp__gte=entry.publication_timestamp).order_by("publication_timestamp")
        if next_entries.exists():
            next_entry = next_entries[0]
        else:
            next_entry = None

        data.update(dict(entry=entry, page_title=page_title,
                         comment_form=comment_form,
                         prev_entry=prev_entry, next_entry=next_entry,
                         ))
        return data
