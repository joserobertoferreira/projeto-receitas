from .environment import BASE_DIR

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [BASE_DIR / 'resources', BASE_DIR / 'base_static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
