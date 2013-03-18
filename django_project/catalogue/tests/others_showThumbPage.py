"""
SANSA-EO Catalogue - others_showThumbPage - Others views
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

from django.shortcuts import get_object_or_404
from catalogue.models import GenericProduct


class OthersViews_showThumbPage_Tests(TestCase):
    """
    Tests others.py showThumbPage method/view
    """
    fixtures = [
        'test_user.json',
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

        'test_genericproduct.json',
        'test_processinglevel.json',
        'test_institution.json',
        'test_license.json',
        'test_projection.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_showThumbPage_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showThumbPage',
                kwargs=myKwargTest)

    def test_showThumbPage_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = reverse(
            'showThumbPage',
            kwargs={'theId': '1934163'})
        self.assertRaises(NotImplementedError, myClient.get, myResp)

    def test_showThumbPage_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = reverse(
            'showThumbPage',
            kwargs={'theId': '90541'})
        self.assertRaises(NotImplementedError, myClient.get, myResp)
