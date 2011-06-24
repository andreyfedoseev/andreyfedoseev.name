from blog.models import Blog
from django.shortcuts import get_object_or_404


class BlogViewMixin(object):

    def dispatch(self, request, *args, **kwargs):
        self.blog = get_object_or_404(Blog, language=request.LANGUAGE_CODE)
        self.is_author = request.user == self.blog.author
        return super(BlogViewMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super(BlogViewMixin, self).get_context_data(**kwargs)
        data["blog"] = self.blog
        data["is_author"] = self.is_author
        return data
