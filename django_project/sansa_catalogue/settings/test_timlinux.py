from .test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac-master',
        'USER': 'timlinux',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    }
}
