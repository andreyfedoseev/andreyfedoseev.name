from blog.models import Entry, Image, PHOTO_TYPE, VIDEO_TYPE
from django import template
from django.template.loader import get_template_from_string
from django.utils.translation import ugettext as _
import re


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
        request = context['request']
        title = self.title or image.image.name.split('/')[-1]
        data = {
            'title': title,
            'original_url': request.build_absolute_uri(image.image.url),
            'original_width': image.image.width,
            'original_height': image.image.height,
            'thumb_url': request.build_absolute_uri(image.image.thumbnail.absolute_url),
            'thumb_width': image.image.thumbnail.width(),
            'thumb_height': image.image.thumbnail.height(),
            'scaled_url': request.build_absolute_uri(image.image.extra_thumbnails['scaled'].absolute_url),
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
        
    return ImageNode(id, format, title)    


class EntryTextNode(template.Node):
    
    def __init__(self, var, format):
        self.var = template.Variable(var)
        self.format = format
        
    def render(self, context):
        try:
            var = self.var.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        if isinstance(var, basestring):
            entry = None
            text = var
        elif isinstance(var, Entry):
            entry = var
            text = entry.text
            
        request = context['request']
            
        if entry and self.format == 'short':
            parts = text.split('<!-- more -->', 1)
            if len(parts) > 1:
                text = parts[0]
                text += """<p class="read-more"><a href="%s#cut">%s</a></p>""" % (request.build_absolute_uri(entry.get_absolute_url()), _(u"Read more"))
        text = text.replace('<!-- more -->', '<a name="cut"></a>')         
        prefix = """
                 {% load blog_tags %}
                 {% load oembed_tags %}
                 """
        text = prefix + text
        return get_template_from_string(text).render(context)


@register.tag(name="render_text")
def do_entry_text(parser, token):
    parts = token.split_contents()
    tag_name = parts[0]
    args = parts[1:]
    if len(args) < 1 or len(args) > 2:
        raise template.TemplateSyntaxError, "%r tag requires from one to two arguments" % tag_name
    format = None
    if len(args) == 2:
        format = args[1]
        if format != 'short':
            format = None
    return EntryTextNode(args[0], format)    


OEMBED_RE = re.compile(r"\{%\s*?oembed.*?%\}(.*?)\{%\sendoembed.*?\%}", re.M)
YOUTUBE_URL_RE = re.compile(r"http\://www.youtube.com/watch\?v=(\w*)")


@register.filter
def cover(entry):
    if not isinstance(entry, Entry):
        return None

    if entry.entry_type == PHOTO_TYPE:
        try:
            return entry.image_set.all()[0].image.extra_thumbnails['scaled'].absolute_url 
        except IndexError:
            pass
    elif entry.entry_type == VIDEO_TYPE:
        oembeds = OEMBED_RE.findall(entry.text)
        for oembed in oembeds: 
            for youtube_video in YOUTUBE_URL_RE.findall(oembed):
                return "http://i.ytimg.com/vi/%s/0.jpg" % youtube_video
    
    return None 
        