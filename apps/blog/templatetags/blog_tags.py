# -*- coding: utf-8 -*-
from blog.models import Image, Blog
from django import template
from django.contrib.humanize.templatetags.humanize import naturalday
from django.utils import translation
from django.utils.translation import ugettext as _
from pytils.dt import ru_strftime, distance_of_time_in_words
from sorl.thumbnail import get_thumbnail
import datetime
import re
import shlex
import subprocess


register = template.Library()


class ImageNode(template.Node):

    def __init__(self, id, format, title):
        self.id = id
        self.format = format
        self.title = title

    def render(self, context):
        try:
            image = Image.objects.get(pk=self.id)
        except Image.DoesNotExist:
            return u""
        title = self.title or image.image.name.split('/')[-1]
        thumbnail = get_thumbnail(image.image, Image.THUMBNAIL_GEOMETRY)
        scaled = get_thumbnail(image.image, Image.SCALED_GEOMETRY)
        fotorama = get_thumbnail(image.image, Image.FOTORAMA_GEOMETRY)
        fotorama_thumbnail = get_thumbnail(image.image, Image.FOTORAMA_THUMBNAIL_GEOMETRY)
        data = {
            'title': title,
            'original_url': image.image.url,
            'original_width': image.image.width,
            'original_height': image.image.height,
            'thumb_url': thumbnail.url,
            'thumb_width': thumbnail.width,
            'thumb_height': thumbnail.height,
            'scaled_url': scaled.url,
            'scaled_width': scaled.width,
            'scaled_height': scaled.height,
            'fotorama_url': fotorama.url,
            'fotorama_width': fotorama.width,
            'fotorama_height': fotorama.height,
            'fotorama_thumbnail_url': fotorama_thumbnail.url,
            'fotorama_thumbnail_width': fotorama_thumbnail.width,
            'fotorama_thumbnail_height': fotorama_thumbnail.height,
        }
        return IMAGE_FORMATS[self.format] % data


IMAGE_FORMATS = {
    'figure': """<figure><a href="%(original_url)s" title="%(title)s"><img src="%(scaled_url)s" alt="%(title)s" width="%(scaled_width)i" height="%(scaled_height)i" /></a><figcaption>%(title)s</figcaption></figure>""",
    'original': """<img src="%(original_url)s" alt="%(title)s" width="%(original_width)i" height="%(original_height)i" />""",
    'thumb': """<img src="%(thumb_url)s" alt="%(title)s" width="%(thumb_width)i" height="%(thumb_height)i" />""",
    'thumb-lightbox': """<a href="%(original_url)s" title="%(title)s" class="lightbox"><img src="%(thumb_url)s" alt="%(title)s" width="%(thumb_width)i" height="%(thumb_height)i" /></a>""",
    'scaled': """<img src="%(scaled_url)s" alt="%(title)s" width="%(scaled_width)i" height="%(scaled_height)i" />""",
    'scaled-lightbox': """<a href="%(original_url)s" title="%(title)s" class="lightbox"><img src="%(scaled_url)s" alt="%(title)s" width="%(scaled_width)i" height="%(scaled_height)i" /></a>""",
    'fotorama': """<a href="%(fotorama_url)s" title="%(title)s"><img src="%(fotorama_thumbnail_url)s" alt="%(title)s" width="%(fotorama_thumbnail_width)i" height="%(fotorama_thumbnail_height)i" /></a>""",
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
