from annoying.decorators import ajax_request, JsonResponse
from blog.forms import EntryForm
from blog.models import Blog, Entry, Image
from blog.utils import render_text
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from django.views.generic import View
from django.views.generic.base import TemplateView
import json


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
        return data


class Index(BlogAdminMixin, TemplateView):

    template_name = "blog/admin/index.html"


class EntryPreview(BlogAdminMixin, TemplateView):

    template_name = "blog/admin/preview.html"

    def get_context_data(self, **kwargs):
        data = super(EntryPreview, self).get_context_data(**kwargs)
        text = self.request.POST.get("data", u"")
        text = text.replace(Entry.MORE_MARKER, u"")
        data["text"] = mark_safe(render_text(text))
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
                                         message=form.success_message))
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
                                         message=form.error_message))
            else:
                messages.error(self.request, form.error_message)
                context["form"] = EntryForm(request.POST)
                return self.render_to_response(context)


class UploadImage(BlogAdminMixin, View):

    def post(self, request, *args, **kwargs):
        files = request.FILES
        file = files.get('file')
        if not file:
            return HttpResponse(json.dumps(dict(status="error")))
        image = Image.objects.create(image=file)
        image_data = {
            'id': image.id,
            'filename': image.image.name.split('/')[-1],
            'src': image.image.thumbnail.absolute_url,
        }
        response = dict(status="success", message=_(u'New image was uploaded.'),
                        image=image_data)
        return HttpResponse(json.dumps(response))


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
                'filename': image.image.name.split('/')[-1],
                'src': image.image.thumbnail.absolute_url,
            })
        return dict(images=images)


class DeleteImage(BlogAdminMixin, View):

    @method_decorator(ajax_request)
    def post(self, request, *args, **kwargs):
        id = int(request.POST.get("id"))
        Image.objects.get(pk=id).delete()
        return dict(status="success")
