"""
SANSA-EO Catalogue - Search_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '29/06/2012'
__copyright__ = 'South African National Space Agency'

from datetime import datetime
from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
# from search.models import Search

from .model_factories import SearchF


class TestSearchCRUD(TestCase):
    """
    Tests search models.
    """
    # fixtures = [
    #     # 'test_user.json',
    #     # 'test_institution.json',
    #     # 'test_license.json',
    #     # # new_dicts
    #     # 'test_radarbeam.json',
    #     # 'test_imagingmode.json',
    #     # 'test_spectralgroup.json',
    #     # 'test_spectralmode.json',
    #     # 'test_scannertype.json',
    #     # 'test_instrumenttype.json',
    #     # 'test_collection.json',
    #     # 'test_satellite.json',
    #     # 'test_satelliteinstrument.json',
    #     # 'test_radarproductprofile.json',
    #     # 'test_opticalproductprofile.json',

    #     # 'test_processinglevel.json',
    #     # 'test_searchdaterange.json',
    #     # 'test_search.json'
    # ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_Search_create(self):
        """
        Tests Search model creation
        """
        myNewData = {
            'record_count': None,
            'use_cloud_cover': False,
            'sensor_inclination_angle_end': None,
            'search_date': '2010-07-15 09:21:38',
            'satellite_id': None,
            'spectral_mode_id': None,
            'guid': '69d814b7-TEST-42b9-9530-50ae77806da9',
            'sensor_inclination_angle_start': None,
            'ip_position': None,
            'deleted': False,
            'spatial_resolution': None,
            'k_orbit_path': None,
            'band_count': None,
            'user_id': 1,
            'geometry': (
                'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 '
                    '-34.65, 17.54 -32.05))'),
            'j_frame_row': None,
            'cloud_mean': 5,
            'license_type': None
        }

        myModel = SearchF(**myNewData)
        # myModel.save()

        #check if PK exists
        self.assertTrue(
            myModel.pk is not None, simpleMessage(
                myModel.pk, 'not None',
                message='Model PK should NOT equal None')
        )

        #we need to create manyTomany field separatly
        myNewDataM2M = {
            'processing_level': [],
            'instrumenttype': [4]
        }
        #add M2M fields
        for field, vals in myNewDataM2M.iteritems():
            for value in vals:
                myModel.__getattribute__(field).add(value)

        #check if M2M models were added
        for field in myNewDataM2M:
            myRes = myModel.__getattribute__(field).count()
            myExpRes = len(myNewDataM2M.get(field))
            self.assertTrue(
                myRes == myExpRes, simpleMessage(
                    myRes, myExpRes,
                    message='Model M2M field "%s" count:' % field)
            )

    def test_Search_read(self):
        """
        Tests Search model read
        """
        myModelPK = 1
        myExpectedModelData = {
            'record_count': None,
            'use_cloud_cover': False,
            'sensor_inclination_angle_end': None,
            'search_date': datetime.strptime(
                '2010-07-15 09:21:38', '%Y-%m-%d %H:%M:%S'),
            'satellite_id': None,
            'spectral_mode_id': None,
            'guid': '69d814b7-3164-42b9-9530-50ae77806da9',
            'sensor_inclination_angle_start': None,
            'ip_position': (
                '0101000020E6100000A01A2FDD246632C0BC749318043E5040'),
            'deleted': False,
            'spatial_resolution': None,
            'k_orbit_path': None,
            'band_count': None,
            'user_id': 1,
            'geometry': (
                '0103000020E6100000010000000500000000000000408A314000000000A0'
                '0740C00000000000D6344000000000A03440C000000000004F3440000000'
                '00009741C00000000000D9314000000000805341C000000000408A314000'
                '000000A00740C0'),
            'j_frame_row': None,
            'cloud_mean': 5,
            'license_type': None
        }
        myModel = Search.objects.get(pk=myModelPK)
        #check if data is correct
        for key, val in myExpectedModelData.items():
            self.assertEqual(
                myModel.__dict__.get(key), val, simpleMessage(
                    myModel.__dict__.get(key), val,
                    message='For key "%s"' % key)
            )

        #check m2m
        myExpectedModelDataM2M = {
            'processing_level': [],
            'instrumenttype': [
                4
            ]
        }
        #add M2M fields
        for field in myExpectedModelDataM2M:
            myRes = len(myModel.__getattribute__(field).all())
            myExpRes = len(myExpectedModelDataM2M.get(field))
            self.assertEqual(
                myRes, myExpRes, simpleMessage(
                    myRes, myExpRes,
                    message='For field "%s"' % field)
            )

    def test_Search_update(self):
        """
        Tests Search model update
        """
        myModelPK = 1
        myModel = Search.objects.get(pk=myModelPK)
        myNewModelData = {
            'user_id': 1,
            'order_id': 1,
            'product_id': 1960810,
            'delivery_detail_id': None,
            'internal_order_id': None,
            'download_path': 'Some path',
            'product_ready': True
        }

        myModel.__dict__.update(myNewModelData)
        myModel.save()

        #check if updated
        for key, val in myNewModelData.items():
            self.assertEqual(
                myModel.__dict__.get(key), val, simpleMessage(
                    myModel.__dict__.get(key), val,
                    message='For key "%s"' % key)
            )

    def test_Search_delete(self):
        """
        Tests Search model delete
        """
        myModelPK = 1
        myModel = Search.objects.get(pk=myModelPK)

        myModel.delete()

        #check if deleted
        self.assertTrue(
            myModel.pk is None, simpleMessage(
                myModel.pk, None,
                message='Model PK should equal None')
        )

    def test_Search_datesAsString(self):
        """
        Tests Search model datesAsString method
        """
        myModelPKs = [1, 2, 4, 7]
        myExpResults = [
            '01-01-1901 : 31-12-2100', '01-01-2009 : 31-12-2012',
            '01-01-2000 : 31-12-2005', '01-01-1900 : 31-12-2100']

        for idx, PK in enumerate(myModelPKs):
            myModel = Search.objects.get(pk=PK)
            myRes = myModel.datesAsString()
            self.assertEqual(
                myRes, myExpResults[idx], simpleMessage(
                    myRes, myExpResults[idx],
                    message='Model PK %s datesAsString:' % PK)
            )
