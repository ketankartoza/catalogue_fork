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

from django.core.management import call_command
from catalogue.models import (
    GenericProduct)
from catalogue.ingestors import dims_iif
from .model_factories import QualityF
from dictionaries.tests.model_factories import (
    SatelliteF,
    SatelliteInstrumentF,
    SpectralModeF,
    InstrumentTypeF,
    SatelliteInstrumentGroupF,
    OpticalProductProfileF,
    ProjectionF
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

        spectral_mode1 = SpectralModeF.create(**{
            'abbreviation': 'MS',
            'instrument_type': instrument_type
        })
        spectral_mode2 = SpectralModeF.create(**{
            'abbreviation': 'PAN',
            'instrument_type': instrument_type
        })
        spectral_mode3 = SpectralModeF.create(**{
            'abbreviation': 'THM',
            'instrument_type': instrument_type
        })
        profile = OpticalProductProfileF.create(**{
            'satellite_instrument': instrument,
            'spectral_mode': spectral_mode1
        })

    # noinspection PyMethodMayBeStatic
    def test_import_using_management_command(self):
        """Test that we can ingest spot using the management command"""
        call_command('dims_iif_harvest',
                     verbosity=2,
                     source_dir=DATA_DIR_PATH,
                     theHaltOnErrorFlag=False)

    # noinspection PyMethodMayBeStatic
    def test_direct_import(self):
        """Test that we can ingest DIMS IIF using the ingestor function"""

        #
        # Test with a full load of data
        #
        dims_iif.ingest(
            source_path=DATA_DIR_PATH,
            verbosity_level=2,
            halt_on_error_flag=False)
        products = GenericProduct.objects.filter(
            original_product_id__contains='LC8')
        product_list = []
        formatted_list = ''
        for product in products:
            product_list.append(product.product_id)
            formatted_list += product.product_id + '\n'

        existing_product_id = 'LC81730832013162JSA00'
        message = 'Expected:\n%s\nTo be in:\n%s\n' % (
            existing_product_id,
            formatted_list)
        assert existing_product_id in product_list, message

        # Reingest and make sure that overridden owner sticks
        # Above ran in test mode so image was

        dims_iif.ingest(
            source_path=DATA_DIR_PATH,
            verbosity_level=2,
            halt_on_error_flag=False)

        product = GenericProduct.objects.get(
            original_product_id=existing_product_id)

        assert 'updating' in product.ingestion_log


if __name__ == '__main__':
    unittest.main()
