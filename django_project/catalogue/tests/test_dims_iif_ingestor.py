# -*- coding: utf-8 -*-
"""
SANSA-EO Catalogue - DIMS IIF ingestor tests

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
__date__ = '3/09/2013'
__copyright__ = 'South African National Space Agency'

import os
from django.test import TestCase
import unittest
import factory
from django.core.management import call_command
from catalogue.models import (
    GenericProduct)
from catalogue.ingestors import dims_iif
from .model_factories import ProjectionF, QualityF
from dictionaries.tests.model_factories import (
    SatelliteF,
    SatelliteInstrumentF,
    SpectralModeF,
    InstrumentTypeF,
    SatelliteInstrumentGroupF,
    OpticalProductProfileF,
)
DATA_DIR_PATH = os.path.join(
    os.path.dirname(__file__),
    'sample_files/DIMS')


class DIMSIIFIngestorTest(TestCase):
    """
    Tests IIF Ingestor
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def testImportUsingManagementCommand(self):
        """Test that we can ingest spot using the management command"""
        call_command('dims_iif_harvest',
                     verbosity=2,
                     source_dir=DATA_DIR_PATH)

    def testImportDirectly(self):
        """Test that we can ingest DIMS IIF using the ingestor function"""

        #
        # Test with a full load of data
        #
        QualityF.create(name='Unknown')
        ProjectionF.create(epsg_code=32734)
        satellite = SatelliteF.create(
            abbreviation='L8',
            operator_abbreviation='LS-8')
        instrument_type = InstrumentTypeF.create(
            abbreviation='OLI',
            operator_abbreviation='OLI')
        group = SatelliteInstrumentGroupF.create(
            satellite=satellite,
            instrument_type=instrument_type
        )

        instrument = SatelliteInstrumentF.create(
            operator_abbreviation='L8-OLI',
            satellite_instrument_group=group
        )

        mySpecMode1 = SpectralModeF.create(**{
            'abbreviation': 'MS',
            'instrument_type': instrument_type
        })
        mySpecMode2 = SpectralModeF.create(**{
            'abbreviation': 'PAN',
            'instrument_type': instrument_type
        })
        mySpecMode3 = SpectralModeF.create(**{
            'abbreviation': 'THM',
            'instrument_type': instrument_type
        })
        myModel = OpticalProductProfileF.create(**{
            'satellite_instrument': instrument,
            'spectral_mode': mySpecMode1
        })
        dims_iif.ingest(
            theSourceDir=DATA_DIR_PATH,
            theVerbosityLevel=2)
        myProducts = GenericProduct.objects.filter(
            original_product_id__contains='LC8')
        myList = []
        myFormattedList = ''
        for myProduct in myProducts:
            myList.append(myProduct.product_id)
            myFormattedList += myProduct.product_id + '\n'

        myExpectedProductId = 'LC81730832013162JSA00'
        myMessage = 'Expected:\n%s\nTo be in:\n%s\n' % (
            myExpectedProductId,
            myFormattedList)
        assert myExpectedProductId in myList, myMessage

        # Reingest and make sure that overridden owner sticks
        # Above ran in test mode so image was

        dims_iif.ingest(
            theSourceDir=DATA_DIR_PATH,
            theVerbosityLevel=2)

        myProduct = GenericProduct.objects.get(
            original_product_id=myExpectedProductId)

        assert 'updating' in myProduct.ingestion_log


if __name__ == '__main__':
    unittest.main()
