from blog.forms import getFormData, EntryForm, saveEntry
from blog.models import Blog, Entry, Image
from django.contrib.auth.decorators import permission_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
import cjson
import oembed


@permission_required('add_entry')
def index(request):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    return render_to_response("blog/admin/index.html", {
                              'blog': blog,
                              }, RequestContext(request))
    
    
@permission_required('add_entry')
def preview(request):
    return render_to_response("blog/admin/preview.html", RequestContext(request))
    
    
@permission_required('add_entry')
def add_entry(request):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse("blog:admin-index"))
        form = EntryForm(request.POST)
        if form.is_valid():
            if 'save' in request.POST:
                data = form.cleaned_data
                entry = Entry()
                entry.blog = blog
                entry = saveEntry(entry, data)
                request.notifications.success(_(u"New entry was created."))
                return HttpResponseRedirect(reverse("blog:edit-entry", args=(entry.id,)))
        else:
            request.notifications.error(_(u"Please correct the indicated errors."))
    else:
        form = EntryForm()
    return render_to_response('blog/admin/forms/entry.html', {
                              'blog': blog,
                              'form': form,
                              }, RequestContext(request))         


@permission_required('edit_entry')
def edit_entry(request, id, slug=None):
    site = Site.objects.get_current()
    blog = get_object_or_404(Blog, site=site)
    if slug:
        entry = get_object_or_404(Entry, id=id, slug=slug)
    else:
        entry = get_object_or_404(Entry, id=id)
    if request.method == 'POST':
        if 'cancel' in request.POST:
            return HttpResponseRedirect(reverse("blog:admin-index"))
        form = EntryForm(request.POST)
        if form.is_valid():
            if 'save' in request.POST:
                data = form.cleaned_data
                entry = saveEntry(entry, data)
                request.notifications.success(_(u"Your changes were saved."))
        else:
            request.notifications.error(_(u"Please correct the indicated errors."))
            
    else:
        data = getFormData(entry)
        form = EntryForm(data)
    return render_to_response('blog/admin/forms/entry.html', {
                              'blog': blog,
                              'entry': entry,
                              'form': form,
                              'action': reverse("blog:edit-entry", args=(entry.id,)),
                              }, RequestContext(request))         


@permission_required('add_image')
def ajax_upload_image(request):
    files = request.FILES
    if request.method != "POST" or not files:
        raise Http404()
    data = {}
    data['status'] = 'failure'
    data['message'] = _(u'Image upload has failed.')
    try:
        file = files['userfile']
        image = Image()
        image.image = file
        image.save()
        data['id'] = image.id
        data['status'] = 'success'
        data['message'] = _(u'New image was uploaded.')
    except:
        import logging, traceback
        logging.debug(traceback.format_exc())
    return HttpResponse(cjson.encode(data))


@permission_required('add_image')
def ajax_get_images(request):
    ids = request.GET.getlist("ids[]")
    data = []
    try:
        for id in ids:
            try:
                id = int(id)
            except ValueError:
                continue
            try:
                image = Image.objects.get(pk=id)
            except:
                continue
            if image:
                data.append({
                    'id': id,
                    'filename': image.image.name.split('/')[-1],
                    'url': image.image.url,
                    'width': image.image.width,
                    'height': image.image.height,
                    'thumb_url': image.image.thumbnail.absolute_url,
                    'thumb_width': image.image.thumbnail.width(),
                    'thumb_height': image.image.thumbnail.height(),
                    'scaled_url': image.image.extra_thumbnails['scaled'].absolute_url,
                    'scaled_width': image.image.extra_thumbnails['scaled'].width(),
                    'scaled_height': image.image.extra_thumbnails['scaled'].height(),
                })
    except:
        import logging, traceback
        logging.debug(traceback.format_exc())
    return HttpResponse(cjson.encode(data))


@permission_required('delete_image')
def ajax_delete_image(request):
    id = int(request.GET.get("id"))
    try:
        Image.objects.get(pk=id).delete()
    except:
        pass
        
    return HttpResponse(cjson.encode(""))
