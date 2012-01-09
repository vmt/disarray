# Django Settings
# Reference: http://docs.djangoproject.com/en/1.3/ref/settings/
#
import os

PROJECT_NAME = "disarray"
PROJECT_ROOT = os.path.dirname(__file__)

try:
    from local.settings import *
except ImportError:
    raise Exception("local.settings module not defined!")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_ROOT, 'local', 'stor', 'database.sqlite3')
    }
}


TEMPLATE_DEBUG     = DEBUG
MANAGERS           = ADMINS

MEDIA_ROOT         = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL          = '/media'
ADMIN_MEDIA_PREFIX = '/admin_media/'
LOGIN_URL          = '/login'
LOGIN_REDIRECT_URL = '/'

TEMPLATE_DIRS      = ( os.path.join(PROJECT_ROOT, 'templates'), )
LANGUAGE_CODE      = 'en-us'
TIME_ZONE          = 'America/Los_Angeles'
SITE_ID            = 1
USE_I18N           = True
USE_L10N           = True
ROOT_URLCONF       = PROJECT_NAME + '.urls'


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.markup',
    'taggit',
    'disarray.task',
)
