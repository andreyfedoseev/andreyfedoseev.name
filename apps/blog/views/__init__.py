from blog.models import Blog
from django.contrib.sites.models import Site
from django.shortcuts import get_object_or_404


class BlogViewMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, language=request.LANGUAGE_CODE)
        self.is_author = request.user == self.blog.author
        self.blog_absolute_uri = "http://%s%s" % (Site.objects.get_current().domain,
                                                  self.blog.get_absolute_url())
        return super(BlogViewMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            data = super(BlogViewMixin, self).get_context_data(**kwargs)
        except AttributeError:
            data = {}
        data["blog"] = self.blog
        data["is_author"] = self.is_author
        data["blog_absolute_uri"] = self.blog_absolute_uri
        return data
