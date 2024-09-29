# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
from .environment import BASE_DIR

LANGUAGE_CODE = 'pt'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]
