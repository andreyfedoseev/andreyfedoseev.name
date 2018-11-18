# coding: utf-8
import os
import sys

import markdown

from pelicanconf_base import *

CONTENT_PATH = os.path.join(os.path.dirname(__file__), "content")

AUTHOR = "Андрей Федосеев"
TELEGRAM = "https://t.me/andreyfedoseev_ru"
SITENAME = "Блог Андрея Федосеева"
SITEURL = "http://localhost:8000"
FEED_DOMAIN = SITEURL
LANG_URLS = {
    "EN": "http://andreyfedoseev.name"
}
DEFAULT_LANG = "ru"

with open(os.path.join(CONTENT_PATH, "include", "about.md"), encoding="utf=8") as about_file:
    ABOUT_SUMMARY = markdown.markdown(about_file.read())
