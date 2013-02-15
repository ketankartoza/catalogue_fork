"""

Tests ingestion

>>> import os
>>> from django.conf import settings
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

Command: python manage.py modis_harvest -v 0 -m 3

>>> call_command('modis_harvest', verbosity=0, maxproducts=3, rcfileskip=True)


###############################################

Test that everything was imported correctly

###############################################

Tests import was complete

>>> OpticalProduct.objects.filter(product_id__startswith='MYD').count()
3
>>> OpticalProduct.objects.filter(product_id__startswith='MYD')
[<OpticalProduct: MYD_MYD_MOD_MOD-_0015_10_00-5_01_000218_000000_1B--_ORBIT->, <OpticalProduct: MYD_MYD_MOD_MOD-_0015_58_0-15_02_000218_000000_1B--_ORBIT->, <OpticalProduct: MYD_MYD_MOD_MOD-_0016_63_0-25_03_000218_000000_1B--_ORBIT->]

Test a product in the middle of the import

>>> p=OpticalProduct.objects.get(product_id='MYD_MYD_MOD_MOD-_0015_58_0-15_02_000218_000000_1B--_ORBIT-')
>>> p.radiometric_resolution
8
>>> p.geometric_resolution
500
>>> p.product_acquisition_start
datetime.datetime(2000, 2, 18, 0, 0)
>>> p.band_count
4
>>> p.owner
<Institution: MODIS>
>>> p.quality
<Quality: Unknown>
>>> p.spatial_coverage.wkt
'POLYGON ((10.5987670000000005 -20.0045339999999996, 10.1164880000000004 -9.9634640000000001, 20.3182229999999997 -9.9588509999999992, 21.2909979999999983 -19.9997730000000011, 10.5987670000000005 -20.0045339999999996))'
>>> p.license
<License: SAC Free License>
>>> p.creating_software
<CreatingSoftware: HDFEOS_V2.9>
>>> p.original_product_id
u'MCD43A2.A2000049.h19v10.005.2006269121249.hdf'
>>> p.local_storage_path
u'MYD/1B/2000/2/18/MYD_MYD_MOD_MOD-_0015_58_0-15_02_000218_000000_1B--_ORBIT-.hdf.bz2'

>>> p.product_id + '.hdf.bz2'
u'MYD_MYD_MOD_MOD-_0015_58_0-15_02_000218_000000_1B--_ORBIT-.hdf.bz2'

Test world file

>>> open(os.path.join(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.wld'))).readlines()
['0.00435290965402\n', '1.95301945208e-06\n', '0.000303136078562\n', '-0.0041837482381\n', '9.99619224734\n', '-9.96559224097\n']


Check that thumbnail, original imagery and world file are there...

>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.jpg'))
True
>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.wld'))
True
>>> os.path.isfile(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.hdf.bz2'))
True


###############################################

Cleanup

###############################################


>>> for p in OpticalProduct.objects.filter(product_id__icontains='RE2'):
...    os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.jpg'))
...    os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailDirectory(), p.product_id + '.wld'))
...    os.remove(os.path.join(settings.IMAGERY_ROOT, p.productDirectory(), p.product_id + '.hdf.bz2'))


"""
