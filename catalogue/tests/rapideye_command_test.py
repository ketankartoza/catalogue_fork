"""

Tests ingestion

>>> from django.core.management import call_command
>>> from catalogue.models import *

###############################################

Prepare testing, load fixtures

###############################################


Load an initial fixture with dictionaries

>>> call_command('loaddata', 'fixtures/catalogue_dictionaries.json')
Installing json fixture 'fixtures/catalogue_dictionaries' from absolute path.
Installed ...

###############################################

Test ingestion

###############################################

>>> call_command('rapideye_harvest', license='CC-BY-SA', owner='LINFINITI', creating_software='QGIS')
>>> python manage.py rapideye_harvest -v 2 -a 'POLYGON(( 22 3, 23 3, 23 2, 22 2, 22 3))' -d 12 -y 2011 -m 03


###############################################

Test that everything was imported correctly

###############################################


###############################################

Test update reading owner from metadata

###############################################


###############################################

Test update

###############################################


###############################################

Cleanup

###############################################


>>> #os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailPath(), p.product_id + '.jpg'))
>>> #os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailPath(), p.product_id + '.wld'))



"""