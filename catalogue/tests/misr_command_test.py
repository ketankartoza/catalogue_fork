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

>>> call_command('misr_ingest', verbosity=0, maxproducts=1, rcfileskip=True)


###############################################

Test that everything was imported correctly

###############################################

>>> OpticalProduct.objects.filter(product_id__startswith='TER_MIS').count()
1
>>> OpticalProduct.objects.filter(product_id__startswith='TER_MIS')
[<OpticalProduct: TER_MIS_VNI_LM--_0176_00_1063_00_000229_090802_1B2-_ORBIT->]

Test a product (just one by now)

>>> p=OpticalProduct.objects.get(product_id='TER_MIS_VNI_LM--_0176_00_1063_00_000229_090802_1B2-_ORBIT-')
>>> p.radiometric_resolution
16
>>> p.geometric_resolution
275
>>> p.product_acquisition_start
datetime.datetime(2000, 2, 29, 9, 8, 2)
>>> p.band_count
5
>>> p.row
1063
>>> p.path
176
>>> p.owner
<Institution: MISR>
>>> p.quality
<Quality: Unknown>
>>> p.spatial_coverage.wkt
'POLYGON ((19...'
>>> p.license
<License: SAC Commercial License>
>>> p.creating_software
<CreatingSoftware: Unknown>
>>> p.original_product_id
u'MISR_AM1_GRP_ELLIPSOID_LM_P176_O001063_AN_SITE_MONGU_F03_0024.hdf'
>>> p.local_storage_path
u'TER/1B2/2000/2/29/TER_MIS_VNI_LM--_0176_00_1063_00_000229_090802_1B2-_ORBIT-.tar.bz2'

>>> p.product_id + '.tar.bz2'
u'TER_MIS_VNI_LM--_0176_00_1063_00_000229_090802_1B2-_ORBIT-.tar.bz2'

Test world file

>>> open(os.path.join(os.path.join(settings.THUMBS_ROOT, p.thumbnailPath(), p.product_id + '.wld'))).readlines()
['0.0129427500\n', '0.0000000000\n', '0.0000000000\n', '-0.0126720000\n', '18.8377963750\n', '-12.3537360000\n']


Check that thumbnail, original imagery and world file are there...

>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailPath(), p.product_id + '.jpg'))
True
>>> os.path.isfile(os.path.join(settings.THUMBS_ROOT, p.thumbnailPath(), p.product_id + '.wld'))
True
>>> os.path.isfile(os.path.join(settings.IMAGERY_ROOT, p.local_storage_path))
True



###############################################

Cleanup

###############################################


>>> for p in OpticalProduct.objects.filter(product_id__startswith='TER_MIS'):
...    os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailPath(), p.product_id + '.jpg'))
...    os.remove(os.path.join(settings.THUMBS_ROOT, p.thumbnailPath(), p.product_id + '.wld'))
...    os.remove(os.path.join(settings.IMAGERY_ROOT, p.local_storage_path))


"""