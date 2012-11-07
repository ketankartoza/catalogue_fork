"""
SANSA-EO Catalogue - Order_model - implements basic CRUD unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__date__ = '10/07/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from catalogue.models.new_dictionaries import (
    Collection,
    Satellite,
    SatelliteInstrument,
    InstrumentType,
    InstrumentTypeSpectralMode,
    SpectralMode
)
from catalogue.models import Order
from datetime import datetime


class NewDictionariesTest(TestCase):

    fixtures = [
        'test_institution.json',
        'test_collection.json',
        'test_satellite.json',
        'test_satelliteinstrument.json',
        'test_instrumenttype.json',
        'test_instrumenttypespectralmode.json',
        'test_spectralmode.json',
        'test_scannertype.json'
    ]

    def test_relatedSpectralModes(self):
        """Test we can get related spectral modes for an instrument."""
        myInstrumentType = InstrumentType.objects.all()[0]
        myRelated = myInstrumentType.relatedSpectralModes()
        myMessage = 'No spectral modes found to be related to InstrumentType'
        self.assertNotEqual(0, myRelated.count(), myMessage)

    def test_relatedScannerType(self):
        """Test we can get related scanner types for an instrument."""
        myInstrumentType = InstrumentType.objects.all()[0]
        myRelated = myInstrumentType.relatedScannerType()
        myMessage = 'No scanner types found to be related to InstrumentType'
        assert myRelated is not None, myMessage

    def test_relatedSatelliteInstruments(self):
        """Test we can get related satellite instruments for a satellite."""
        mySatellite = Satellite.objects.all()[0]
        myRelated = mySatellite.relatedSatelliteInstruments()
        myMessage = 'No satellite instruments found for satellite'
        self.assertNotEqual(0, myRelated.count(), myMessage)

    def test_relatedSatellites(self):
        """Test we can get related satellites for a collection."""
        myCollection = Collection.objects.all()[0]
        myRelated = myCollection.relatedSatellites()
        myMessage = 'No satellites found for collection'
        self.assertNotEqual(0, myRelated.count(), myMessage)
