from .settings_default import *

SECRET_KEY = '123'

DEBUG = True
SENDPULSE_DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'b4',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

import os
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'files', 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'files', 'static')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DADATA_API_KEY = ''
