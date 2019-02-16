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
#跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
      'localhost:63343',
      'localhost:8000',
      'localhost:8001',
      '127.0.0.1:8000',
      '127.0.0.1:8001',
      'http://localhost:63343',
      'http://localhost:8000',
      'http://localhost:8001',
      'http://127.0.0.1:8000',
      'http://127.0.0.1:8001',
      'chrome-extension://fhbjgbiflinjbdggehcddcbncdddomop'
)