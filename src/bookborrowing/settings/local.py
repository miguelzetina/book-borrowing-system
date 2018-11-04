"""
Django settings with Docker container
"""
from . import *

# Debug
DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'bookborrowing',
        'USER': 'bookborrowing',
        'PASSWORD': 'password',
        'HOST': 'postgresql',
        'PORT': 5432,
    }
}