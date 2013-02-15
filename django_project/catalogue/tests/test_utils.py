"""
SANSA-EO Catalogue - test_utils - common test utils

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '13/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
from django.test.client import RequestFactory

from catalogue.models import User


def simpleMessage(theResult, theExpectedResult, message='', enclose_in=''):
    """Format simple assert message

    Params:
        message - specify more expressive message
        enclose_in - character/text to enclose output with, helpful with strings,
            i.e. theString -> #theString#"""

    return '%(message)s\nGot: %(enclose_in)s%(result)s%(enclose_in)s \n\
Expected: %(enclose_in)s%(expectedResult)s%(enclose_in)s ' % {'message': message,
    'result': theResult, 'expectedResult': theExpectedResult, 'enclose_in': enclose_in}


class SearchTestCase(TestCase):
    """
    General Search Test Case
    """

    fixtures = [
        'test_institution.json',
        'test_license.json',
        'test_projection.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_user.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_genericproduct.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_radarproduct.json',
        # new_dicts
        'test_spectralgroup.json',
        'test_spectralmode.json',
        'test_scannertype.json',
        'test_instrumenttype.json',
        'test_collection.json',
        'test_satellite.json',
        'test_satelliteinstrument.json',
        'test_productprofile.json',

        'test_missiongroup.json'
        ]

    def setUp(self):
        """
        Set up before each test
        """
        self.factory = RequestFactory(enforce_csrf_checks=True)
        #get user object
        self.user = User.objects.get(pk=1)
