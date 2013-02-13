from .project import *

# http://hustoknow.blogspot.com/2011/02/setting-up-django-nose-on-hudson.html
INSTALLED_APPS += (
    'django_nose',  # don't remove this comma
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = (
    '--with-coverage',
    '--cover-erase',
    '--cover-html',
    '--cover-html-dir=xmlrunner/html',
    '--cover-inclusive',
    '--cover-package=catalogue',
    '--cover-package',
    '--cover-package=useraccounts',
    '--cover-package=search',
    '--nocapture',
    '--nologcapture',
    #  default test settings don't include any specific tests (see jenkins.py)
)


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# change this to a proper location
EMAIL_FILE_PATH = '/tmp/'


LOGGING = {
    # internal dictConfig version - DON'T CHANGE
    'version': 1,
    'disable_existing_loggers': True,
    # default root logger - handle with sentry
    'root': {
        'level': 'DEBUG',
        'handlers': ['nullhandler'],
    },
    'handlers': {
        'nullhandler': {
            'class': 'logging.NullHandler',
        },
    }
}
