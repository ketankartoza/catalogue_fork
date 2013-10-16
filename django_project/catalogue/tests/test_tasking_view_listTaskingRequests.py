"""
SANSA-EO Catalogue - tasking_view_listTaskingRequests - Tasking views unittests

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
__date__ = '12/08/2013'
__copyright__ = 'South African National Space Agency'

from datetime import date

from django.core.urlresolvers import reverse, NoReverseMatch
from django.template import TemplateDoesNotExist
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF

from .model_factories import TaskingRequestF


class TaskingViews_listTaskingRequests_Tests(TestCase):
    """
    Tests tasking.py listTaskingRequests method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_listTaskingRequests_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs': 1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'listTaskingRequests',
                kwargs=myKwargTest)

    def test_listTaskingRequests_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('listTaskingRequests', kwargs={}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/listtaskingrequests/')

    def test_listTaskingRequests_login_staff(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('listTaskingRequests', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], '/listtaskingrequests/')

        # check used templates
        myExpTemplates = [
            'taskingRequestListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequestList.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

        myCurrentMonth = myResp.context['myCurrentMonth']
        self.assertEqual(myCurrentMonth, date.today())

    def test_listTaskingRequests_login_user(self):
        """
        Test view if regular user is logged in
        """

        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        TaskingRequestF.create(**{
            'user': myUser
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('listTaskingRequests', kwargs={}))

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], '/listtaskingrequests/')

        # check used templates
        myExpTemplates = [
            'taskingRequestListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequestList.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

        myCurrentMonth = myResp.context['myCurrentMonth']
        self.assertEqual(myCurrentMonth, date.today())

    def test_listTaskingRequests_pdf_pageSize(self):
        """
        Test view if pdf is requested

        WARNING: PDF report for this view is not fully implemented
        Rasies -> TemplateDoesNotExist
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })
        TaskingRequestF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        self.assertRaises(
            TemplateDoesNotExist, myClient.get,
            reverse('listTaskingRequests', kwargs={}), {'pdf': ''})

    def test_listTaskingRequests_login_page_param_existant(self):
        """
        Test view if staff user is logged in, specifying page param
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('listTaskingRequests', kwargs={}),
            {'page': '1'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], '/listtaskingrequests/')

        # check used templates
        myExpTemplates = [
            'taskingRequestListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequestList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

        myCurrentMonth = myResp.context['myCurrentMonth']
        self.assertEqual(myCurrentMonth, date.today())

    def test_listTaskingRequests_login_page_param_nonexistant(self):
        """
        Test view if staff user is logged in, specifying page param, that does
        not exist
        View will default to page 1
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('listTaskingRequests', kwargs={}),
            {'page': '1000'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], '/listtaskingrequests/')

        # check used templates
        myExpTemplates = [
            'taskingRequestListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequestList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

        myCurrentMonth = myResp.context['myCurrentMonth']
        self.assertEqual(myCurrentMonth, date.today())

    def test_listTaskingRequests_login_page_param_invalid_input(self):
        """
        Test view if staff user is logged in, specifying invalid page param
        View will default to page 1
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create()

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('listTaskingRequests', kwargs={}),
            {'page': 'this is a new page'})

        self.assertEqual(myResp.status_code, 200)
        # check response
        self.assertEqual(myResp.context['myUrl'], '/listtaskingrequests/')

        # check used templates
        myExpTemplates = [
            'taskingRequestListPage.html', u'base.html', u'pipeline/js.html',
            u'pipeline/css.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequestList.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequests = myResp.context['myRecords']
        self.assertEqual(len(myTaskingRequests.object_list), 1)

        myCurrentMonth = myResp.context['myCurrentMonth']
        self.assertEqual(myCurrentMonth, date.today())
