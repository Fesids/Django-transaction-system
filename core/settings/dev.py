from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

SECRET_KEY = 'secret'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'django_transacao',
        'USER': 'root',
        'PASSWORD': '67890000',
        'PORT': '3306',
        'HOST': 'localhost'
    }
}


CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:5173",
    "http://localhost:5173"
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:5173/",
    "http://127.0.0.1:5173",
    "http://localhost:5173/",
    "http://localhost:5173",
]

CORS_ALLOWED_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'