from .test import *

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sac-master',
        'USER': 'jenkins',
        'PASSWORD': 'jenkins-test',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST_NAME': 'sac_unittest_master',
    }
}

INSTALLED_APPS += (
    'django_jenkins',  # don't remove this comma
)

NOSE_ARGS += (
    '--with-xunit',
    '--xunit-file=xmlrunner/nosetests.xml',
    '--with-xcoverage',
    '--xcoverage-file=coverage.xml'
    # we need to specify which tests to execute
    # this is needed as we can't use Nose default test discoverer, because we
    # are still using tests customized for Django default test runner
    'catalogue.tests',
    'dictionaries.tests',
    'useraccounts.tests',
    'search.tests',
    'reports.tests'
)

#
# For django-jenkins integration
#
PROJECT_APPS = (
    'catalogue',
    'dictionaries',
    'useraccounts',
    'search',
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
    #'django_jenkins.tasks.run_sloccount',
)
