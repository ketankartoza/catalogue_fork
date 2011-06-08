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

Command: python manage.py rapideye_harvest -v 0 -a 'POLYGON(( 22 3, 23 3, 23 2, 22 2, 22 3))' -d 12 -y 2011 -m 03

>>> call_command('rapideye_harvest', license='CC-BY-SA', owner='LINFINITI', creating_software='QGIS', area='POLYGON(( 22 3, 23 3, 23 2, 22 2, 22 3))', day='12', month='03', year='2011', quality='zzzzzzz', verbosity=0)


###############################################

Test that everything was imported correctly

###############################################

Tests import was complete

>>> OpticalProduct.objects.filter(acquisition_mode__sensor_type__mission_sensor__mission__abbreviation__startswith='RE').count()
10

Test a product in the middle of the import

>>> p=OpticalProduct.objects.get(product_id='RE2_REI_VRN_PB--_0022_83_0002_50_110312_090000_1B--_ORBIT-')
>>> p.radiometric_resolution
16
>>> int(p.geometric_resolution)
5
>>> p.product_acquisition_start
datetime.datetime(2011, 3, 12, 9, 0)


>>> int(p.solar_azimuth_angle)
118
>>> p.band_count
5
>>> int(p.solar_zenith_angle)
12
>>> p.owner
<Institution: LINFINITI>
>>> p.quality
<Quality: zzzzzzz>
>>> p.spatial_coverage.wkt
'POLYGON ((22.7269649999999999 2.6044179999999999, 22.9427570000000003 2.6041029999999998, 22.9424390000000002 2.3870969999999998, 22.7266820000000003 2.3873859999999998, 22.7269649999999999 2.6044179999999999))'
>>> p.license
<License: CC-BY-SA>
>>> p.cloud_cover
50
>>> p.creating_software
<CreatingSoftware: QGIS>
>>> int(p.sensor_viewing_angle)
-6
>>> int(p.sensor_inclination_angle)
3
>>> p.original_product_id
u'https://delivery.rapideye.de/catalogue/browse_images/2011/03/12/5746735/3440223_2011-03-12_5746735_5746745_browse.tiff'

Check that thumbnail and world file are there...

>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.jpg'))
True
>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.wld'))
True


###############################################

Cleanup

###############################################


>>> for p in OpticalProduct.objects.filter(product_id__icontains='RE2'):
...    os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.jpg'))
...    os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.wld'))


"""