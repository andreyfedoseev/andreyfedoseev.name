import os
import sys

import markdown

from pelicanconf_base import *

CONTENT_PATH = os.path.join(os.path.dirname(__file__), "content")

AUTHOR = "Andrey Fedoseev"
SITENAME = "Andrey Fedoseev's Blog"
SITEURL = "http://localhost:8000"
TELEGRAM = "https://t.me/andreyfedoseev_en"
FEED_DOMAIN = SITEURL
LANG_URLS = {
    "RU": "http://andreyfedoseev.ru"
}
DEFAULT_LANG = "en"

with open(os.path.join(CONTENT_PATH, "include", "about.md"), encoding="utf=8") as about_file:
    ABOUT_SUMMARY = markdown.markdown(about_file.read())
