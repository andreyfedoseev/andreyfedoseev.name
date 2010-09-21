import os
import logging

gettext = lambda s: s

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
)

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

INTERNAL_IPS = ('127.0.0.1',)

DATABASE_ENGINE = 'sqlite3'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'project.db'
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

TIME_ZONE = 'America/Chicago'

LANGUAGES = (
    ('ru', gettext('Russian')),
#    ('en', gettext('English')),
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
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'media')
STATIC_URL = MEDIA_URL
STATICFILES_EXCLUDED_APPS = (
    'project',
)
STATICFILES_MEDIA_DIRNAMES = (
    'media',
    'static',
)
STATICFILES_PREPEND_LABEL_APPS = (
    'django.contrib.admin',
)

ADMIN_MEDIA_ROOT = os.path.join(STATIC_ROOT, 'admin_media')
ADMIN_MEDIA_PREFIX = '/admin_media/'


# Don't share this with anybody.
SECRET_KEY = ''

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'johnny.middleware.LocalStoreClearMiddleware',
    'johnny.middleware.QueryCacheMiddleware',
    'django_notify.middleware.NotificationsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'project.urls'


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.markup',
    'debug_toolbar',
    'johnny',
    'staticfiles',
    'compressor',
#    'south',
    'pytils',
    'robots',
    'sorl.thumbnail',
    'blueprint',
    'jquery',
    'oembed',
    'gravatar',
    'registration',
    'tagging',
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
    "django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "staticfiles.context_processors.static_url",
    'django_notify.context_processors.notifications',
)

SITE_ID = 1

GRAVATAR_DEFAULT_IMAGE = "http://andreyfedoseev.name" + STATIC_URL + "blog/images/default-avatar.png"

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

CACHE_BACKEND = 'johnny.backends.memcached://localhost:11211'
JOHNNY_MIDDLEWARE_KEY_PREFIX = 'jc_andreyfedoseev.name'

FORCE_LOWERCASE_TAGS = True
MAX_TAG_LENGTH = 100

