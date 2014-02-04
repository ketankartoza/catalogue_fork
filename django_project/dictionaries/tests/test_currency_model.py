"""
SANSA-EO Catalogue - Dictionaries Currency - basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
    Agency (SANSA) and may not be redistributed without expresse permission.
    This program may include code which is the intellectual property of
    Linfiniti Consulting CC. Linfiniti grants SANSA perpetual,
    non-transferrable license to use any code contained herein which is the
    intellectual property of Linfiniti Consulting CC.
"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.2'
__date__ = '04/02/2014'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import CurrencyF


class TestCurrencyCRUD(TestCase):
    """
    Tests Currency model
    """

    def setUp(self):
        """
        Sets up before each test
        """

    def test_Currency_create(self):
        """
        Tests Currency model creation
        """
        myModel = CurrencyF.create()

        self.assertTrue(myModel.pk is not None)

    def test_Currency_delete(self):
        """
        Tests Currency model delete
        """
        myModel = CurrencyF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_Currency_read(self):
        """
        Tests Currency model read
        """

        myModel = CurrencyF.create(**{
            'abbreviation': 'SG',
            'name': 'SuperGold',
        })

        self.assertEqual(myModel.name, 'SuperGold')

        self.assertEqual(myModel.abbreviation, 'SG')

    def test_Currency_update(self):
        """
        Tests Currency model update
        """

        myModel = CurrencyF.create()

        myModel.__dict__.update(**{
            'abbreviation': 'SG',
            'name': 'SuperGold'
        })

        myModel.save()

        self.assertEqual(myModel.name, 'SuperGold')

        self.assertEqual(myModel.abbreviation, 'SG')

    def test_Currency_repr(self):
        """
        Tests Currency model repr
        """

        myModel = CurrencyF.create(**{
            'name': 'SuperGold'
        })

        self.assertEqual(unicode(myModel), u'SuperGold')
