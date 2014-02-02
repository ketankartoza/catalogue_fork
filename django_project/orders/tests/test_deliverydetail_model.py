"""
SANSA-EO Catalogue - DeliveryDetail_model - implements basic CRUD unittests

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
__date__ = '08/08/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import DeliveryDetailF


class DeliveryDetailCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_DeliveryDetail_create(self):
        """
        Tests DeliveryDetail model creation
        """

        myModel = DeliveryDetailF.create()
        self.assertTrue(myModel.pk is not None)

    def test_DeliveryDetail_delete(self):
        """
        Tests DeliveryDetail model delete
        """
        myModel = DeliveryDetailF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_DeliveryDetail_read(self):
        """
        Tests DeliveryDetail model read
        """

        myModel = DeliveryDetailF.create(**{
            'geometry': (
                'POLYGON ((17.54003 -32.05957, 20.83593 -32.41113, 20.30859 '
                '-35.17968, 17.84765 -34.65234, 17.54003 -32.05957))')
        })

        self.assertEqual(
            myModel.geometry.hex,
            ('01030000000100000005000000E0DBF4673F8A31404FE960FD9F0740C0CBBE2B'
            '82FFD53440C63368E89F3440C065DF15C1FF4E344065DF15C1FF9641C05474249'
            '7FFD83140B3EF8AE07F5341C0E0DBF4673F8A31404FE960FD9F0740C0')
        )

    def test_DeliveryDetail_update(self):
        """
        Tests DeliveryDetail model update
        """
        myModel = DeliveryDetailF.create()

        myModel.__dict__.update({
            'geometry': (
                'POLYGON ((17.54003 -32.05957, 20.83593 -32.41113, 20.30859 '
                '-35.17968, 17.84765 -34.65234, 17.54003 -32.05957))')
        })
        myModel.save()

        self.assertEqual(
            myModel.geometry.hex,
            ('01030000000100000005000000E0DBF4673F8A31404FE960FD9F0740C0CBBE2B'
            '82FFD53440C63368E89F3440C065DF15C1FF4E344065DF15C1FF9641C05474249'
            '7FFD83140B3EF8AE07F5341C0E0DBF4673F8A31404FE960FD9F0740C0')
        )