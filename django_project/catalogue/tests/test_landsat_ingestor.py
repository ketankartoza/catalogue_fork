# -*- coding: utf-8 -*-
"""
SANSA-EO Catalogue - Landsat ingestor tests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkley@sansa.org.za'
__version__ = '0.1'
__date__ = '12/07/2012'
__copyright__ = 'South African National Space Agency'

import os
from django.test import TestCase
import unittest
from django.core.management import call_command
from catalogue.models import (
    GenericProduct)
from catalogue.ingestors import landsat

DATA_DIR_PATH = os.path.join(
    os.path.dirname(__file__),
    'sample_files/landsat')


class LandsatIngestorTest(TestCase):
    """
    Tests Landsat Ingestor
    """

    fixtures = [
        'test_user.json',
        'test_processinglevel.json',
        'test_institution.json',
        'test_license.json',
        'test_projection.json',
        'test_quality.json',
        'test_sansauserprofile.json',
        'test_creatingsoftware.json',
        # new_dicts
        'test_spectralgroup.json',
        'test_spectralmode.json',
        'test_scannertype.json',
        'test_instrumenttype.json',
        'test_collection.json',
        'test_satellite.json',
        'test_satelliteinstrument.json',
        'test_opticalproductprofile.json',
        'test_radarproductprofile.json',
        # Products
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json',
        'test_datum.json',
        'test_deliverymethod.json',
        'test_fileformat.json',
        'test_resamplingmethod.json',
        'test_imagingmode.json',
        'test_radarbeam.json']

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def testImportUsingManagementCommand(self):
        """Test that we can ingest spot using the management command"""
        call_command('landsat_harvest',
                     verbosity=2,
                     source_dir=DATA_DIR_PATH)

    def testImportDirectly(self):
        """Test that we can ingest landsat using the ingestor function"""

        #
        # Test with a full load of data
        #
        landsat.ingest(
            theSourceDir=DATA_DIR_PATH,
            theVerbosityLevel=1)
        myProducts = GenericProduct.objects.filter(product_id__contains='L5')
        myList = []
        myFormattedList = ''
        for myProduct in myProducts:
            myList.append(myProduct.product_id)
            myFormattedList += myProduct.product_id + '\n'

        myExpectedProductId = 'Foooooo'
        myMessage = 'Expected:\n%s\nTo be in:\n%s\n' % (
            myExpectedProductId,
            myFormattedList)
        assert myExpectedProductId in myList, myMessage

        # Reingesst and make sure that overridden owner sticks

        landsat.ingest(
            theSourceDir=DATA_DIR_PATH,
            theOwner='Foobar')
        myProduct = GenericProduct.objects.get(
            product_id=myExpectedProductId)
        assert myProduct.owner.name == 'Foobar'


if __name__ == '__main__':
    unittest.main()
