"""
SANSA-EO Catalogue - reports_searchHistory - Reports views
    unittests

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '22/11/2012'
__copyright__ = 'South African National Space Agency'

import datetime
from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client


class ReportsViews_searchHistory_Tests(TestCase):
    """
    Tests reports.py searchHistory method/view
    """
    fixtures = [
        'test_user.json',
        'test_search.json',
        'test_searchdatarange.json',
        'test_searchrecord.json',
        'test_missionsensor.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_order.json',
        #'test_taskingrequest.json',
        'test_processinglevel.json',
        'test_fileformat.json',
        'test_projection.json',
        'test_datum.json',
        'test_resamplingmethod.json',
        #'test_fileformat.json',
        'test_missiongroup.json',
        'test_mission.json',
        #'test_missionsensor.json',
        'test_genericproduct.json',
        'test_institution.json',
        'test_license.json',
        'test_quality.json',
        'test_creatingsoftware.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_myReports_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'mysearches',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('searchHistory', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/mysearches/')

    def test_myReports_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('searchHistory', kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['mySearches']), 1)
        # check used templates
        myExpTemplates = ['mySearches.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_myReports_stafflogin(self):
        """
        Test view if staff is logged as user
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('searchHistory', kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['mySearches']), 25)
        # check used templates
        myExpTemplates = ['mySearches.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
