from annoying.decorators import ajax_request, JsonResponse
from annoying.functions import get_object_or_None
from blog.forms import EntryForm
from blog.models import Blog, Entry, Image, Comment
from blog.utils import render_text
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.base import TemplateView
from sorl.thumbnail import get_thumbnail
import json
import re


#noinspection PyUnresolvedReferences
class BlogAdminMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, language=request.LANGUAGE_CODE)
        user = request.user
        if user == self.blog.author or user.is_superuser:
            return super(BlogAdminMixin, self).dispatch(request, *args, **kwargs)
        return HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        data = super(BlogAdminMixin, self).get_context_data(**kwargs)
        data["blog"] = self.blog
        data["is_author"] = True
        return data


class Index(BlogAdminMixin, TemplateView):

    template_name = "blog/admin/index.html"

    def get_context_data(self, **kwargs):
        data = super(Index, self).get_context_data(**kwargs)
        data["published"] = self.blog.published_entries()
        data["drafts"] = self.blog.entry_set.filter(published=False)
        return data


class EntryPreview(BlogAdminMixin, TemplateView):

    template_name = "blog/admin/preview.html"

    def get_context_data(self, **kwargs):
        data = super(EntryPreview, self).get_context_data(**kwargs)
        text = self.request.POST.get("text", u"")
        text = text.replace(Entry.MORE_MARKER, u"")
        markdown = "markdown" in self.request.POST
        data["text"] = mark_safe(render_text(text, markdown))
        return data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class EditEntry(BlogAdminMixin, TemplateView):

    template_name = "blog/admin/entry.html"

    def get_context_data(self, **kwargs):
        data = super(EditEntry, self).get_context_data(**kwargs)
        if "entry_id" in kwargs:
            data["entry"] = get_object_or_404(Entry, id=int(kwargs["entry_id"]))
        return data

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        entry = context.get("entry")
        context["form"] = EntryForm(instance=entry)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return redirect("blog:admin_index")
        context = self.get_context_data(**kwargs)
        entry = context.get("entry")
        new_entry = False
        if not entry:
            new_entry = True
            entry = Entry(blog=self.blog)
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            entry = form.save()
            if request.is_ajax():
                return JsonResponse(dict(status="success",
                                         message=unicode(form.success_message)))
            else:
                messages.success(self.request, form.success_message)
                if new_entry:
                    return redirect("blog:admin_edit_entry", entry_id=entry.id)
                context["form"] = EntryForm(instance=entry)
                return self.render_to_response(context)

        else:
            if request.is_ajax():
                errors = {}
                for field_name, errors_list in form.errors.items():
                    errors[field_name] = errors_list[0]
                return JsonResponse(dict(status="error", errors=errors,
                                         message=unicode(form.error_message)))
            else:
                messages.error(self.request, form.error_message)
                context["form"] = EntryForm(request.POST)
                return self.render_to_response(context)



IMAGE_NAME_RE  = re.compile("^(?P<name>.+?)(?:\.(?P<extension>png|gif|jpg|jpeg))?$", re.I)


class UploadImage(BlogAdminMixin, View):

    @method_decorator(ajax_request)
    def post(self, request, *args, **kwargs):
        files = request.FILES
        files = files.getlist('files[]')
        if not files:
            return HttpResponse(json.dumps(dict(status="error")))

        images = []
        for file in files:
            if not file.content_type.startswith("image/"):
                continue
            image = Image.objects.create(image=file)

            name = IMAGE_NAME_RE.search(file.name).groupdict()["name"]

            images.append({
                'id': image.id,
                'name': name,
                'src': get_thumbnail(image.image, Image.THUMBNAIL_GEOMETRY).url,
            })
        response = dict(status="success", message=_(u'Images were uploaded.'),
                        images=images)
        return response


class ListEntryImages(BlogAdminMixin, View):

    @method_decorator(ajax_request)
    def get(self, request, *args, **kwargs):
        entry_id = kwargs.get("entry_id")
        if not entry_id:
            raise Http404()
        entry = get_object_or_404(Entry, id=int(entry_id))
        images = []
        for image in entry.image_set.all():
            images.append({
                'id': image.id,
                'name': IMAGE_NAME_RE.search(image.image.name.split('/')[-1]).groupdict()["name"],
                'src': get_thumbnail(image.image, Image.THUMBNAIL_GEOMETRY).url,
            })
        return dict(images=images)


class DeleteImage(BlogAdminMixin, View):

    @method_decorator(ajax_request)
    def post(self, request, *args, **kwargs):
        id = int(request.POST.get("id"))
        Image.objects.get(pk=id).delete()
        return dict(status="success")


class SpamComments(BlogAdminMixin, TemplateView):

    template_name = "blog/admin/comments-spam.html"

    def post(self, request, *args, **kwargs):

        if request.is_ajax() and "not_spam" in request.POST:
            comment_id = request.POST.get("comment_id")
            if not comment_id:
                return JsonResponse(dict(status="error",
                                         message="Missing comment ID."))
            try:
                comment_id = int(comment_id)
            except (TypeError, ValueError):
                return JsonResponse(dict(status="error",
                                         message="Invalid comment ID."))
            comment = get_object_or_None(Comment, id=comment_id)
            if comment and comment.is_spam:
                comment.is_spam = False
                comment.save()
            return JsonResponse(dict(
                status="success",
                spam_count=self.blog.spam_comments().count()
            ))

        elif "clear" in request.POST:
            Comment.objects.filter(is_spam=True).delete()
            messages.success(request, u"All spam comments are removed.")
            return redirect("blog:admin_index")
        else:
            return HttpResponseBadRequest()
