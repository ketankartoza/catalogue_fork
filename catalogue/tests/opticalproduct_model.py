"""
SANSA-EO Catalogue - opticalproduct_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.2'
__date__ = '11/10/2012'
__copyright__ = 'South African National Space Agency'

import os
import shutil
import logging
import settings
from django.test import TestCase
from django.contrib.gis.geos import GEOSGeometry
from catalogue.tests.test_utils import simpleMessage
from catalogue.models import (OpticalProduct,
                             Projection,
                             AcquisitionMode,
                             ProcessingLevel,
                             Quality,
                             CreatingSoftware,
                             Institution,
                             License,
                             GenericImageryProduct,
                             GenericSensorProduct,
                             GenericProduct)
from datetime import datetime


class OpticalProductCRUD_Test(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_user.json',
        'test_license.json',
        'test_creatingsoftware.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_quality.json',
        'test_projection.json',
        'test_institution.json',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        #'test_radarproduct.json'
    ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_OpticalProduct_create(self):
        """
        Tests OpticalProduct model creation

        As this is sub classed model, we need to include 'parent' model
        attributes. Django will handle parent model creation automatically
        """
        myNewData = {
            # we need to include 'parent' model attributes
            # without it parent models will no be created
            'product_date': '2100-01-01 12:00:00',
            'spatial_coverage': (
                'POLYGON ((21.3566000000000145 -27.2013999999999783, 21.495500'
                '0000000496 -26.6752999999999929, 22.0914000000000215 -26.7661'
                '999999999978, 21.9554000000000542 -27.2926999999999964, 21.35'
                '66000000000145 -27.2013999999999783))'),
            'projection_id': 89,
            'license_id': 1,
            'original_product_id': '11204048606190846322X',
            'local_storage_path': None,
            'creating_software_id': 1,
            'remote_thumbnail_url': '',
            'product_revision': None,
            'owner_id': 1,
            'metadata': '',
            'quality_id': 1,
            'processing_level_id': 16,
            'product_id': (
                'S1-_HRV_X--_S1C2_0120_00_0404_00_000101_084632_1B--_ORBIT-'),
            'radiometric_resolution': 16,
            'spatial_resolution_y': 1.0,
            'spatial_resolution_x': 1.0,
            'spatial_resolution': 1.0,
            'band_count': 3,
            'product_acquisition_end': None,
            'acquisition_mode_id': 87,
            'path_offset': 0,
            'orbit_number': None,
            'radiometric_signal_to_noise_ratio': None,
            'geometric_accuracy_mean': None,
            'spectral_accuracy': None,
            'geometric_accuracy_2sigma': None,
            'radiometric_percentage_error': None,
            'row_offset': 0,
            'online_storage_medium_id': None,
            'geometric_accuracy_1sigma': None,
            'offline_storage_medium_id': None,
            'path': 120,
            'product_acquisition_start': '2100-01-01 12:05:00',
            'row': 404,
            #specific model attributes
            'solar_azimuth_angle': 0.0,
            'gain_change_per_channel': None,
            'gain_value_per_channel': None,
            'cloud_cover': 5,
            'bias_per_channel': None,
            'solar_zenith_angle': 0.0,
            'sensor_viewing_angle': 2.0,
            'sensor_inclination_angle': 2.21492,
            'gain_name': None,
            'earth_sun_distance': None
        }
        myModel = OpticalProduct(**myNewData)
        myModel.save()
        #check if PK exists
        self.assertTrue(
            myModel.pk is not None,
            simpleMessage(
                myModel.pk, 'not None',
                message='Model PK should NOT equal None'))

    def test_OpticalProduct_read(self):
        """
        Tests OpticalProduct model read
        """
        myModelPK = 1934163
        myExpectedModelData = {
            'solar_azimuth_angle': 0.0,
            'gain_change_per_channel': None,
            'gain_value_per_channel': None,
            'cloud_cover': 5,
            'bias_per_channel': None,
            'solar_zenith_angle': 0.0,
            'sensor_viewing_angle': 2.0,
            'sensor_inclination_angle': 2.21492,
            'gain_name': None,
            'earth_sun_distance': None
        }
        myModel = OpticalProduct.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(
                myModel.__dict__.get(key), val,
                simpleMessage(
                    myModel.__dict__.get(key), val,
                    message='For key "%s"' % key))

    def test_OpticalProduct_update(self):
        """
        Tests OpticalProduct model update
        """
        myModelPK = 1934163
        myModel = OpticalProduct.objects.get(pk=myModelPK)
        myNewModelData = {
            'product_acquisition_end': None,
            'acquisition_mode_id': 87,
            'path_offset': 0,
            'orbit_number': None,
            'radiometric_signal_to_noise_ratio': None,
            'geometric_accuracy_mean': None,
            'spectral_accuracy': None,
            'geometric_accuracy_2sigma': None,
            'radiometric_percentage_error': None,
            'row_offset': 0,
            'online_storage_medium_id': None,
            'geometric_accuracy_1sigma': None,
            'offline_storage_medium_id': None,
            'path': 120,
            'product_acquisition_start': '2100-01-01 12:05:00',
            'row': 404
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            myRes = myModel.__dict__.get(key)
            self.assertEqual(
                myRes, val,
                simpleMessage(myRes, val, message='For key "%s"' % key))

    def Xtest_OpticalProduct_delete(self):
        """
        Tests OpticalProduct model delete

        This test FAILS because current application doesn't support
        cascade delete on inherited models - Story #227
        """
        myModelPK = 1934163
        myModel = OpticalProduct.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(
            myModel.pk is None,
            simpleMessage(
                myModel.pk, None, message='Model PK should equal None'))

    def test_OpticalProduct_getMetadataDict(self):
        """
        Tests OpticalProduct model getMetadataDict method
        """
        myModelPKs = [1934163, 1001218]
        myExpResults = [{
            'product_date': '1986-06-19T08:46:32',
            'institution_address': u'Hartebeeshoek',
            'institution_region': '', 'image_quality_code': u'Unknown',
            'vertical_cs': u'ORBIT', 'processing_level_code': u'3Ba',
            'cloud_cover_percentage': 5,
            'file_identifier': u'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_08463'
            '2_1B--_ORBIT-',
            'spatial_coverage': '21.3566,-27.2014 21.4955,-26.6753 22.0914,-26'
            '.7662 21.9554,-27.2927 21.3566,-27.2014',
            'bbox_east': 22.09140000000002, 'md_abstract': '',
            'md_product_date': '1986-06-19T08:46:32',
            'institution_city': u'Gauteng', 'bbox_north': -26.675299999999993,
            'institution_name': u'Satellite Applications Centre',
            'institution_country': u'South Africa',
            'bbox_west': 21.356600000000014, 'institution_postcode': u'0000',
            'md_data_identification': u'HRV-1:Camera 2',
            'bbox_south': -27.292699999999996
        }, {
            'product_date': '1992-07-03T08:29:48',
            'institution_address': u'Hartebeeshoek',
            'institution_region': '', 'image_quality_code': u'Unknown',
            'vertical_cs': u'UTM35S', 'processing_level_code': u'2A',
            'cloud_cover_percentage': -1,
            'file_identifier': u'S1-_Pan_P--_CAM2_0126_00_0387_00_920703_08294'
            '8_L2A-_UTM35S',
            'spatial_coverage': '26.447275,-18.739992 27.00868,-18.826267 27.1'
            '34314,-18.296593 26.574713,-18.210571 26.447275,-18.739992',
            'bbox_east': 27.134314, 'md_abstract': '',
            'md_product_date': '1992-07-03T08:29:48',
            'institution_city': u'Gauteng', 'bbox_north': -18.210571,
            'institution_name': u'Satellite Applications Centre',
            'institution_country': u'South Africa', 'bbox_west': 26.447275,
            'institution_postcode': u'0000',
            'md_data_identification': u'HRV-3:Camera 1',
            'bbox_south': -18.826267}]

        for idx, PK in enumerate(myModelPKs):
            myModel = OpticalProduct.objects.get(pk=PK)
            myRes = myModel.getMetadataDict()
            self.assertEqual(
                myRes, myExpResults[idx],
                simpleMessage(
                    myRes, myExpResults[idx],
                    message='Model PK %s getMetadataDict:' % PK))

    def test_OpticalProduct_thumbnailDirectory(self):
        """
        Tests OpticalProduct model thumbnailDirectory method
        """
        myModelPKs = [1934163, 1001218]
        myExpResults = ['S1/1986/6/19', 'S3/1992/7/3']

        for idx, PK in enumerate(myModelPKs):
            myModel = OpticalProduct.objects.get(pk=PK)
            myRes = myModel.thumbnailDirectory()
            self.assertEqual(
                myRes, myExpResults[idx],
                simpleMessage(
                    myRes, myExpResults[idx],
                    message='Model PK %s thumbnailDirectory:' % PK))

    def test_OpticalProduct_productDirectory(self):
        """
        Tests OpticalProduct model productDirectory method
        """
        myModelPKs = [1934163, 1001218]
        myExpResults = ['S1/3Ba/1986/6/19', 'S3/2A/1992/7/3']

        for idx, PK in enumerate(myModelPKs):
            myModel = OpticalProduct.objects.get(pk=PK)
            myRes = myModel.productDirectory()
            self.assertEqual(
                myRes, myExpResults[idx],
                simpleMessage(
                    myRes, myExpResults[idx],
                    message='Model PK %s productDirectory:' % PK))

    def test_ProductIdChange(self):
        """Check product id change moves assets and sets correct product data.
        """
        # First prepare our test images
        myDir = os.path.join(os.path.dirname(__file__),
                             'sample_files',
                             'test_thumbnails',
                             'L5')

        myThumbOutputPath = settings.THUMBS_ROOT
        # Create the thumbnails destination dir if it does not exist.
        if not os.path.isdir(myThumbOutputPath):
            try:
                os.makedirs(myThumbOutputPath)
            except OSError:
                logging.debug(
                    'Failed to make output directory (%s) ...quitting' % (
                        myThumbOutputPath,))
                return 'False'

        shutil.copytree(myDir, os.path.join(myThumbOutputPath, 'L5'))

        myId = 'L5-_TM-_HRF_BPSM_0176_00_0064_00_050101_081933_L2A-_UTM34S'
        OpticalProduct.objects.filter(product_id=myId).delete()
        GenericSensorProduct.objects.filter(product_id=myId).delete()
        GenericImageryProduct.objects.filter(product_id=myId).delete()
        GenericProduct.objects.filter(product_id=myId).delete()

        myProduct = OpticalProduct()

        myProjection = Projection.objects.get(epsg_code='32734')
        myProduct.projection = myProjection

        myProcessingLevel = ProcessingLevel.objects.get(abbreviation='2A')
        myProduct.processing_level = myProcessingLevel

        myMode = AcquisitionMode.objects.get(id=80)
        myProduct.acquisition_mode = myMode

        myProduct.product_acquisition_start = datetime(
            2007, 01, 01, 8, 19, 33, 0)

        myProduct.path = 176
        myProduct.row = 64

        myProduct.path_offset = 0
        myProduct.row_offset = 0

        myOwner = Institution.objects.get(id=1)
        myProduct.owner = myOwner

        myLicense = License.objects.get(id=1)
        myProduct.license = myLicense

        myQuality = Quality.objects.get(id=1)
        myProduct.quality = myQuality

        myCreatingSoftware = CreatingSoftware.objects.get(id=1)
        myProduct.creating_software = myCreatingSoftware

        mySpatialCoverage = GEOSGeometry(
            'SRID=4326;POLYGON((0.0 0.0, 1.0 0.0, 1.0 1.0, 0.0 1.0, 0.0 0.0))')

        myProduct.spatial_coverage = mySpatialCoverage.ewkt

        myProduct.radiometric_resolution = 8


        myProduct.setSacProductId(True)
        myProduct.save()
        assert myProduct.product_id == (
            'L5-_TM-_HRF_BPSM_0176_00_0064_00_050101_081933_L2A-_UTM34S')
