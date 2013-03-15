"""
SANSA-EO Catalogue - others_showProduct - Others views
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

from catalogue.models import GenericProduct


class OthersViews_showProduct_Tests(TestCase):
    """
    Tests others.py showProduct method/view
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

    def test_showProduct_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showProduct',
                kwargs=myKwargTest)

    def test_showProduct_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'showProduct',
                kwargs={'theProductId': 'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/showProduct/S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-/')

    def test_showProduct_userlogin(self):
        """
        Test view if user is logged as user and product id is found
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'showProduct',
                kwargs={'theProductId': 'S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'}))
        self.assertEqual(myResp.status_code, 200)

        self.assertEqual(
            myResp.context['messages'], ['Product found'])
        myExpProducts, myExpProdType = GenericProduct.objects.filter(product_id='S1-_HRV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-').get().getConcreteProduct()
        self.assertEqual(
            myResp.context['myProduct'], myExpProducts)
        # check used templates
        myExpTemplates = [
            'productView.html', u'base.html', u'menu.html',
            u'useraccounts/menu_content.html',
            'productTypes/genericImageryProduct.html',
            u'productTypes/genericProduct.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_showProduct_userlogin_bad_product(self):
        """
        Test view if user is logged as user and product id is not found
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myReqs = reverse(
            'showProduct',
            kwargs={'theProductId': 'S1-_RVV_X--_S1C2_0120_00_0404_00_860619_084632_1B--_ORBIT-'})
        self.assertRaises(UnboundLocalError, myClient.get, myReqs)
