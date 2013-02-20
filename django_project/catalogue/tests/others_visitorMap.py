"""
SANSA-EO Catalogue - others_VisitorMap - Others views
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


class OthersViews_visitorMap_Tests(TestCase):
    """
    Tests others.py visitorMap method/view
    """
    fixtures = [
        'test_user.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_visitorMap_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'visitorMap',
                kwargs=myKwargTest)

    def test_visitorMap_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'visitorMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/visitormap/')

    def test_visitorMap_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'visitorMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/visitormap/')

    def test_visitorMap_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['myMessages']), 8)
        self.assertEqual(
            len(myResp.context['myExtents']), 16)
        self.assertEqual(
            len(myResp.context['myLayerDefinitions']), 6)
        myExpLaylersList = (
            '[zaSpot10mMosaic2010,zaSpot10mMosaic2009,zaSpot10mMosaic2008,'
            'zaSpot10mMosaic2007,zaRoadsBoundaries,visitors]'
        )
        self.assertEqual(
            myResp.context['myLayersList'], myExpLaylersList)
        myExpActiveBaseMap = (
            'zaSpot10mMosaic2010'
        )
        self.assertEqual(
            myResp.context['myActiveBaseMap'], myExpActiveBaseMap)
        # check used templates
        myExpTemplates = [
            'simpleMap.html', u'base.html', u'menu.html',
            u'useraccounts/menu_content.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
