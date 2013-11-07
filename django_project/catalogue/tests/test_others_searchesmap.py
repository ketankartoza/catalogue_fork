"""
SANSA-EO Catalogue - others_searchesMap - Others views
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


class OthersViews_searchesMap(TestCase):
    """
    Tests others.py searchesMap method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_searchesMap_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'searchesMap',
                kwargs=myKwargTest)

    def test_searchesMap_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'searchesMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/searchesmap/')

    def test_searchesMap_userlogin(self):
        """
        Test view if user is logged as user
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'searchesMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/searchesmap/')

    def test_searchesMap_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'searchesMap',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['myMessages'],
            ['<h3>All searches</h3>', 'Total Searches: 0'])
        self.assertEqual(
            myResp.context['myExtent'], '(-90.0,-45.0, 90.0, 45.0)')
        self.assertEqual(
            len(myResp.context['myLayerDefinitions']), 6)
        myExpLaylersList = (
            '[BlueMarble, heatmap_total, heatmap_last3month, heatmap_lastmonth'
            ', heatmap_lastweek,searches]'
        )
        self.assertEqual(
            myResp.context['myLayersList'], myExpLaylersList)
        self.assertEqual(
            myResp.context['myPartnerFlag'], False)
        self.assertEqual(
            myResp.context['myShowSearchFeatureInfoFlag'], 'true')
        self.assertEqual(
            myResp.context['myLegendFlag'], 'true')
        self.assertEqual(
            myResp.context['mySearchAreasToggle'], 'true')

        # check used templates
        myExpTemplates = [
            'map.html', u'mapbody.html', u'base.html', u'pipeline/css.html',
            u'pipeline/css.html', u'pipeline/js.html', u'menu.html',
            u'useraccounts/menu_content.html', u'page.html',
            u'base-fluid.html', u'pipeline/css.html', u'pipeline/css.html',
            u'menu.html', u'useraccounts/menu_content.html',
            u'pipeline/js.html'
        ]

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
