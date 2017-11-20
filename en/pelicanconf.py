import os
import sys

import markdown

sys.path.append("..")

from pelicanconf_base import *


AUTHOR = "Andrey Fedoseev"
SITENAME = "Andrey Fedoseev's Blog"
SITEURL = "http://andreyfedoseev.name"
FEED_DOMAIN = SITEURL
LANG_URLS = {
    "RU": "http://andreyfedoseev.ru"
}
DEFAULT_LANG = "en"

with open(os.path.join(PATH, "include", "about.md".format())) as about_file:
    ABOUT_SUMMARY = markdown.markdown(about_file.read().decode("utf-8"))
