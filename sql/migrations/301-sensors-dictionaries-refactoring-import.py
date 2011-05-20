"""

Can be run from project dir with
$ python manage.py runscript -s -v 2 --pythonpath=./sql/migrations 201-sensors-dictionaries-refactoring-import.py

CSV files are in "sql/migrations/dictionaries_v5" folder

"""

TEST_ONLY=True
CSV_FOLDER="sql/migrations/dictionaries_v5"

from django.core.management import setup_environ
import csv
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

#settings.DISABLE_TRANSACTION_MANAGEMENT=True
setup_environ(settings)

# Commit explicitly
transaction.enter_transaction_management()
transaction.managed()

# Handle rollback on errors
try:

    # Delete all MISR, MODIS and RE (sensors have changed), need to re-run ingestors
    to_delete = Mission.objects.filter(abbreviation__in=['MCD', 'MYD', 'MOD', 'RE1', 'RE2', 'RE3', 'RE4', 'RE5'])
    print "Deleting (%s) products for missions 'MCD', 'MYD', 'MOD', 'RE1', 'RE2', 'RE3', 'RE4', 'RE5', need to re-run ingestors..." % to_delete.count()
    to_delete.delete()

    #################################
    #
    # Mission
    #
    #################################
    print '-' * 40
    print "Importing Mission objects..."
    print '-' * 40
    obj = []
    obj_keys = []
    for m in csv.DictReader(open(CSV_FOLDER + '/Mission.csv'), delimiter='\t', quotechar='"'):
        obj.append(m)
        obj_keys.append(m['SAC_Satellite_Abbreviation'].strip())

    # Check that the DB does not contain any additional entry, abort if yes
    obj_extra = Mission.objects.exclude(abbreviation__in=obj_keys)
    #import ipy; ipy.shell()
    if obj_extra.count():
        for m in obj_extra:
            print 'Extra Mission: %s: %s' % (m, m.name)
        raise Exception, 'Mission contains extra values.'

    for row in obj:
        # Map fields
        data = {
            'abbreviation' : row['SAC_Satellite_Abbreviation'].strip(),
            'operator_abbreviation' : row['Satellite_Abbreviation'].strip(),
            'owner' : row['Satellite_Owner'].strip(),
            'name' : row['Satellite_Name'].strip(),
            'mission_group' : MissionGroup.objects.all()[0],
        }
        # Check if already in DB
        try:
            m = Mission.objects.get(abbreviation=row['SAC_Satellite_Abbreviation'].strip())
            print "\tFound\t\t%s: updating..." % m
            # Assign data
            for k in data.keys():
                setattr(m, k, data[k])
            m.save()
        except Mission.DoesNotExist:
            print "\tNot found\t%s: creating..." % row['SAC_Satellite_Abbreviation'].strip()
            m = Mission(**data)
            m.save()

    #################################
    #
    # MissionSensor
    #
    #################################
    print '-' * 40
    print "Importing MissionSensors objects..."
    print '-' * 40
    obj = []
    obj_keys = []

    for m in csv.DictReader(open(CSV_FOLDER + '/MissionSensor.csv'), delimiter='\t', quotechar='"'):
        obj.append(m)
        obj_keys.append("%s:%s" % (m['SAC_Sensor_Abbreviation'].strip(), m['Satellite_Abbreviation'].strip()))

    # Check that the DB does not contain any additional entry, abort if yes
    obj_extra = []
    for st in MissionSensor.objects.all():
        if not "%s:%s" % (st.abbreviation, st.mission.operator_abbreviation) in obj_keys:
            obj_extra.append(st)

    #import ipy; ipy.shell()
    if len(obj_extra):
        for m in obj_extra:
            print 'Extra MissionSensor: %s:%s' % (m.abbreviation, m.name)
        raise Exception, 'MissionSensor contains extra values.'

    for row in obj:
        # Map fields
        data = {
            'abbreviation' : row['SAC_Sensor_Abbreviation'].strip(),
            'operator_abbreviation' : row['Sensor_Abbreviation'].strip(),
            'name' : row['Sensor_Name'].strip(),
            'mission' : Mission.objects.get(operator_abbreviation=row['Satellite_Abbreviation'].strip()),
        }
        # Check if already in DB
        try:
            m = MissionSensor.objects.get(abbreviation=row['SAC_Sensor_Abbreviation'].strip())
            print "\tFound\t\t%s: updating..." % m
            # Assign data
            for k in data.keys():
                setattr(m, k, data[k])
            m.save()
        except MissionSensor.DoesNotExist:
            print "\tNot found\t%s: creating..." % row['SAC_Sensor_Abbreviation'].strip()
            m = MissionSensor(**data)
            m.save()


    #################################
    #
    # SensorType
    #
    #################################
    print '-' * 40
    print "Importing SensorType objects..."
    print '-' * 40
    obj = []
    obj_keys = []
    for m in csv.DictReader(open(CSV_FOLDER + '/SensorType.csv'), delimiter='\t', quotechar='"'):
        obj.append(m)
        obj_keys.append("%s:%s" % (m['SAC_Sensor_Type_Abbreviation'].strip(), m['Sensor_Abbreviation'].strip()))

    # Check that the DB does not contain any additional entry, abort if yes
    obj_extra = []
    for st in SensorType.objects.all():
        if not "%s:%s" % (st.abbreviation, st.mission_sensor.operator_abbreviation) in obj_keys:
            obj_extra.append(st)
    #import ipy; ipy.shell()
    if len(obj_extra):
        for m in obj_extra:
            print 'Extra SensorType: %s' % m
        raise Exception, 'SensorType contains extra values.'

    for row in obj:
        # Map fields
        data = {
            'abbreviation' : row['SAC_Sensor_Type_Abbreviation'].strip(),
            'operator_abbreviation' : row['Sensor_Type_Abbreviation'].strip(),
            'name' : row['Sensor_Type_Name'].strip(),
            'geometric_resolution' : int(row['Resolution']),
            'band_count' : int(row['Bands']),
            'mission_sensor' : MissionSensor.objects.get(operator_abbreviation=row['Sensor_Abbreviation'].strip(), abbreviation=row['SAC_Sensor_Abbreviation'].strip()),
        }
        # Check if already in DB
        try:
            m = SensorType.objects.get(abbreviation=row['SAC_Sensor_Type_Abbreviation'].strip(), mission_sensor=data['mission_sensor'])
            print "\tFound\t\t%s: updating..." % m
            # Assign data
            for k in data.keys():
                setattr(m, k, data[k])
            m.save()
        except SensorType.DoesNotExist:
            print "\tNot found\t%s: creating..." % row['SAC_Sensor_Abbreviation'].strip()
            m = SensorType(**data)
            m.save()

    #################################
    #
    # AcquisitionMode
    #
    #################################
    print '-' * 40
    print "Importing AcquisitionMode objects..."
    print '-' * 40
    obj = []
    obj_keys = []
    for m in csv.DictReader(open(CSV_FOLDER + '/AcquisitionMode.csv'), delimiter='\t', quotechar='"'):
        obj.append(m)
        obj_keys.append("%s:%s" % (m['SAC_Acquisition_Mode_Abbreviation'].strip(), m['Sensor_Type_Abbreviation'].strip()))

    # Check that the DB does not contain any additional entry, abort if yes
    obj_extra = []
    for st in AcquisitionMode.objects.all():
        if not "%s:%s" % (st.abbreviation, st.sensor_type.abbreviation) in obj_keys:
            obj_extra.append(st)
    #import ipy; ipy.shell()
    if len(obj_extra):
        for m in obj_extra:
            print 'Extra AcquisitionMode: %s' % m
        raise Exception, 'AcquisitionMode contains extra values.'

    for row in obj:
        # Map fields
        data = {
            'abbreviation' : row['SAC_Acquisition_Mode_Abbreviation'].strip(),
            'operator_abbreviation' : row['Acquisition_Mode_Abbreviation'].strip(),
            'name' : row['Acquisition_Mode_Name'].strip(),
            'sensor_type' : SensorType.objects.get(operator_abbreviation=row['Sensor_Abbreviation'].strip(), abbreviation=row['SAC_Sensor_Abbreviation'].strip()),
        }
        # Check if already in DB
        try:
            m = AcquisitionMode.objects.get(abbreviation=row['SAC_Acquisition_Mode_Abbreviation'].strip(), mission_sensor=data['mission_sensor'])
            print "\tFound\t\t%s: updating..." % m
            # Assign data
            for k in data.keys():
                setattr(m, k, data[k])
            m.save()
        except AcquisitionMode.DoesNotExist:
            print "\tNot found\t%s: creating..." % row['SAC_Sensor_Abbreviation'].strip()
            m = AcquisitionMode(**data)
            m.save()


    if TEST_ONLY:
        # Rollback
        print 'Testing: rolling back...'
        transaction.rollback()
    else:
        # Commit
        print 'Commiting...'
        transaction.commit()

except Exception, e:
    print 'Errors: rolling back...'
    transaction.rollback()
    traceback.print_exc(file=sys.stdout)

finally:
    transaction.leave_transaction_management()
