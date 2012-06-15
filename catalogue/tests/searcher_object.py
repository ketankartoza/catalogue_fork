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


class SearcherObject_Test(TestCase):
    """
    Tests Searcher object
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
        Test Panchromatic band count, range 0-2
        """
        myTestSearches = [5]
        myExpectedResults = [8]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            #create a fake request object
            request = self.factory.get(
                '/searchresult/%s' % mySearch.guid)
            #assign user to request (usually done by middleware)
            request.user = self.user

            #create Searcher object
            mySearcher = Searcher(request, mySearch.guid)
            mySearcher.search()

            assert mySearcher.mQuerySet.count() >= myExpectedResults[idx], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s expected more then:' % searchPK)

    def test_Truecolor_bandcount(self):
        """
        Test Truecolor band count, range 3
        """
        myTestSearches = [6]
        myExpectedResults = [50]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            #create a fake request object
            request = self.factory.get(
                '/searchresult/%s' % mySearch.guid)
            #assign user to request (usually done by middleware)
            request.user = self.user

            #create Searcher object
            mySearcher = Searcher(request, mySearch.guid)
            mySearcher.search()

            assert mySearcher.mQuerySet.count() >= myExpectedResults[idx], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s expected more then:' % searchPK)

    def test_Multispectral_bandcount(self):
        """
        Test Multispectral band count, range 4-8
        """
        myTestSearches = [7]
        myExpectedResults = [15]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            #create a fake request object
            request = self.factory.get(
                '/searchresult/%s' % mySearch.guid)
            #assign user to request (usually done by middleware)
            request.user = self.user

            #create Searcher object
            mySearcher = Searcher(request, mySearch.guid)
            mySearcher.search()

            assert mySearcher.mQuerySet.count() >= myExpectedResults[idx], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s expected more then:' % searchPK)

    def test_Superspectral_bandcount(self):
        """
        Test Superspectral band count, range 9-40
        """
        myTestSearches = [8]
        myExpectedResults = [1]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            #create a fake request object
            request = self.factory.get(
                '/searchresult/%s' % mySearch.guid)
            #assign user to request (usually done by middleware)
            request.user = self.user

            #create Searcher object
            mySearcher = Searcher(request, mySearch.guid)
            mySearcher.search()

            assert mySearcher.mQuerySet.count() == myExpectedResults[idx], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s:' % searchPK)

    def test_Hyperspectral_bandcount(self):
        """
        Test Hyperspectral band count, range 41-1000
        """
        myTestSearches = [9]
        myExpectedResults = [1]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            #create a fake request object
            request = self.factory.get(
                '/searchresult/%s' % mySearch.guid)
            #assign user to request (usually done by middleware)
            request.user = self.user

            #create Searcher object
            mySearcher = Searcher(request, mySearch.guid)
            mySearcher.search()

            assert mySearcher.mQuerySet.count() == myExpectedResults[idx], \
            simpleMessage(mySearcher.mQuerySet.count(), myExpectedResults[idx],
                message='For search pk %s:' % searchPK)

    def test_isAdvanced(self):
        """
        Tests if search is an advanced search
        """
        #test searches pk
        myTestSearches = [1, 4, 5, 6]
        myExpectedResults = [False, False, True, True]

        for idx, searchPK in enumerate(myTestSearches):
            mySearch = Search.objects.get(pk=searchPK)

            assert mySearch.isAdvanced == myExpectedResults[idx], \
            simpleMessage(mySearch.isAdvanced, myExpectedResults[idx],
                message='For search pk %s:' % searchPK)
