from BeautifulSoup import BeautifulSoup, Tag
from django.template.base import BLOCK_TAG_START, BLOCK_TAG_END, \
    VARIABLE_TAG_START, VARIABLE_TAG_END, COMMENT_TAG_START, COMMENT_TAG_END
from django.template.context import Context
from django.template.loader import get_template_from_string
from django.utils.html import escape
import re


def fix_embeds(value):
    soup = BeautifulSoup(value, selfClosingTags=["param"])
    for object in soup.findAll("object"):
        movie = None
        for param in object.findAll("param"):
            if param["name"] == "movie":
                movie = param["value"]
        embeds = object.findAll("embed")
        if embeds:
            embed = embeds[0]
        else:
            embed = None
        data = object.get("data")
        if not data:
            if movie:
                object["data"] = movie
            elif embed and embed.get("src"):
                object["data"] = embed["src"]
            else:
                continue

        if not object.get("type") and embed.get("type"):
            object["type"] = embed["type"]
        del object["classid"]
        for embed in object.findAll("embed"):
            embed.extract()

    for embed in soup.findAll("embed"):
        src = embed.get("src")
        type = embed.get("type")
        if not src or not type:
            continue
        width = embed.get("width")
        height = embed.get("height")
        object = Tag(soup, "object")
        object["data"] = src
        object["type"] = type
        if width:
            object["width"] = width
        if height:
            object["height"] = height
        embed.replaceWith(object)


    return unicode(soup)


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


def render_text(text):

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
    return fix_embeds(get_template_from_string(text).render(Context()))

