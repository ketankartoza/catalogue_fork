"""
SANSA-EO Catalogue - creatingSoftware_model - implements basic CRUD unittests

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
__date__ = '31/07/2013'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase

from .model_factories import CreatingSoftwareF


class Test_CreatingSoftwareCRUD(TestCase):
    """
    Tests models.
    """

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_creatingSoftware_create(self):
        """
        Tests CreatingSoftware model creation
        """

        myModel = CreatingSoftwareF.create()
        #check if PK exists
        self.assertTrue(myModel.pk is not None)

    def test_creatingSoftware_delete(self):
        """
        Tests CreatingSoftware model delete
        """
        myModel = CreatingSoftwareF.create()

        myModel.delete()

        #check if deleted
        self.assertTrue(myModel.pk is None)

    def test_creatingSoftware_read(self):
        """
        Tests CreatingSoftware model read
        """
        myModel = CreatingSoftwareF.create(**{
            'version': 'FreeGeoSpatialSoftware 10.1',
            'name': 'FGSS10.1'
        })

        self.assertEqual(myModel.version, 'FreeGeoSpatialSoftware 10.1')
        self.assertEqual(myModel.name, 'FGSS10.1')

    def test_creatingSoftware_update(self):
        """
        Tests CreatingSoftware model update
        """

        myModel = CreatingSoftwareF.create()

        myModel.__dict__.update({
            'version': 'FreeGeoSpatialSoftware 10.1',
            'name': 'FGSS10.1'
        })
        myModel.save()

        self.assertEqual(myModel.version, 'FreeGeoSpatialSoftware 10.1')
        self.assertEqual(myModel.name, 'FGSS10.1')

    def test_creatingSoftware_repr(self):
        """
        Tests CreatingSoftware model repr
        """

        myModel = CreatingSoftwareF.create(**{
            'name': 'FGSS10.1'
        })

        self.assertEqual(unicode(myModel), 'FGSS10.1')
