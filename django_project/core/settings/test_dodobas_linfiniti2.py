from .test import *

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

# define yuglify binary...
# pip install virtual-node
# npm install yuglify
PIPELINE_YUGLIFY_BINARY = ABS_PATH('node_modules', 'yuglify', 'bin', 'yuglify')
