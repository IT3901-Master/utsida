#Settings specific for production environment

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE=True

SESSION_COOKIE_SECURE=True
