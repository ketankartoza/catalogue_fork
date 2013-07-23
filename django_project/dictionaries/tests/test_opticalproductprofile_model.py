"""
SANSA-EO Catalogue - Dictionaries OpticalProductProfile - basic CRUD
unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '23/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage


from .model_factories import (
    OpticalProductProfileF, SatelliteInstrumentF, SpectralModeF,
    InstrumentTypeF
)


class TestOpticalProductProfileCRUD(TestCase):
    """
    Tests OpticalProductProfile model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_OpticalProductProfile_create(self):
        """
        Tests OpticalProductProfile model creation
        """
        myModel = OpticalProductProfileF.create()

        self.assertTrue(
            myModel.pk is not None,
            simpleMessage(
                myModel.pk, 'not None',
                message='Model PK should NOT equal None')
        )

    def test_OpticalProductProfile_delete(self):
        """
        Tests OpticalProductProfile model delete
        """
        myModel = OpticalProductProfileF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(
            myModel.pk is None, simpleMessage(
                myModel.pk, None,
                message='Model PK should equal None')
        )

    def test_OpticalProductProfile_read(self):
        """
        Tests OpticalProductProfile model read
        """

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode'
        })

        myModel = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'spectral_mode': mySpecMode
        })

        self.assertEqual(
            myModel.satellite_instrument.operator_abbreviation, 'SATIN 1')

        self.assertEqual(myModel.spectral_mode.name, 'Temp Spectral mode')

    def test_OpticalProductProfile_update(self):
        """
        Tests OpticalProductProfile model update
        """

        myModel = OpticalProductProfileF.create()

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })
        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode'
        })

        myModel.satellite_instrument = mySatInst
        myModel.spectral_mode = mySpecMode

        myModel.save()

        self.assertEqual(
            myModel.satellite_instrument.operator_abbreviation, 'SATIN 1')

        self.assertEqual(myModel.spectral_mode.name, 'Temp Spectral mode')

    def test_OpticalProductProfile_repr(self):
        """
        Tests OpticalProductProfile model repr
        """

        mySatInst = SatelliteInstrumentF.create(**{
            'operator_abbreviation': 'SATIN 1'
        })

        myInstType = InstrumentTypeF.create(**{
            'name': 'INSTYPE1'
        })

        mySpecMode = SpectralModeF.create(**{
            'name': 'Temp Spectral mode',
            'instrument_type': myInstType
        })

        myModel = OpticalProductProfileF.create(**{
            'satellite_instrument': mySatInst,
            'spectral_mode': mySpecMode
        })

        self.assertEqual(
            unicode(myModel), u'SATIN 1 -- Temp Spectral mode - INSTYPE1')
