from .dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac_new2',
        'USER': 'dodobas',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
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
        # console output, useful for debugging
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            # 'level': 'DEBUG',
        }
    },
    # 'loggers': {
    #     'pycsw': {
    #         'handlers': ['console'],
    #         'level': 'DEBUG',
    #        'propagate': True
    #    }
    # }
}

# set up devserver if installed
try:
    import devserver
    INSTALLED_APPS += (
        'devserver',
    )
except ImportError:
    pass

# These are optional - only set if you have wierd issues like DataSource
# unknown
GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'
GDAL_LIBRARY_PATH = '/usr/lib/libgdal1.7.0.so.1'
