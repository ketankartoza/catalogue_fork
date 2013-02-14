"""

Tests ingestion

>>>
>>> from django.core.management import call_command
>>>

###############################################

Prepare testing, load fixtures

###############################################


Load an initial fixture with

>>> call_command('loaddata', 'fixtures/catalogue.json', verbosity=0)


###############################################

Test ingestion

###############################################

Command: python manage.py terrasar_harvest -v 0 -a 'POLYGON(( 12 3, 23 3, 23 2, 12 2, 12 3))' -m 3

>>> call_command('terrasar_harvest', license='CC-BY-SA', owner='LINFINITI', creating_software='QGIS', area='POLYGON(( 12 3, 23 3, 23 2, 12 2, 12 3))', maxproducts=10, quality='zzzzzzz', verbosity=0)


###############################################

Test that everything was imported correctly


###############################################

Tests import was complete

>>> RadarProduct.objects.filter(product_id__startswith='TSX').count()
10

Test a product in the middle of the import

>>> p=RadarProduct.objects.filter(product_id__startswith='TSX').order_by('pk')[6]
>>> p.radiometric_resolution
16
>>> p.geometric_resolution
18.10...
>>> p.product_acquisition_start
datetime.datetime(2011, 2, 28, 17, 13, 15)
>>> p.band_count
5
>>> int(p.incidence_angle)
27
>>> p.polarising_mode
u'S'
>>> p.orbit_direction
u'A'
>>> p.imaging_mode
u'ScanSAR (SC)'
>>> p.owner
<Institution: LINFINITI>
>>> p.quality
<Quality: zzzzzzz>
>>> p.spatial_coverage.wkt
'POLYGON ((...'
>>> p.license
<License: CC-BY-SA>
>>> p.creating_software
<CreatingSoftware: QGIS>

Test the sensors chain

>>> p.acquisition_mode.abbreviation
u'HH'
>>> p.acquisition_mode.sensor_type.abbreviation
u'SCS'
>>> p.acquisition_mode.sensor_type.mission_sensor.abbreviation
u'SAR'
>>> p.acquisition_mode.sensor_type.mission_sensor.mission.abbreviation
u'TSX'


###############################################

Cleanup

###############################################


"""
