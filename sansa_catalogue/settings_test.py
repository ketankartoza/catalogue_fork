# This settings file is used for running tests.
# You can use if for example like this:
#
# python manage.py test --settings=sansa_catalogue.settings_test
#
# If running on a remote server you should have a virtual frame buffer
# enabled and mozilla firefox installed so that the selenium tests can run
# This applies to running it on Jenkins too. Here is how you might invoke
# it with aframebuffer (though note that its easier in Jenkins to just
# use the xfvb plugin):

# xvfb-run --server-args="-screen 0, 1024x768x24" \
# python manage.py test --settings=sansa_catalogue.settings_test

# This is an exception to our 'dont import globally' rule
from settings import *

# See http://hustoknow.blogspot.com/2011/02/setting-up-django-nose-on-hudson.html
INSTALLED_APPS += (
    'django_nose',
    'django_jenkins', # don't remove this comma
)


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--cover-html',
    '--cover-html-dir=xmlrunner/html',
    '--cover-inclusive',
    '--cover-package=catalogue',
    '--cover-package=dictionaries',
    '--nocapture',
    '--nologcapture',
]

JENKINS_NOSE_ARGS = (
    '--with-xunit',
    '--xunit-file=xmlrunner/nosetests.xml',
    '--with-xcoverage',
    '--xcoverage-file=coverage.xml')

NOSE_ARGS += JENKINS_NOSE_ARGS

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# change this to a proper location
EMAIL_FILE_PATH = '/tmp/'

#COVERAGE_MODULE_EXCLUDES = [
#        'tests$',
#        'settings$',
#        '^urls$',
#        'locale$',
#        '__init__',
#        'django',
#        'migrations',
#    ]

#coverage.use_cache(False)
#for e in COVERAGE_MODULE_EXCLUDES:
#    coverage.exclude(e)
#coverage.start()

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

#
# For django-jenkins integration
#
PROJECT_APPS = (
    'catalogue',
    )

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.django_tests',
    #'django_jenkins.tasks.run_pep8',
    # Needs rhino or nodejs
    #'django_jenkins.tasks.run_jslint',
    #'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_sloccount',
    )
