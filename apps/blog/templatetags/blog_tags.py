# -*- coding: utf-8 -*- 

from BeautifulSoup import BeautifulSoup, Tag
from blog.models import Entry, Image, PHOTO_TYPE, VIDEO_TYPE
from django import template
from django.conf import settings
from django.contrib.humanize.templatetags.humanize import naturalday
from django.db.models.signals import post_save
from django.template import BLOCK_TAG_START, BLOCK_TAG_END, VARIABLE_TAG_START, \
    VARIABLE_TAG_END, COMMENT_TAG_START, COMMENT_TAG_END
from django.template.loader import get_template_from_string
from django.utils import translation
from django.utils.encoding import force_unicode, smart_str
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from pytils.dt import ru_strftime, distance_of_time_in_words
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
    if title:
        title = title[1:-1]
        
    return ImageNode(id, format, title)    


ESCAPE_RE = re.compile(r"(\{%\s*?escape\s*?(html)?\s*?%\}(.*?)\{%\s*?endescape.\s?%\})", re.S)
TEMPLATE_TAG_MAPPING = {
    BLOCK_TAG_START: '{% templatetag openblock %}',
    BLOCK_TAG_END: '{% templatetag closeblock %}',
    VARIABLE_TAG_START: '{% templatetag openvariable %}',
    VARIABLE_TAG_END: '{% templatetag closevariable %}',
    COMMENT_TAG_START: '{% templatetag opencomment %}',
    COMMENT_TAG_END: '{% templatetag closecomment %}',
}
TEMPLATE_TAGS_BITS_RE = re.compile("(%s)" % "|".join(TEMPLATE_TAG_MAPPING.keys()), re.S)


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

        for block, html, content in ESCAPE_RE.findall(text):
            escaped = u""
            for bit in TEMPLATE_TAGS_BITS_RE.split(content):
                escaped += TEMPLATE_TAG_MAPPING.get(bit, bit)
            if html:
                escaped = escape(escaped)
            text = text.replace(block, escaped) 

        prefix = """
                 {% load blog_tags %}
                 {% load oembed_tags %}
                 """
        text = prefix + text
        return fix_embeds(get_template_from_string(text).render(context))


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

@register.filter
def safe_markdown(value, arg=''):
    try:
        import markdown
    except ImportError:
        if settings.DEBUG:
            raise template.TemplateSyntaxError("Error in {% markdown %} filter: The Python markdown library isn't installed.")
        return force_unicode(value)
    else:
        # markdown.version was first added in 1.6b. The only version of markdown
        # to fully support extensions before 1.6b was the shortlived 1.6a.
        if hasattr(markdown, 'version'):
            extensions = [e for e in arg.split(",") if e]

            # Unicode support only in markdown v1.7 or above. Version_info
            # exist only in markdown v1.6.2rc-2 or above.
            if getattr(markdown, "version_info", None) < (1,7):
                return mark_safe(force_unicode(markdown.markdown(smart_str(value), extensions, safe_mode="escape")))
            else:
                return mark_safe(markdown.markdown(force_unicode(value), extensions, safe_mode="escape"))
        else:
            return mark_safe(force_unicode(markdown.markdown(smart_str(value))))
safe_markdown.is_safe = True


def fix_embeds(value):
    soup = BeautifulSoup(value)
    for object in soup.findAll("object"):
        movie = None
        for param in object.findAll("param"):
            if param['name'] == 'movie':
                movie = param['value']
        embeds = object.findAll("embed")
        if embeds:
            embed = embeds[0]
        else:
            embed = None
        data = object.get('data')
        if not data:
            if movie:
                object['data'] = movie
            elif embed and embed.get('src'):
                object['data'] = embed['src']
            else:
                continue
        object['type'] = 'application/x-shockwave-flash'
        del object['codebase']
        del object['clsid']
        del object['classid']
        for embed in object.findAll('embed'):
            embed.extract()
    
    for embed in soup.findAll('embed'):
        src = embed.get('src')
        if not src:
            continue
        width = embed.get('width')
        height = embed.get('height')
        object = Tag(soup, 'object')
        object['type'] = 'application/x-shockwave-flash'
        object['data'] = src
        if width:
            object['width'] = width
        if height:
            object['height'] = height
        object.insert(0, Tag(soup, 'param', [('name', 'movie'), ('value', src)]))
        embed.replaceWith(object)

                
    return unicode(soup)
