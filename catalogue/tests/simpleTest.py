from django.test import TestCase
from catalogue import models


class SimpleTest(TestCase):
    """
    Tests models.
    """
    fixtures = [
        'test_aquisitionmode.json',
        'test_deliverymethod.json',
        'test_licence.json',
        'test_missionsensor.json',
        'test_quality.json',
        'test_creatingsoftware.json',
        'test_fileformat.json',
        'test_missiongroup.json',
        'test_processinglevel.json',
        'test_resamplingmethod.json',
        'test_datum.json',
        'test_institution.json',
        'test_mission.json',
        'test_projection.json',
        'test_sensortype.json'
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
