from .installed_apps import INSTALLED_APPS
from .middleware import MIDDLEWARE

# Django debug toolbar
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE

INTERNAL_IPS = [
    '127.0.0.1',
]
