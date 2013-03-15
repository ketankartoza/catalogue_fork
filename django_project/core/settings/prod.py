from .project import *

SENTRY_DSN = ('http://c9b3062853e34c2b857122d75d4ec663:'
              'ff3010968b4e47c0a84166da3c1842ae@sentry.linfiniti.com/3')

MIDDLEWARE_CLASSES = (
    'raven.contrib.django.middleware.SentryResponseErrorIdMiddleware',
    'raven.contrib.django.middleware.SentryLogMiddleware',
) + MIDDLEWARE_CLASSES

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
            'format': (
                '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
    },
    'handlers': {
        # send email to mail_admins, if DEBUG=False
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # sentry logger
        'sentry': {
            'level': 'WARNING',  # use LOG_LEVEL from settings_local
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        # console output, useful for debugging
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False
        },
        'raven': {
            'level': 'ERROR',
            'handlers': ['mail_admins'],
            'propagate': False
        },
        'sentry.errors': {
            'level': 'ERROR',
            'handlers': ['mail_admins'],
            'propagate': False
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'pycsw': {
            'handlers': ['sentry'],
            'level': 'ERROR',
            'propagate': False
        }
    }
}
