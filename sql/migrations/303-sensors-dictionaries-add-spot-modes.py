"""
Add acquisition modes for spot
Can be run from project dir with
$ python manage.py runscript -s -v 2 --pythonpath=./sql/migrations 303-sensors-dictionaries-add-spot-modes.py

"""

TEST_ONLY=False
ABORT_ON_EXTRA_VALUES=False

from django.core.management import setup_environ
from django.db import transaction
from catalogue.models import *
import traceback
import sys


try:
    import settings
except ImportError:
    import sys
    sys.stderr.write("Couldn't find the settings.py module.")
    sys.exit(1)

setup_environ(settings)


# Commit explicitly
transaction.enter_transaction_management()
transaction.managed()
try:
    # Handle rollback on errors
    # Defaults
    spot_missions = Mission.objects.filter( operator_abbreviation__startswith = "SPOT" )
    print "Spot missions:"
    print "===================="
    print "===================="
    print "===================="
    for myMission in spot_missions:
        print myMission #.operator_abbreviation

        mission_sensors = MissionSensor.objects.filter( mission=myMission )
        print "Spot sensors for mission:" + str(myMission)
        print "===================="
        print "===================="
        for mySensor in mission_sensors:
            print mySensor #.operator_abbreviation

            sensor_types = SensorType.objects.filter( mission_sensor=mySensor )
            print "Spot sensor types for sensor:" +str(mySensor)
            print "===================="
            for mySensorType in sensor_types:
                print "Adding Cam1 and Cam2 for spot sensor type: " + str(mySensorType) #.operator_abbreviation
                myMode = AcquisitionMode()
                myMode.sensor_type = mySensorType
                myMode.abbreviation = str(myMission.abbreviation) + "C1"
                myMode.name = "Camera 1"
                myMode.geometric_resolution = 0
                myMode.band_count = 0
                myMode.is_grayscale = 0
                myMode.operator_abbreviation = str(myMission.abbreviation) + "C1"
                myMode.save()
                myMode2 = AcquisitionMode()
                myMode2.sensor_type = mySensorType
                myMode2.abbreviation =  str(myMission.abbreviation) + "C2"
                myMode2.name = "Camera 2"
                myMode2.geometric_resolution = 0
                myMode2.band_count = 0
                myMode2.is_grayscale = 0
                myMode2.operator_abbreviation = str(myMission.abbreviation) + "C2"
                myMode2.save()

    if TEST_ONLY:
        # Rollback
        print 'Testing: rolling back...'
        transaction.rollback()
    else:
        # Commit
        print 'Committing...'
        transaction.commit()
except Exception, e:
    print 'Errors: rolling back...'
    transaction.rollback()
    traceback.print_exc(file=sys.stdout)
finally:
    transaction.leave_transaction_management()
