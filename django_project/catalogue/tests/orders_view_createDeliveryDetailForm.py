"""
SANSA-EO Catalogue - orders_view_createDeliveryDetailForm - Orders views
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
__date__ = '23/10/2012'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from catalogue.forms import ProductDeliveryDetailForm


class OrdersViews_createDeliveryDetailForm_Tests(TestCase):
    """
    Tests orders.py createDeliveryDetailForm method/view
    """

    fixtures = [
        'test_fileformat.json',
        'test_marketsector.json',
        'test_institution.json',
        'test_license.json',
        'test_projection.json',
        'test_quality.json',
        'test_datum.json',
        'test_resamplingmethod.json',
        'test_creatingsoftware.json',
        'test_deliverymethod.json',
        'test_deliverydetail.json',
        'test_search.json',
        'test_searchdaterange.json',
        'test_processinglevel.json',
        # new_dicts
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
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_opticalproduct.json',
        'test_user.json',
        'test_orderstatus.json',
        'test_orderstatushistory.json',
        'test_order.json',
        'test_searchrecord.json'
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_createDeliveryDetailForm_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theReferenceId': 'testtest'}, {'theReferenceId': None},
            {'theReferenceId': 3.14}, {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'createDeliveryDetailForm',
                kwargs=myKwargTest)

    def test_createDeliveryDetailForm_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('createDeliveryDetailForm', kwargs={'theReferenceId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/deliverydetailform/1/')

    def test_createDeliveryDetailForm_login_staff(self):
        """
        Test view if user is staff
        """

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('createDeliveryDetailForm', kwargs={'theReferenceId': 1}))

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['myDeliveryDetailForm'].__class__,
            ProductDeliveryDetailForm)

        # check used templates
        myExpTemplates = 'deliveryDetailForm.html'
        myUsedTemplates = myResp.template.name

        self.assertEqual(myUsedTemplates, myExpTemplates)
