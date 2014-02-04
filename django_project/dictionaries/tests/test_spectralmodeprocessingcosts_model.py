"""
SANSA-EO Catalogue - Dictionaries SpectralModeProcessingCosts - basic CRUD
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


from .model_factories import (
    SpectralModeProcessingCostsF, SpectralModeF, CurrencyF,
    InstrumentTypeProcessingLevelF, InstrumentTypeF, ProcessingLevelF
)


class TestSpectralModeProcessingCostsCRUD(TestCase):
    """
    Tests SpectralModeProcessingCosts model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_SpectralModeProcessingCosts_create(self):
        """
        Tests SpectralModeProcessingCosts model creation
        """
        myModel = SpectralModeProcessingCostsF.create()

        self.assertTrue(myModel.pk is not None)

    def test_SpectralModeProcessingCosts_delete(self):
        """
        Tests SpectralModeProcessingCosts model delete
        """
        myModel = SpectralModeProcessingCostsF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_SpectralModeProcessingCosts_read(self):
        """
        Tests SpectralModeProcessingCosts model read
        """

        mySpecMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })
        myForeignCur = CurrencyF.create(**{
            'name': 'SuperGold'
        })
        myInstTypeProcLevel = InstrumentTypeProcessingLevelF.create(**{
            'operator_processing_level_name': 'Level 0'
        })

        myModel = SpectralModeProcessingCostsF.create(**{
            'spectral_mode': mySpecMode,
            'instrumenttypeprocessinglevel': myInstTypeProcLevel,
            'cost_per_scene': 200.94,
            'currency': myForeignCur,
            'cost_per_scene_in_foreign': 123.12
        })

        self.assertEqual(myModel.spectral_mode.name, 'New Spectral mode')

        self.assertEqual(
            myModel.instrumenttypeprocessinglevel.operator_processing_level_name,
            'Level 0'
        )

        self.assertEqual(myModel.cost_per_scene, 200.94)

        self.assertEqual(myModel.currency.name, 'SuperGold')

        self.assertEqual(myModel.cost_per_scene_in_foreign, 123.12)

    def test_SpectralModeProcessingCosts_update(self):
        """
        Tests SpectralModeProcessingCosts model update
        """
        mySpecMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })
        myForeignCur = CurrencyF.create(**{
            'name': 'SuperGold'
        })
        myInstTypeProcLevel = InstrumentTypeProcessingLevelF.create(**{
            'operator_processing_level_name': 'Level 0'
        })

        myModel = InstrumentTypeProcessingLevelF.create()

        myModel.__dict__.update(**{
            'cost_per_scene': 200.94,
            'cost_per_scene_in_foreign': 123.12
        })

        myModel.spectral_mode = mySpecMode
        myModel.instrumenttypeprocessinglevel = myInstTypeProcLevel
        myModel.currency = myForeignCur
        myModel.save()

        self.assertEqual(myModel.spectral_mode.name, 'New Spectral mode')

        self.assertEqual(
            myModel.instrumenttypeprocessinglevel.operator_processing_level_name,
            'Level 0'
        )

        self.assertEqual(myModel.cost_per_scene, 200.94)

        self.assertEqual(myModel.currency.name, 'SuperGold')

        self.assertEqual(myModel.cost_per_scene_in_foreign, 123.12)

    def test_SpectralModeProcessingCosts_repr(self):
        """
        Tests SpectralModeProcessingCosts model repr
        """
        mySpecMode = SpectralModeF.create(**{
            'name': 'New Spectral mode'
        })

        myInstType = InstrumentTypeF.create(**{
            'name': 'IT name'
        })

        myProcLevel = ProcessingLevelF.create(**{
            'abbreviation': 'PL1'
        })

        myInstTypeProcLevel = InstrumentTypeProcessingLevelF.create(**{
            'instrument_type': myInstType,
            'processinglevel': myProcLevel
        })

        myCurrency = CurrencyF.create(**{
            'name': 'SuperGold',
            'abbreviation': 'SG'
        })

        myModel = SpectralModeProcessingCostsF.create(**{
            'spectral_mode': mySpecMode,
            'instrumenttypeprocessinglevel': myInstTypeProcLevel,
            'cost_per_scene': 200.94,
            'currency': myCurrency
        })

        self.assertEqual(
            unicode(myModel),
            u'200.94 SG (New Spectral mode - IT name - PL1)')
