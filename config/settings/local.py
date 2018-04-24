from .base import *

SECRET_KEY = env(
    'DJANGO_SECRET_KEY',
    default='%&*hjf890ujs0d9f&*__===fsjdifj09j++89^(*YH('
)

DEBUG = env.bool('DJANGO_DEBUG', default=True)

ALLOWED_HOSTS = [
    '172.16.19.130',
    'localhost',
    '127.0.0.1',
    '*',
]
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
      'localhost:63343',
)