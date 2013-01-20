import os
import logging

gettext = lambda s: s

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

TIME_ZONE = 'America/Chicago'

LANGUAGES = (
    ('ru', gettext('Russian')),
    ('en', gettext('English')),
)

LANGUAGE_CODE = 'ru'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# Static file configuration
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "..", "static")
STATIC_URL = "/static/"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
    'less.finders.LessFinder',
    'coffeescript.finders.CoffeescriptFinder',
)

# Don't share this with anybody.
SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'project.middleware.LocaleMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'project.urls'


INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.markup',
    'django_extensions',
    'pytils',
    'debug_toolbar',
    'compressor',
    'south',
    'sorl.thumbnail',
    'simplegravatar',
    'annoying',
    'oembed',
    'robots',
    'tagging',
    'haystack',
    'coffeescript',
    'less',
    'flatblocks',
    'utils',
    'blog',
    'project',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
)

SITE_ID = 1

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

FORCE_LOWERCASE_TAGS = True
MAX_TAG_LENGTH = 100

SIMPLEGRAVATAR_DEFAULT = "identicon"

LOGIN_URL = "/login"

COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]

HAYSTACK_SITECONF = "project.search_sites"
HAYSTACK_SEARCH_ENGINE = "solr"
HAYSTACK_SOLR_URL = 'http://127.0.0.1:8393/solr/andreyfedoseev_name'
HAYSTACK_INCLUDE_SPELLING = True

THUMBNAIL_QUALITY = 90

LOGIN_REDIRECT_URL = "/"
