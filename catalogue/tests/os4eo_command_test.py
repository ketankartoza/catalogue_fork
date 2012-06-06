"""
os4eo management command tests



>>> import os
>>> from django.conf import settings
>>> from django.core.management import call_command
>>> from catalogue.models import *

###############################################

Prepare testing, load fixtures and ingest
at least one DIMS product

###############################################


Load an initial fixture with dictionaries

>>> call_command('loaddata', 'fixtures/catalogue_dictionaries.json', verbosity=0)


TODO: tests

"""
