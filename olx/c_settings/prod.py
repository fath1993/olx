from olx.settings import *

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

CSRF_TRUSTED_ORIGINS = []

ALLOWED_HOSTS = ['*']

POSTGRES_USER = env("POSTGRES_USER")
POSTGRES_PASSWORD = env("POSTGRES_PASSWORD")

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': f'db_main',
    'USER': f'{POSTGRES_USER}',
    'PASSWORD': f'{POSTGRES_PASSWORD}',
    'HOST': 'db',
    'PORT': '5432',
}

DATABASES['log_db'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': f'db_log',
    'USER': f'{POSTGRES_USER}',
    'PASSWORD': f'{POSTGRES_PASSWORD}',
    'HOST': 'db',
    'PORT': '5432',
}


