#Settings specific for production environment

from .base import *


DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_COOKIE_SECURE=False

SESSION_COOKIE_SECURE=True
