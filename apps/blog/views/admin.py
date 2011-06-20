from annoying.decorators import ajax_request
from blog.forms import EntryForm
from blog.models import Blog, Entry, Image
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView, UpdateView
import json


class Index(TemplateView):

    template_name = "blog/admin/index.html"

    def get_context_data(self, **kwargs):
        site = Site.objects.get_current()
        blog = get_object_or_404(Blog, site=site)
        return locals()


class EntryPreview(TemplateView):

    template_name = "blog/admin/preview.html"

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class AddEntry(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):

    form_class = EntryForm

    template_name = "blog/admin/forms/entry.html"

    def dispatch(self, request, *args, **kwargs):
        site = Site.objects.get_current()
        self.blog = get_object_or_404(Blog, site=site)
        return super(AddEntry, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs["blog"] = self.blog
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = None
        return super(AddEntry, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse("blog:admin_index"))
        self.object = Entry(blog=self.blog)
        return super(AddEntry, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        result = super(AddEntry, self).form_invalid(form)
        messages.error(self.request, _(u"Please correct the indicated errors."))
        return result

    def form_valid(self, form):
        result = super(AddEntry, self).form_valid(form)
        messages.success(self.request, _(u"New entry was created."))
        return result

    def get_success_url(self):
        return reverse("blog:admin_edit_entry", args=(self.object.id,))


class EditEntry(UpdateView):

    model = Entry
    form_class = EntryForm
    context_object_name = "entry"
    template_name = "blog/admin/forms/entry.html"

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(reverse("blog:admin_index"))
        return super(EditEntry, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        result = super(EditEntry, self).form_invalid(form)
        messages.error(self.request, _(u"Please correct the indicated errors."))
        return result

    def form_valid(self, form):
        result = super(EditEntry, self).form_valid(form)
        messages.success(self.request, _(u"Your changes were saved."))
        return result

    def get_success_url(self):
        return reverse("blog:admin_edit_entry", args=(self.object.id,))


@permission_required('add_image')
def ajax_upload_image(request):
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


@permission_required('add_image')
@ajax_request
def ajax_list_entry_images(request, entry_id=None):
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


@permission_required('delete_image')
@ajax_request
def ajax_delete_image(request):
    id = int(request.POST.get("id"))
    Image.objects.get(pk=id).delete()
    return dict(status="success")
