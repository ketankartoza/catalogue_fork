"""
SANSA-EO Catalogue - others_showPreview - Others views
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


class OthersViews_showPreview_Tests(TestCase):
    """
    Tests others.py showPreview method/view
    """
    fixtures = [
        'test_user.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_showPreview_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'showPreview',
                kwargs=myKwargTest)

    def test_showPreview_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'showPreview',
                kwargs={'theId': '1', 'theSize': 'a'}))
        self.assertEqual(myResp.status_code, 200)
        expString = (
            '<center><img src="/thumbnail/1/a/"><center><img src="/media/image'
            's/info_32.png" onclick=\'showMetadata(1);\'  alt="Click to view m'
            'etadata for this image"\n            title="Click to view metadat'
            'a for this image" />&nbsp;<img src="/media/images/buy_32.png" onc'
            'lick=\'addToCart(1);\'  alt="Click to add to your cart" title="Cl'
            'ick\n            to add this image to your cart" />&nbsp;<a data-'
            'toggle="modal" data-target="#myModal" id="large_preview" href="/t'
            'humbnailpage/1/"><img src="/media/images/search_32.png" alt="Clic'
            'k for larger\n            view" title="Click for larger preview"/'
            '></a></center>'
        )
        self.assertEqual(
            myResp.content, expString)
        # check used templates
        myExpTemplates = []

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_showPreview_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'showPreview',
                kwargs={'theId': '1', 'theSize': 'a'}))
        self.assertEqual(myResp.status_code, 200)
        expString = (
            '<center><img src="/thumbnail/1/a/"><center><img src="/media/image'
            's/info_32.png" onclick=\'showMetadata(1);\'  alt="Click to view m'
            'etadata for this image"\n            title="Click to view metadat'
            'a for this image" />&nbsp;<img src="/media/images/buy_32.png" onc'
            'lick=\'addToCart(1);\'  alt="Click to add to your cart" title="Cl'
            'ick\n            to add this image to your cart" />&nbsp;<a data-'
            'toggle="modal" data-target="#myModal" id="large_preview" href="/t'
            'humbnailpage/1/"><img src="/media/images/search_32.png" alt="Clic'
            'k for larger\n            view" title="Click for larger preview"/'
            '></a></center>'
        )
        self.assertEqual(
            myResp.content, expString)
        # check used templates
        myExpTemplates = []

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
