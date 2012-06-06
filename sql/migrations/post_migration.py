#!/usr/bin/env python

"""
From: http://djangosnippets.org/snippets/696/

This script fix missing permissions or contenttypes after a SQL manual
migration

Can be run from project dir with
$ python manage.py runscript -v 2 --pythonpath=./sql/migrations post_migration.py

"""

from django.core.management import setup_environ
try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Couldn't find the settings.py module.")
    sys.exit(1)

setup_environ(settings)

# Add any missing content types
print "update_all_contenttypes ok"

from django.contrib.contenttypes.management \
    import update_all_contenttypes
update_all_contenttypes()

# Add any missing permissions
from django.contrib.auth.management import create_permissions
from django.db.models import get_apps

print "create_permissions ok"

for app in get_apps():
    create_permissions(app, None, 2)
