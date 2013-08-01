"""
SANSA-EO Catalogue - TaskingRequest_model - implements basic CRUD unittests

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
__date__ = '01/08/2013'
__copyright__ = 'South African National Space Agency'

from datetime import datetime

from django.test import TestCase

from .model_factories import TaskingRequestF


class TaskingRequestCRUD_Test(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_TaskingRequest_create(self):
        """
        Tests TaskingRequest model creation
        """
        myModel = TaskingRequestF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_TaskingRequest_delete(self):
        """
        Tests TaskingRequest model delete
        """
        myModel = TaskingRequestF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_TaskingRequest_read(self):
        """
        Tests TaskingRequest model read
        """

        myModel = TaskingRequestF.create(**{
            'target_date': datetime(2008, 1, 1)
        })

        self.assertEqual(myModel.target_date, datetime(2008, 1, 1))

    def test_TaskingRequest_update(self):
        """
        Tests TaskingRequest model update
        """
        myModel = TaskingRequestF.create()

        myModel.__dict__.update({
            'target_date': datetime(2008, 1, 1)
        })
        myModel.save()

        self.assertEqual(myModel.target_date, datetime(2008, 1, 1))

    def test_TaskingRequest_repr(self):
        """
        Tests TaskingRequest model repr
        """
        myModel = TaskingRequestF.create(**{
            'id': 1
        })

        self.assertEqual(unicode(myModel), '1')
