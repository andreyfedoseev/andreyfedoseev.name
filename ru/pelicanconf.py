# coding: utf-8
from __future__ import unicode_literals
import sys
sys.path.append("..")

from pelicanconf_base import *

AUTHOR = "Андрей Федосеев"
SITENAME = "Блог Андрея Федосеева"
SITEURL = "http://localhost:8000"
FEED_DOMAIN = SITEURL
LANG_URLS = {
    "RU": ""
}
DEFAULT_LANG = "ru"

with open(os.path.join(PATH, "include", "about.md".format())) as about_file:
    ABOUT_SUMMARY = about_file.read().decode("utf-8")
