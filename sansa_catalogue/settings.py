import os
# This is an exception to our 'dont import globally' rule
from settings_local import *

# See: http://www.djangobook.com/en/1.0/chapter12/#cn222
AUTH_PROFILE_MODULE = 'catalogue.SacUserProfile'

# Django settings for sac_catalogue project.

MANAGERS = ADMINS
DATABASES = {
        'default': {  # new db that does not mimic acs system
         'ENGINE': 'django.contrib.gis.db.backends.postgis',
         'NAME': DBNAME,
         'USER': DBUSER,
         'PASSWORD': DBPASSWORD,
         'HOST': DBHOST,
         'PORT': DBPORT,
         'TEST_NAME': DBTEST,
         },
        'acs': {  # legacy acs port to django
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': ACSDBNAME,
         'USER': ACSDBUSER,
         'PASSWORD': ACSDBPASSWORD,
         'HOST': ACSDBHOST,
         'PORT': ACSDBPORT,
         }
        }
DATABASE_ROUTERS = ['catalogue.dbrouter.CatalogueRouter']

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: '/home/media/media.lawrence.com/media/'
MEDIA_ROOT = os.path.join(ROOT_PROJECT_FOLDER, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: 'http://media.lawrence.com/media/', 'http://example.com/media/'
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' 'static/' subdirectories and in STATICFILES_DIRS.
# Example: '/home/media/media.lawrence.com/static/'
STATIC_ROOT = os.path.join(ROOT_PROJECT_FOLDER, 'static')

# URL prefix for static files.
# Example: 'http://media.lawrence.com/static/'
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like '/home/html/static' or 'C:/www/django/static'.
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT_PROJECT_FOLDER, 'project_static_files'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'c(x1$mngg*&#re1shf2r3(j&1&rl528_ubo2#x_)ljabk2*cly'

# List of callables that know how to import templates from various sources.
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
MIDDLEWARE_CLASSES += EXTRA_MIDDLEWARE_CLASSES

TEMPLATE_DEBUG = DEBUG
LOGGING_OUTPUT_ENABLED = DEBUG
LOGGING_LOG_SQL = DEBUG

ROOT_URLCONF = 'sansa_catalogue.urls'

TEMPLATE_DIRS = (
    os.path.join(ROOT_PROJECT_FOLDER, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.gis',
    'django.contrib.messages',
    'offline_messages',
    'django_nose',
    'registration',
    'raven.contrib.django',  # for sentry logging
    'catalogue',
    #'acscatalogue',
    'shapes',
    'django_extensions',
    'userprofile',
)
INSTALLED_APPS += EXTRA_INSTALLED_APPS

#where to take the user after they logged in
LOGIN_REDIRECT_URL = '/'
#where to take the user if they try to access a page requiring a logged in user
LOGIN_URL = '/accounts/login/'

#for userprofile app
I18N_URLS = False
DEFAULT_AVATAR = os.path.join(MEDIA_ROOT, 'generic.jpg')
AVATAR_WEBSEARCH = False

#limit the number of returned metadata records
MAX_METADATA_RECORDS = 500

# South is currently disabled
SOUTH_MIGRATION_MODULES = {
  'acs': 'ignore',
}

# For offline messages app
MESSAGE_STORAGE = 'offline_messages.storage.OfflineStorageEngine'


#
# Sentry settings - logs exceptions to a database
# see http://sentry.sansa.org.za/account/projects/catalogue-live/docs/django/

LOGGING = {
    # internal dictConfig version - DON'T CHANGE
    'version': 1,
    'disable_existing_loggers': True,
    # default root logger - handle with sentry
    'root': {
        'level': 'DEBUG',
        'handlers': ['sentry'],
    },
    'formatters': {
        # define output formats
        'verbose': {
            'format': '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'filters': {
        # user defined filters
        'require_debug_false': {
            # activate only if DEBUG=False
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # send email to mail_admins, if DEBUG=False
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # sentry logger
        'sentry': {
            'level': LOG_LEVEL, #  use LOG_LEVEL from settings_local
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        # console output, useful for debugging
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'temp_log.log',
        },
    },
    'loggers': {
        # in case of an ERROR with raven/sentry send an email to project admins
        'raven': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'sentry.errors': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },

        # i.e. log every db query to the file, only if DEBUG=True
        # https://docs.djangoproject.com/en/1.4/topics/logging/#django-db-backends

        # 'django.db.backends': {
        #     'handlers': ['file'],
        # }
    }
}