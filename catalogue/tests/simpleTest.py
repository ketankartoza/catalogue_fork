from django.test import TestCase
from catalogue import models


class SimpleTest(TestCase):
    """
    Tests models.
    """
    fixtures = [
                'catalogue.json'
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

        self.assertEqual(myMissionGroup_count, myExpectedValue)
