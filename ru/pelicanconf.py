# coding: utf-8
from __future__ import unicode_literals

import os
import sys

import markdown

sys.path.append("..")

from pelicanconf_base import *

AUTHOR = "Андрей Федосеев"
TELEGRAM = "https://t.me/andreyfedoseev_ru"
SITENAME = "Блог Андрея Федосеева"
SITEURL = "http://localhost:8080"
FEED_DOMAIN = SITEURL
LANG_URLS = {
    "EN": "http://andreyfedoseev.name"
}
DEFAULT_LANG = "ru"

with open(os.path.join(PATH, "include", "about.md".format())) as about_file:
    ABOUT_SUMMARY = markdown.markdown(about_file.read().decode("utf-8"))
