from .project import *


ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac_november',
        'USER': 'dodobas',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
        'TEST_NAME': 'sac_dev_unittest_master',
    }
}

PIPELINE_YUGLIFY_BINARY = ABS_PATH('node_modules', 'yuglify', 'bin', 'yuglify')

