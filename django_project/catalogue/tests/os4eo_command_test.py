"""
os4eo management command tests



>>>
>>> from django.core.management import call_command
>>>

###############################################

Prepare testing, load fixtures and ingest
at least one DIMS product

###############################################


Load an initial fixture with dictionaries

>>> call_command('loaddata', 'fixtures/catalogue_dictionaries.json', verbosity=0)


TODO: tests

"""
