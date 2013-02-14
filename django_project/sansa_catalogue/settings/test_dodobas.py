from .django_project.sansa_catalogue.settings.test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac_new2',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    }
}
