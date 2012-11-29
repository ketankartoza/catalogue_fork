"""
SANSA-EO Catalogue - reports_dictionaryReport - Reports views
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


class ReportsViews_dictionaryReport_Tests(TestCase):
    """
    Tests reports.py dictionaryReport method/view
    """
    fixtures = [
        'test_user.json',
        'test_mission.json',
        'test_missionsensor.json',
        'test_sensortype.json',
        'test_acquisitionmode.json',
        'test_missiongroup.json'
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
                NoReverseMatch, reverse, 'dictionaryReport',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('dictionaryReport',
                    kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/dictionaryReport/')

    def test_myReports_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('dictionaryReport',
                    kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/dictionaryReport/')

    def test_myReports_stafflogin(self):
        """
        Test view if user is logged as staff and basic functionality
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('dictionaryReport',
                    kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['myTypeResults']), 22)
        self.assertEqual(
            len(myResp.context['myResults']), 35)
        # check used templates
        myExpTemplates = ['dictionaryReport.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
