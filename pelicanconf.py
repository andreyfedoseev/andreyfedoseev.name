# coding: utf-8
from __future__ import unicode_literals

AUTHOR = "Andrey Fedoseev"
SITENAME = "Andrey Fedoseev's Weblog"
SITEURL = ""

JINJA_EXTENSIONS = [
    "jinja2.ext.i18n",
]

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["i18n_subsites"]

I18N_SUBSITES = {
    "en": {
        "SITENAME": "Andrey Fedoseev's Weblog",
        "OUTPUT_PATH": "./output/",
    },
    "ru": {
        "SITENAME": "Блог Андрея Федосеева",
        "OUTPUT_PATH": "./output/ru",
    },
}

THEME = "theme"

PATH_METADATA = "blog/(?P<lang>en|ru)"

PATH = "content"
PAGES_PATHS = ["pages"]
ARTICLES_PATHS = ["blog"]


AUTHORS_SAVE_AS = ""
ARCHIVES_SAVE_AS = ""

INDEX_SAVE_AS = "blog/index.html"
INDEX_URL = "blog/"

ARTICLE_SAVE_AS = "blog/{slug}/index.html"
ARTICLE_URL = "blog/{slug}/"

CATEGORIES_SAVE_AS = "blog/categories/index.html"
CATEGORY_SAVE_AS = "blog/categories/{slug}/index.html"
CATEGORY_URL = "blog/categories/{slug}/"

TAGS_SAVE_AS = "blog/tags/index.html"
TAG_SAVE_AS = "blog/tag/{slug}/index.html"
TAG_URL = "blog/tag/{slug}/"

YEAR_ARCHIVE_SAVE_AS = "blog/archive/{date:%Y}/index.html"


PAGINATION_PATTERNS = (
    (1, "{base_name}/", "{base_name}/index.html"),
    (2, "{base_name}/page/{number}/", "{base_name}/page/{number}/index.html"),
)

TIMEZONE = "Asia/Yekaterinburg"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

MD_EXTENSIONS = ["extra"]
