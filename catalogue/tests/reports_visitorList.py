"""
SANSA-EO Catalogue - reports_visitorList - Reports views
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

from catalogue.models import Visit


class ReportsViews_visitorList_Tests(TestCase):
    """
    Tests reports.py visitorList method/view
    """
    fixtures = [
        'test_user.json',
        'test_visit.json',
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
                NoReverseMatch, reverse, 'visitorList',
                kwargs=myKwargTest)

    def test_myReports_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/visitorlist/')

    def test_myReports_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            myResp.context['app_path'], u'/visitorlist/')

    def test_myReports_stafflogin(self):
        """
        Test view if user is logged as staff
        """
        myRecords = Visit.objects.all().order_by('-visit_date')
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}))
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['myRecords'].object_list), len(myRecords))
        # check used templates
        myExpTemplates = ['visitors.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_myReports_stafflogin_pdf(self):
        """
        Test view if pdf is requested
        """
        myRecords = Visit.objects.all().order_by('-visit_date')
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}), {'pdf': ''})
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['myRecords'].object_list), len(myRecords))
        # check used templates
        myExpTemplates = ['pdf/visitors.html', u'pdfpage.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        self.assertEqual(myResp['content-type'], 'application/pdf')
        self.assertEqual(
            myResp['content-disposition'], 'attachment; filename=report.pdf')

    def test_myReports_stafflogin_invalidpage(self):
        """
        Test view if user is logged in, specifying invalid page parameter
        View will default to page 1
        """
        myRecords = Visit.objects.all().order_by('-visit_date')
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}), {'page': 'this is a new page!'})
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['myRecords'].object_list), len(myRecords))
        # check used templates
        myExpTemplates = ['visitors.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_myReports_stafflogin_outboundpage(self):
        """
        Test view if user is logged in, specifying outbound page parameter
        View will default to page 1
        """
        myRecords = Visit.objects.all().order_by('-visit_date')
        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse(
                'visitorList',
                kwargs={}), {'page': '10001'})
        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(
            len(myResp.context['myRecords'].object_list), len(myRecords))
        # check used templates
        myExpTemplates = ['visitors.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
