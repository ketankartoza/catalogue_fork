"""
SANSA-EO Catalogue - reports_sensorSummaryTable - Reports views
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


class ReportsViews_sensorSummaryTable_Tests(TestCase):
    """
    Tests reports.py sensorSummaryTable method/view
    """
    fixtures = [
        'test_user.json',
        'test_missionsensor.json',
        'test_processinglevel.json',
        'test_missiongroup.json',
        'test_mission.json',
        'test_genericproduct.json',
        'test_institution.json',
        'test_license.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_acquisitionmode.json',
        'test_sensortype.json',
        'test_projection.json',
        # new dicts
        'test_radarbeam.json',
        'test_imagingmode.json',
        'test_spectralgroup.json',
        'test_spectralmode.json',
        'test_scannertype.json',
        'test_instrumenttype.json',
        'test_collection.json',
        'test_satellite.json',
        'test_satelliteinstrument.json',
        'test_radarproductprofile.json',
        'test_opticalproductprofile.json',

        'test_genericsensorproduct.json',
        'test_genericimageryproduct.json',
        'test_taskingrequest.json',
        'test_order.json',
        'test_orderstatus.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_marketsector.json',
        'test_datum',
        'test_resamplingmethod.json',
        'test_fileformat',
        'test_search',
        'test_searchrecord.json',
        'test_opticalproduct.json'
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
                NoReverseMatch, reverse, 'sensorSummaryTable',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('sensorSummaryTable',
                    kwargs={'theSensorId': '34'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/sensorSummaryTable/34/')

    def test_myReports_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('sensorSummaryTable',
                    kwargs={'theSensorId': '34'}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/sensorSummaryTable/34/')

    def test_myReports_stafflogin_generic(self):
        """
        Test view if user is logged as staff and basic functionality
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('sensorSummaryTable',
                    kwargs={'theSensorId': '1'}))
        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            myResp.context['mySensor'].__unicode__(), u'NOAA-14 AVHRR')
        self.assertEqual(
            myResp.context['mySensorYearyStats'].__name__, 'sliceForDisplay')
        self.assertEqual(
            myResp.context['myResults']['Tasking requests for this sensor'], 2)
        self.assertEqual(
            myResp.context['myResults']['Tasking requests all sensors'], 2)
        self.assertEqual(
            myResp.context['myResults']['Searches for this sensor'], 1)
        self.assertEqual(
            myResp.context['myResults']['Searches for all sensors'], 26)
        self.assertEqual(
            myResp.context['myResults']
            ['Total ordered products for this sensor'], 0)
        self.assertEqual(
            myResp.context['myResults']
            ['Total ordered products for all sensors'], 3)
        self.assertEqual(
            myResp.context['myResults']['Total products for this sensor'], 0)
        self.assertEqual(
            myResp.context['myResults']['Total products for all sensors'], 114)
        # check used templates
        myExpTemplates = ['sensorSummaryTable.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_myReports_stafflogin_ordered(self):
        """
        Test view if user is logged as staff and testing
        sensor that has ordered products
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('sensorSummaryTable',
                    kwargs={'theSensorId': '21'}))
        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            myResp.context['mySensor'].__unicode__(), u'SPOT 1 HRV')
        self.assertEqual(
            myResp.context['mySensorYearyStats'].__name__, 'sliceForDisplay')
        self.assertEqual(
            myResp.context['myResults']['Tasking requests for this sensor'], 0)
        self.assertEqual(
            myResp.context['myResults']['Tasking requests all sensors'], 2)
        self.assertEqual(
            myResp.context['myResults']['Searches for this sensor'], 0)
        self.assertEqual(
            myResp.context['myResults']['Searches for all sensors'], 26)
        self.assertEqual(
            myResp.context['myResults']
            ['Total ordered products for this sensor'], 2)
        self.assertEqual(
            myResp.context['myResults']
            ['Total ordered products for all sensors'], 3)
        self.assertEqual(
            myResp.context['myResults']['Total products for this sensor'], 6)
        self.assertEqual(
            myResp.context['myResults']['Total products for all sensors'], 114)
        # check used templates
        myExpTemplates = ['sensorSummaryTable.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
