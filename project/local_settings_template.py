from project.settings import *

DATABASE_ENGINE = 'postgresql_psycopg2'    # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = ''
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.

GRAVATAR_DEFAULT_IMAGE = "http://localhost:8000" + STATIC_URL + "blog/images/default-avatar.png"

SECRET_KEY = ''

