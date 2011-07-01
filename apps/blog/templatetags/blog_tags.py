# -*- coding: utf-8 -*-
from blog.models import Image, Blog
from django import template
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import translation
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from pytils.dt import ru_strftime, distance_of_time_in_words
import datetime
import re
import shlex
import subprocess
import markdown


register = template.Library()


class ImageNode(template.Node):
    
    def __init__(self, id, format, title):
        self.id = id
        self.format = format
        self.title = title

    def build_absolute_uri(self, request, url):
        if request:
            return request.build_absolute_uri(url)
        return url
        
    def render(self, context):
        try:
            image = Image.objects.get(pk=self.id)
        except Image.DoesNotExist:
            return u""
        request = context.get('request')
        title = self.title or image.image.name.split('/')[-1]
        data = {
            'title': title,
            'original_url': self.build_absolute_uri(request, image.image.url),
            'original_width': image.image.width,
            'original_height': image.image.height,
            'thumb_url': self.build_absolute_uri(request, image.image.thumbnail.absolute_url),
            'thumb_width': image.image.thumbnail.width(),
            'thumb_height': image.image.thumbnail.height(),
            'scaled_url': self.build_absolute_uri(request, image.image.extra_thumbnails['scaled'].absolute_url),
            'scaled_width': image.image.extra_thumbnails['scaled'].width(),
            'scaled_height': image.image.extra_thumbnails['scaled'].height(),
        }            
        return IMAGE_FORMATS[self.format] % data
        

IMAGE_FORMATS = {
    'original': """<img src="%(original_url)s" alt="%(title)s" width="%(original_width)i" height="%(original_height)i" />""",
    'thumb': """<img src="%(thumb_url)s" alt="%(title)s" width="%(thumb_width)i" height="%(thumb_height)i" />""",
    'thumb-lightbox': """<a href="%(original_url)s" title="%(title)s" class="lightbox"><img src="%(thumb_url)s" alt="%(title)s" width="%(thumb_width)i" height="%(thumb_height)i" /></a>""",
    'scaled': """<img src="%(scaled_url)s" alt="%(title)s" width="%(scaled_width)i" height="%(scaled_height)i" />""",
    'scaled-lightbox': """<a href="%(original_url)s" title="%(title)s" class="lightbox"><img src="%(scaled_url)s" alt="%(title)s" width="%(scaled_width)i" height="%(scaled_height)i" /></a>""",
}        
        
@register.tag(name="image")
def do_image(parser, token):
    parts = token.split_contents()
    tag_name = parts[0]
    args = parts[1:]
    if not args or len(args) > 3:
        raise template.TemplateSyntaxError, "%r tag requires from one to three arguments" % tag_name
    try:
        id = int(args[0])
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag first argument must be integer" % tag_name

    format = None
    title = ""
    for arg in args[1:]:
        if arg.startswith('"') and arg.startswith('"'):
            title = arg
        else:
            format = arg
    if not format:
        format = 'original' 
    if format not in IMAGE_FORMATS: 
        raise template.TemplateSyntaxError, "%r tag second argument must be one of %s" % \
             (tag_name, ', '.join(['%s' % f for f in IMAGE_FORMATS]))
    if title and (not title.startswith('"') or not title.endswith('"')):
        raise template.TemplateSyntaxError, "%r title must be in quotes" % tag_name
    if title:
        title = title[1:-1]
        
    return ImageNode(id, format, title)    


class HightlightNode(template.Node):
    
    def __init__(self, nodelist, format):
        self.nodelist = nodelist
        self.format = format
        
    def render(self, context):
        output = self.nodelist.render(context)
        args = shlex.split("highlight -S %s -f" % str(self.format))
        try:
            p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            out, errors = p.communicate(output.encode('utf-8'))
            if out:
                output = out.decode('utf-8')
        except:
            pass
        
        return output


@register.tag(name="highlight")
def do_highlight(parser, token):
    parts = token.split_contents()
    tag_name = parts[0]
    args = parts[1:]
    if len(args) != 1:
        raise template.TemplateSyntaxError, "%r tag requires exactly one argument" % tag_name
    nodelist = parser.parse(('endhighlight',))
    parser.delete_first_token()    
    return HightlightNode(nodelist, args[0])    


OEMBED_RE = re.compile(r"\{%\s*?oembed.*?%\}(.*?)\{%\sendoembed.*?\s%}", re.M)
YOUTUBE_URL_RE = re.compile(r"http://www.youtube.com/watch\?v=(\w*)")


@register.filter
def humanized_date(date):
    if not isinstance(date, datetime.datetime):
        return u""

    language = translation.get_language()

    delta = datetime.datetime.now() - date 
    if language == 'ru':
        if delta.days > 5:
            return ru_strftime(format=u"%d %B %Y", date=date, inflected=True) + " года".decode('utf-8')
        else:
            return distance_of_time_in_words(date) 
    return naturalday(date)


@register.inclusion_tag("blog/include/localized-flatblock.html", takes_context=True)
def localized_flatblock(context, name):
    request = context["request"]
    name = "%s-%s" % (name, request.LANGUAGE_CODE)
    return dict(name=name)


@register.inclusion_tag("blog/include/locale-switcher.html", takes_context=True)
def locale_switcher(context):
    blog = context["blog"]
    blogs = list(Blog.objects.exclude(id=blog.id))
    for blog in blogs:
        blog.message = translation.trans_real.translation(blog.language).gettext("lang-switcher-message-%s" % blog.language)
    return dict(blogs=blogs)

# Mark these strings as translatable so they are added to django.po
_("lang-switcher-message-ru")
_("lang-switcher-message-en")