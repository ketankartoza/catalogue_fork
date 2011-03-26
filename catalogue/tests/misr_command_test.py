"""

Tests ingestion

>>> import os
>>> from django.conf import settings
>>> from django.core.management import call_command
>>> from catalogue.models import *

###############################################

Prepare testing, load fixtures

###############################################


Load an initial fixture with dictionaries

>>> call_command('loaddata', 'fixtures/catalogue_dictionaries.json', verbosity=0)


###############################################

Test ingestion

###############################################

Command: python manage.py misr_ingest -v 0 -m 3

>>> call_command('misr_ingest', verbosity=0, maxproducts=3, rcfileskip=True)


###############################################

Test that everything was imported correctly

###############################################

Tests import was complete

###############################################

Cleanup

###############################################

