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
__version__ = '0.2'
__date__ = '09/08/2013'
__copyright__ = 'South African National Space Agency'


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF

from .model_factories import OpticalProductF


class OthersViews_showThumbPage_Tests(TestCase):
    """
    Tests others.py showThumbPage method/view
    """

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
        OpticalProductF.create(**{'id':123})
        myClient = Client()
        myResp = reverse('showThumbPage', kwargs={'theId': '123'})

        self.assertRaises(NotImplementedError, myClient.get, myResp)

    def test_showThumbPage_userlogin(self):
        """
        Test view if user is logged as user
        """

        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        OpticalProductF.create(**{'id':123})

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = reverse('showThumbPage', kwargs={'theId': '123'})

        self.assertRaises(NotImplementedError, myClient.get, myResp)
