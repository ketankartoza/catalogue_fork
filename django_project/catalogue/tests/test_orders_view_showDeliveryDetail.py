"""
SANSA-EO Catalogue - orders_view_showDeliveryDetail - Orders views
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
__version__ = '0.2'
__date__ = '20/08/2013'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF
from .model_factories import OrderF, DeliveryDetailF


class OrdersViews_showDeliveryDetail_Tests(TestCase):
    """
    Tests orders.py showDeliveryDetail method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_showDeliveryDetail_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theReferenceId': 'testtest'}, {'theReferenceId': None},
            {'theReferenceId': 3.14}, {'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showDeliveryDetail',
                kwargs=myKwargTest)

    def test_showDeliveryDetail_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('showDeliveryDetail', kwargs={'theReferenceId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/showdeliverydetail/1/')

    def test_showDeliveryDetail_login_staff(self):
        """
        Test view if user is staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myDeliveryDetail = DeliveryDetailF.create()

        OrderF.create(**{
            'id': 1,
            'delivery_detail': myDeliveryDetail
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('showDeliveryDetail', kwargs={'theReferenceId': 1})
        )

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['myDeliveryDetail'],
            myDeliveryDetail)

        # check used templates
        myExpTemplates = ['deliveryDetail.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]

        self.assertEqual(myUsedTemplates, myExpTemplates)
