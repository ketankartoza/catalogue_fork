"""
SANSA-EO Catalogue - tasking_view_downloadTaskingRequest - Tasking views
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
__date__ = '12/08/2013'
__copyright__ = 'South African National Space Agency'

from django.core.urlresolvers import reverse, NoReverseMatch
from django.test import TestCase
from django.test.client import Client

from core.model_factories import UserF

from model_factories import TaskingRequestF


class TaskingViews_downloadTaskingRequest_Tests(TestCase):
    """
    Tests tasking.py downloadTaskingRequest method/view
    """
    def setUp(self):
        """
        Set up before each test
        """

    def test_downloadTaskingRequest_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [
            {}, {'theId': 'testtest'}, {'theId': None}, {'theId': 3.14},
            {'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'downloadTaskingRequest',
                kwargs=myKwargTest)

    def test_downloadTaskingRequest_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}))
        self.assertEqual(myResp.status_code, 302)
        self.assertEqual(
            myResp['Location'], (
                'http://testserver/accounts/signin/?next=/taskingrequest/1/'))

    def test_downloadTaskingRequest_login_staff_shp(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_1.zip')

    def test_downloadTaskingRequest_login_staff_kml(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'kml': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kml+xml')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_1.kml')

    def test_downloadTaskingRequest_login_staff_kmz(self):
        """
        Test view if staff user is logged in
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'kmz': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(
            myResp['content-type'], 'application/vnd.google-earth.kmz')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_1.kmz')

    def test_downloadTaskingRequest_login_user(self):
        """
        Test view if regular user is logged in
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{'id': 2})

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 2}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_2.zip')

    def test_downloadTaskingRequest_login_user_notowned(self):
        """
        Test view if regular user is logged in, but not owner of target object
        """
        UserF.create(**{
            'username': 'pompies',
            'password': 'password'
        })

        TaskingRequestF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 1}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)
        self.assertEqual(myResp['content-type'], 'application/javascript')
        #check the length of returned script
        self.assertEqual(len(myResp.content), 108)

    def test_downloadTaskingRequest_login_staff_notowned(self):
        """
        Test view if staff user is logged in, but not owner of target object
        """
        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{'id': 2})

        myClient = Client()
        myClient.login(username='timlinux', password='password')
        myResp = myClient.get(
            reverse('downloadTaskingRequest', kwargs={'theId': 2}),
            {'shp': ''})

        self.assertEqual(myResp.status_code, 200)

        # check response
        self.assertEqual(myResp['content-type'], 'application/zip')
        self.assertEqual(
            myResp['content-disposition'],
            'attachment; filename=geometry_for_taskingrequest_2.zip')

    def test_downloadTaskingRequest_login_staff_invalidrequest(self):
        """
        Test view if staff user is logged in, but using invalid request params
        """

        UserF.create(**{
            'username': 'timlinux',
            'password': 'password',
            'is_staff': True
        })

        TaskingRequestF.create(**{'id': 1})

        myClient = Client()
        myClient.login(username='timlinux', password='password')

        myTestParams = [{}, {'test': ''}, {'json': ''}]

        for myTestParam in myTestParams:
            myResp = myClient.get(
                reverse('downloadTaskingRequest', kwargs={'theId': 1}),
                myTestParam)

            self.assertEqual(myResp.status_code, 404)
