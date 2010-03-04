from blog.models import Blog
from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect


def frontpage(request):
    site = Site.objects.get_current()
    blog = Blog.objects.get(site=site)
    return HttpResponsePermanentRedirect(blog.get_absolute_url())