"""
SANSA-EO Catalogue - tasking_view_viewTaskingRequest - Tasking views unittests

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


from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from catalogue.forms import OrderStatusHistoryForm

from core.model_factories import UserF
from .model_factories import TaskingRequestF


class TaskingViews_viewTaskingRequest_Tests(TestCase):
    """
    Tests tasking.py viewTaskingRequest method/view
    """

    def setUp(self):
        """
        Set up before each test
        """

    def test_viewTaskingRequest_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'viewTaskingRequest',
                kwargs=myKwargTest)

    def test_viewTaskingRequest_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('viewTaskingRequest', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'],
            'http://testserver/accounts/signin/?next=/viewtaskingrequest/1/')

    def test_viewTaskingRequest_login_staff(self):
        """
        Test view if user is staff
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{
            'id': 1,
            'user': myUser
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewTaskingRequest', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 200)
        # is OrderStatusHistoryForm initialized
        self.assertEqual(
            myResp.context['myForm'].__class__, OrderStatusHistoryForm)

        # check used templates
        myExpTemplates = [
            'taskingRequestPage.html', u'base.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequest = myResp.context['myTaskingRequest']
        self.assertEqual(myTaskingRequest.pk, 1)

    def test_viewTaskingRequest_login_user(self):
        """
        Test view if user is not staff
        """
        myUser = UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        TaskingRequestF.create(**{
            'id': 2,
            'user': myUser
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewTaskingRequest', kwargs={'theId': 2}))

        self.assertEqual(myResp.status_code, 200)
        # is OrderStatusHistoryForm initialized
        self.assertEqual(
            myResp.context['myForm'].__class__, None.__class__)

        # check used templates
        myExpTemplates = [
            'taskingRequestPage.html', u'base.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequest = myResp.context['myTaskingRequest']
        self.assertEqual(myTaskingRequest.pk, 2)

    def test_viewTaskingRequest_staff_access(self):
        """
        Test staff user object access
        Staf
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{
            'id': 1,
            'user': myUser
        })
        # add another TR, owned by some user
        TaskingRequestF.create(**{'id': 1234})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewTaskingRequest', kwargs={'theId': 1234}))

        self.assertEqual(myResp.status_code, 200)
        # is OrderStatusHistoryForm initialized
        self.assertEqual(
            myResp.context['myForm'].__class__, OrderStatusHistoryForm)

        # check used templates
        myExpTemplates = [
            'taskingRequestPage.html', u'base.html', u'menu.html',
            u'useraccounts/menu_content.html', u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

        #check taskingrequest object
        myTaskingRequest = myResp.context['myTaskingRequest']
        self.assertEqual(myTaskingRequest.pk, 1234)

    def test_viewTaskingRequest_user_access(self):
        """
        Test regular user object access
        Regular users can only access owned tasking requests
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        TaskingRequestF.create(**{
            'id': 1,
            'user': myUser
        })

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewTaskingRequest', kwargs={'theId': 1}))

        self.assertEqual(myResp.status_code, 404)

    def test_viewTaskingRequest_non_existent(self):
        """
        Ensure that non-existent Requests throw a 404.
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('viewTaskingRequest', kwargs={'theId': 123987}))

        self.assertEqual(myResp.status_code, 404)

    def test_viewTaskingRequest_ajax_requests(self):
        """
        Test view if the request is an AJAX request
        """
        myUser = UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{
            'id': 1,
            'user': myUser
        })

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('viewTaskingRequest', kwargs={'theId': 1}),
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(myResp.status_code, 200)
        # is OrderStatusHistoryForm initialized
        self.assertEqual(
            myResp.context['myForm'].__class__, OrderStatusHistoryForm)

        # check used templates
        myExpTemplates = [
            'taskingRequestPageAjax.html', u'emptytemplate.html',
            u'taskingRequest.html']
        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
