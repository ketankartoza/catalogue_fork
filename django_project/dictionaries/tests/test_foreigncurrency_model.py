"""
SANSA-EO Catalogue - Dictionaries ForeignCurrency - basic CRUD
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

from .model_factories import ForeignCurrencyF


class TestForeignCurrencyCRUD(TestCase):
    """
    Tests ForeignCurrency model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_ForeignCurrency_create(self):
        """
        Tests ForeignCurrency model creation
        """
        myModel = ForeignCurrencyF.create()

        self.assertTrue(myModel.pk is not None)

    def test_ForeignCurrency_delete(self):
        """
        Tests ForeignCurrency model delete
        """
        myModel = ForeignCurrencyF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_ForeignCurrency_read(self):
        """
        Tests ForeignCurrency model read
        """

        myModel = ForeignCurrencyF.create(**{
            'abbreviation': 'SG',
            'name': 'SuperGold',
            'conversion_rate': 0.01
        })

        self.assertEqual(myModel.name, 'SuperGold')

        self.assertEqual(myModel.conversion_rate, 0.01)

        self.assertEqual(myModel.abbreviation, 'SG')

    def test_ForeignCurrency_update(self):
        """
        Tests ForeignCurrency model update
        """

        myModel = ForeignCurrencyF.create()

        myModel.__dict__.update(**{
            'abbreviation': 'SG',
            'name': 'SuperGold',
            'conversion_rate': 0.01
        })

        myModel.save()

        self.assertEqual(myModel.name, 'SuperGold')

        self.assertEqual(myModel.conversion_rate, 0.01)

        self.assertEqual(myModel.abbreviation, 'SG')

    def test_ForeignCurrency_repr(self):
        """
        Tests ForeignCurrency model repr
        """

        myModel = ForeignCurrencyF.create(**{
            'name': 'SuperGold'
        })

        self.assertEqual(unicode(myModel), u'SuperGold')
