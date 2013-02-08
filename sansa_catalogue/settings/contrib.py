from .base import *

# Extra installed apps
INSTALLED_APPS += [
    'offline_messages',
    'registration',
    'raven.contrib.django',
    'shapes',
    'django_extensions',
    'userprofile',
]

# Added by Tim for registration app
ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'noreply@catalogue.sansa.org.za'
#define organisation acronym, used in filenaming schemes
ORGANISATION_ACRONYM = 'SANSA'
