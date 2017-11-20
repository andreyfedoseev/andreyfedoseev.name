# coding: utf-8
from __future__ import unicode_literals
from pelican.utils import SafeDatetime
from pyembed.markdown import PyEmbedMarkdown
from pytils.dt import ru_strftime
import datetime


AUTHOR = "Andrey Fedoseev"
SITENAME = "Andrey Fedoseev's Weblog"
SITEURL = ""
LANG_URLS = {
    "RU": ""
}
DEFAULT_LANG = "en"
PATH = "content"
OUTPUT_PATH = "output/"
THEME = "../theme"
STATIC_PATHS = [
    "images",
]

JINJA_EXTENSIONS = (
    "jinja2.ext.i18n",
)


PLUGIN_PATHS = (
    "../plugins",
)

PLUGINS = (
    "i18n",
    "feeds",
)

PAGES_PATHS = (
    "pages",
)
PAGE_EXCLUDES = [
    "include",
]
ARTICLES_PATHS = (
    "blog",
)
ARTICLE_EXCLUDES = [
    "include",
]

DIRECT_TEMPLATES = (
    "index",
    "tags",
    "archives",
    "about",
    "robots",
    "sitemap",
    "error",
)

AUTHORS_SAVE_AS = ""
CATEGORIES_SAVE_AS = ""

INDEX_SAVE_AS = "blog/index.html"
INDEX_URL = "/blog/"

ARCHIVES_SAVE_AS = "blog/archive/index.html"
ARCHIVE_URL = "/blog/archive/"

ARTICLE_SAVE_AS = "blog/articles/{slug}/index.html"
ARTICLE_URL = "/blog/articles/{slug}/"

TAGS_SAVE_AS = "blog/topics/index.html"
TAGS_URL = "/blog/topics/"
TAG_SAVE_AS = "blog/topics/{slug}/index.html"
TAG_URL = "/blog/topics/{slug}/"

ABOUT_SAVE_AS = "about/index.html"
ABOUT_URL = "/about/"

ROBOTS_SAVE_AS = "robots.txt"
SITEMAP_SAVE_AS = "sitemap.xml"
ERROR_SAVE_AS = "error.html"

DEFAULT_PAGINATION = False

TIMEZONE = "Asia/Yekaterinburg"

# Feed generation is usually not desired when developing
FEED_DOMAIN = SITEURL
FEED_ATOM = None
FEED_RSS = "blog/feeds/rss.xml"
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
CATEGORY_FEED_RSS = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TAG_FEED_ATOM = None
TAG_FEED_RSS = "blog/feeds/%s.rss.xml"
TRANSLATION_FEED_ATOM = None
TRANSLATION_FEED_RSS = None


# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

MD_EXTENSIONS = (
    "codehilite(css_class=codehilite)",
    "extra",
    PyEmbedMarkdown(),
)

DATE_FORMATS = {
    "en": b"%B %d, %Y",
    "ru": b"%d %B %Y",
}

TODAY = datetime.date.today()


def sort_tags(tags_and_articles):
    return [tag for tag, articles in sorted(tags_and_articles, reverse=True, key=lambda x: len(x[1]))]


def format_date(date, lang):
    if isinstance(date, SafeDatetime):
        date = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond, date.tzinfo)
    date_format = DATE_FORMATS[lang]
    if lang == "ru":
        return ru_strftime(date_format, date, inflected=True)
    return date.strftime(date_format)


def get_month_name(date, lang):
    if isinstance(date, SafeDatetime):
        date = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute, date.second, date.microsecond, date.tzinfo)
    date_format = "%B"
    if lang == "ru":
        return ru_strftime(date_format, date)
    return date.strftime(date_format)


def build_archive(articles, lang):
    archive = {}

    month_names = {}

    for article in articles:
        date = article.date
        year, month, day = date.year, date.month, date.day
        if year not in archive:
            archive[year] = {}
        if month not in month_names:
            month_names[month] = get_month_name(date, lang)
        if month not in archive[year]:
            archive[year][month] = []
        archive[year][month].append((day, article))

    for year in archive:
        for month in archive[year]:
            archive[year][month] = sorted(archive[year][month], key=lambda x: x[1].date)
        archive[year] = [(month_names[month], articles) for month, articles in sorted(archive[year].items())]

    return sorted(archive.items(), reverse=True)


JINJA_FILTERS = {
    "sort_tags": sort_tags,
    "format_date": format_date,
    "build_archive": build_archive,
}
