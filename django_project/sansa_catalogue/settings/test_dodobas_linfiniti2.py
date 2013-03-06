from .test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac_dev_dodobas',
        'USER': 'dodobas',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
        'TEST_NAME': 'sac_dev_unittest_master',
    }
}
