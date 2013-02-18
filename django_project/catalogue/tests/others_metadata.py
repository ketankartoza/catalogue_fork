"""
SANSA-EO Catalogue - others_metadata - Others views
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


class OthersViews_metadata(TestCase):
    """
    Tests others.py metadata method/view
    """
    fixtures = [
        'test_user.json',
        'test_spectralgroup.json',
        'test_spectralmode.json',
        'test_scannertype.json',
        'test_instrumenttype.json',
        'test_collection.json',
        'test_satellite.json',
        'test_satelliteinstrument.json',
        'test_productprofile.json',
        'test_genericproduct.json',
        'test_processinglevel.json',
        'test_institution.json',
        'test_license.json',
        'test_projection.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_genericimageryproduct.json',
        'test_genericsensorproduct.json',
        'test_acquisitionmode.json',
        'test_sensortype.json',
        'test_missionsensor.json',
        'test_mission.json',
        'test_missiongroup.json',
    ]

    def setUp(self):
        """
        Set up before each test
        """

    def test_metadata_badURL(self):
        """
        Test badURL requests
        """
        myKwargsTests = [{'testargs':1}]

        for myKwargTest in myKwargsTests:
            self.assertRaises(
                NoReverseMatch, reverse, 'metadata',
                kwargs=myKwargTest)

    def test_metadata_nologin_badproductid(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'metadata',
                kwargs={'theId': '1'}))
        self.assertEqual(myResp.status_code, 404)

    def test_metadata_nologin(self):
        """
        Test view if user is not logged in
        """
        myClient = Client()
        myResp = myClient.get(
            reverse(
                'metadata',
                kwargs={'theId': '1934163'}))
        self.assertEqual(myResp.status_code, 200)
        expString = (
            '\n<h3 class="centered prepend-1 append-1 ">Generic Imagery Produc'
            't details for</h3>\n<p class="centered"><b>S1-_HRV_X--_S1C2_0120_'
            '00_0404_00_860619_084632_1B--_ORBIT-</b></p>\n<p class="centered '
            'prepend-1 append-1">Generic Imagery product is always a composite'
            ' / aggregate product (i.e. it derives from more than one other pr'
            'oduct.</p>\n<p>\n <center>\n   <img src="/thumbnail/1934163/mediu'
            'm/"\n                 class=\'mini-icon\'\n                 alt="'
            'Thumbnail"\n                 id="miniPreview1934163"\n           '
            '      longdesc="1934163"\n                 />\n  </center>\n</p>'
            '\n<table>\n<tr><th colspan="2">Generic Properties</th></tr>\n<tr>'
            '<td class="loud">Product Date</td><td class="quiet">June 19, 1986'
            ', 8:46 a.m.</td></tr>\n<tr><td class="loud">Processing Level</td>'
            '<td class="quiet">Level 3Ba</td></tr>\n<tr><td class="loud">Owner'
            '</td><td class="quiet">Satellite Applications Centre</td></tr>\n<'
            'tr><td class="loud">License</td><td class="quiet">SAC Commercial '
            'License</td></tr>\n<tr><td class="loud">Spatial Coverage</td><td '
            'class="quiet">POLYGON ((21.3566000000000145 -27.2013999999999783,'
            ' 21.4955000000000496 -26.6752999999999929, 22.0914000000000215 -2'
            '6.7661999999999978, 21.9554000000000542 -27.2926999999999964, 21.'
            '3566000000000145 -27.2013999999999783))</td></tr>\n<tr><td class='
            '"loud">Projection</td><td class="quiet">EPSG: 0 ORBIT</td></tr>\n'
            '<tr><td class="loud">Quality</td><td class="quiet">Unknown</td></'
            'tr>\n<tr><td class="loud">Creating Software</td><td class="quiet"'
            '>Unknown</td></tr>\n<tr><td class="loud">Original Product ID</td>'
            '<td class="quiet">11204048606190846322X</td></tr>\n<tr><td class='
            '"loud">Product ID</td><td class="quiet">S1-_HRV_X--_S1C2_0120_00_'
            '0404_00_860619_084632_1B--_ORBIT-</td></tr>\n<tr><td class="loud"'
            '>Product Revision</td><td class="quiet">None</td></tr>\n<tr><th c'
            'olspan="2">Generic Imagery Product-Specific Properties</th></tr>'
            '\n<tr><td class="loud">Imaging Mode</td><td class="quiet"></td></'
            'tr>\n<tr><td class="loud">Spatial Resolution</td><td class="quiet'
            '">20.0</td></tr>\n<tr><td class="loud">Spatial Resolution_x</td><'
            'td class="quiet">20.0</td></tr>\n<tr><td class="loud">Spatial Res'
            'olution_y</td><td class="quiet">20.0</td></tr>\n<tr><td class="lo'
            'ud">Radiometric Resolution</td><td class="quiet">16</td></tr>\n<t'
            'r><td class="loud">Band Count</td><td class="quiet">3</td></tr>\n'
            '</table>\n'
        )

        self.assertEqual(
            myResp.content, expString)
        # check used templates
        myExpTemplates = ['productTypes/genericImageryProduct.html', u'productTypes/genericProduct.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)

    def test_metadata_userlogin(self):
        """
        Test view if user is logged as user
        """
        myClient = Client()
        myClient.login(username='pompies', password='password')
        myResp = myClient.get(
            reverse(
                'metadata',
                kwargs={'theId': '1934163'}))
        self.assertEqual(myResp.status_code, 200)
        expString = (
            '\n<h3 class="centered prepend-1 append-1 ">Generic Imagery Produc'
            't details for</h3>\n<p class="centered"><b>S1-_HRV_X--_S1C2_0120_'
            '00_0404_00_860619_084632_1B--_ORBIT-</b></p>\n<p class="centered '
            'prepend-1 append-1">Generic Imagery product is always a composite'
            ' / aggregate product (i.e. it derives from more than one other pr'
            'oduct.</p>\n<p>\n <center>\n   <img src="/thumbnail/1934163/mediu'
            'm/"\n                 class=\'mini-icon\'\n                 alt="'
            'Thumbnail"\n                 id="miniPreview1934163"\n           '
            '      longdesc="1934163"\n                 />\n  </center>\n</p>'
            '\n<table>\n<tr><th colspan="2">Generic Properties</th></tr>\n<tr>'
            '<td class="loud">Product Date</td><td class="quiet">June 19, 1986'
            ', 8:46 a.m.</td></tr>\n<tr><td class="loud">Processing Level</td>'
            '<td class="quiet">Level 3Ba</td></tr>\n<tr><td class="loud">Owner'
            '</td><td class="quiet">Satellite Applications Centre</td></tr>\n<'
            'tr><td class="loud">License</td><td class="quiet">SAC Commercial '
            'License</td></tr>\n<tr><td class="loud">Spatial Coverage</td><td '
            'class="quiet">POLYGON ((21.3566000000000145 -27.2013999999999783,'
            ' 21.4955000000000496 -26.6752999999999929, 22.0914000000000215 -2'
            '6.7661999999999978, 21.9554000000000542 -27.2926999999999964, 21.'
            '3566000000000145 -27.2013999999999783))</td></tr>\n<tr><td class='
            '"loud">Projection</td><td class="quiet">EPSG: 0 ORBIT</td></tr>\n'
            '<tr><td class="loud">Quality</td><td class="quiet">Unknown</td></'
            'tr>\n<tr><td class="loud">Creating Software</td><td class="quiet"'
            '>Unknown</td></tr>\n<tr><td class="loud">Original Product ID</td>'
            '<td class="quiet">11204048606190846322X</td></tr>\n<tr><td class='
            '"loud">Product ID</td><td class="quiet">S1-_HRV_X--_S1C2_0120_00_'
            '0404_00_860619_084632_1B--_ORBIT-</td></tr>\n<tr><td class="loud"'
            '>Product Revision</td><td class="quiet">None</td></tr>\n<tr><th c'
            'olspan="2">Generic Imagery Product-Specific Properties</th></tr>'
            '\n<tr><td class="loud">Imaging Mode</td><td class="quiet"></td></'
            'tr>\n<tr><td class="loud">Spatial Resolution</td><td class="quiet'
            '">20.0</td></tr>\n<tr><td class="loud">Spatial Resolution_x</td><'
            'td class="quiet">20.0</td></tr>\n<tr><td class="loud">Spatial Res'
            'olution_y</td><td class="quiet">20.0</td></tr>\n<tr><td class="lo'
            'ud">Radiometric Resolution</td><td class="quiet">16</td></tr>\n<t'
            'r><td class="loud">Band Count</td><td class="quiet">3</td></tr>\n'
            '</table>\n'
        )
        self.assertEqual(
            myResp.content, expString)
        # check used templates
        myExpTemplates = ['productTypes/genericImageryProduct.html', u'productTypes/genericProduct.html']

        myUsedTemplates = [tmpl.name for tmpl in myResp.templates]
        self.assertEqual(myUsedTemplates, myExpTemplates)
