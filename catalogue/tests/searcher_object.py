"""
SANSA-EO Catalogue - searcher_object - tests correctness of
    search results

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
__date__ = '14/06/2012'
__copyright__ = 'South African National Space Agency'

from django.test import TestCase
try:
    #this is only available in Django 1.3+
    #fallback to one defined in utils
    from django.test.client import RequestFactory
except ImportError, e:
    from catalogue.tests.test_utils import RequestFactory

from catalogue.tests.test_utils import simpleMessage
from catalogue.views.searcher import Searcher
from catalogue.models import Search, User

from django.test.client import Client

class BandCountSearches_Test(TestCase):
    """
    Tests FeatureReaders returned geometry type
    """

    fixtures = [
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
        'test_radarproduct.json'
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        self.factory = RequestFactory(enforce_csrf_checks=True)
        #authenticate
        self.factory.login(username='timlinux', password='chrisdebug')
        #get user object
        self.user = User.objects.get(pk=1)

    def test_Panchromatic_bandcount(self):
        """
        """
        for search in Search.objects.all():
            #create a fake request object
            request = self.factory.get(
                '/searchresult/%s' % search.guid)
            #assign user to request (usually done by middleware)
            request.user = self.user
            #create Searcher object
            mySearcher = Searcher(request, search.guid)
            mySearcher.search()
            print len(mySearcher.mRecordCount)
        #fail test
        assert 1 == 2, 'bla'
