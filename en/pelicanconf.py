import sys
sys.path.append("..")

from pelicanconf_base import *


AUTHOR = "Andrey Fedoseev"
SITENAME = "Andrey Fedoseev's Weblog"
SITEURL = "http://localhost:8000"
FEED_DOMAIN = SITEURL
LANG_URLS = {
    "RU": ""
}
DEFAULT_LANG = "en"

with open(os.path.join(PATH, "include", "about.md".format())) as about_file:
    ABOUT_SUMMARY = about_file.read().decode("utf-8")
