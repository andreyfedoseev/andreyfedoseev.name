from blog.models import Blog
from django.shortcuts import get_object_or_404, redirect


def frontpage(request):
    blog = get_object_or_404(Blog, language=request.LANGUAGE_CODE)
    return redirect(blog, permanent=True)