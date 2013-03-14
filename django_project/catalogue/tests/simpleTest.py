from django.test import TestCase
from catalogue.tests.test_utils import simpleMessage
from catalogue import models


class SimpleTest(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_aquisitionmode.json',
        'test_deliverymethod.json',
        'test_licence.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_fileformat.json',
        'test_processinglevel.json',
        'test_resamplingmethod.json',
        'test_datum.json',
        'test_institution.json',
        'test_projection.json',
        ]

    def setUp(self):
        """
        Sets up before each test
        """
        pass

    def test_MissionGroup_count(self):
        """
        Tests number of entries in missiongroup table
        """
        myExpectedValue = 1
        myMissionGroup_count = models.MissionGroup.objects.all().count()

        self.assertEqual(myMissionGroup_count, myExpectedValue,
                simpleMessage(myMissionGroup_count, myExpectedValue))
