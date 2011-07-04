from project.settings import *

DATABASES = {
    'default': {
        'NAME': 'andreyfedosev_name',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': '',
        'PASSWORD': ''
    },
}

GRAVATAR_DEFAULT_IMAGE = "http://andreyfedoseev.name" + STATIC_URL + "blog/images/default-avatar.png"

SECRET_KEY = ''

AKISMET_KEY = ""