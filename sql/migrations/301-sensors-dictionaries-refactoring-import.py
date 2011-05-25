"""

Can be run from project dir with
$ python manage.py runscript -s -v 2 --pythonpath=./sql/migrations 201-sensors-dictionaries-refactoring-import.py

CSV files are in "sql/migrations/dictionaries_v5" folder

"""

TEST_ONLY=False
ABORT_ON_EXTRA_VALUES=False
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
        if ABORT_ON_EXTRA_VALUES:
            raise Exception, 'Mission contains extra values.'
        else:
            print '[WARNING] Mission contains extra values.'

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
        if ABORT_ON_EXTRA_VALUES:
            raise Exception, 'MissionSensor contains extra values.'
        else:
            print '[WARNING] MissionSensor contains extra values.'

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
            m = MissionSensor.objects.get(abbreviation=row['SAC_Sensor_Abbreviation'].strip(), operator_abbreviation__isnull=True)
            # Assign data
            for k in data.keys():
                setattr(m, k, data[k])
            m.save()
            print "\tFound\t\t%s:%s: updating..." % (m.abbreviation, m.operator_abbreviation)
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
        #print 'Retrieving %s:%s' % (m['Sensor_Abbreviation'].strip(),m['SAC_Sensor_Abbreviation'].strip())
        #import ipy; ipy.shell()
        ms = MissionSensor.objects.get(operator_abbreviation=m['Sensor_Abbreviation'].strip(), abbreviation=m['SAC_Sensor_Abbreviation'].strip())
        obj_keys.append("%s:%s" % (m['SAC_Sensor_Type_Abbreviation'].strip(), ms.operator_abbreviation))

    #import ipy; ipy.shell()

    # Check that the DB does not contain any additional entry, abort if yes
    obj_extra = []
    for st in SensorType.objects.all():
        if not "%s:%s" % (st.abbreviation, st.mission_sensor.operator_abbreviation) in obj_keys:
            obj_extra.append(st)

    #import ipy; ipy.shell()
    if len(obj_extra):
        for m in obj_extra:
            print 'Extra SensorType: %s:%s' % (m.abbreviation, m.mission_sensor.operator_abbreviation)
        if ABORT_ON_EXTRA_VALUES:
            raise Exception, 'SensorType contains extra values.'
        else:
            print '[WARNING] SensorType contains extra values.'

    for row in obj:
        # Map fields
        data = {
            'abbreviation' : row['SAC_Sensor_Type_Abbreviation'].strip(),
            'operator_abbreviation' : row['Sensor_Type_Abbreviation'].strip(),
            'name' : row['Type_Name'].strip(),
            # Following commented fields are not in the schema (they currently belong to AcquisitionMode)
            #'geometric_resolution' : int(row['Resolution']),
            #'band_count' : int(row['Bands']),
            'mission_sensor' : MissionSensor.objects.get(operator_abbreviation=row['Sensor_Abbreviation'].strip(), abbreviation=row['SAC_Sensor_Abbreviation'].strip()),
        }
        # Check if already in DB
        try:
            m = SensorType.objects.get(abbreviation=row['SAC_Sensor_Type_Abbreviation'].strip(), mission_sensor=data['mission_sensor'], operator_abbreviation__isnull=True)
            print "\tFound\t\t%s:%s: updating..." % (row['SAC_Sensor_Type_Abbreviation'].strip(), data['mission_sensor'])
            # Assign data
            for k in data.keys():
                setattr(m, k, data[k])
            m.save()
        except SensorType.DoesNotExist:
            print "\tNot found\t%s:%s: creating..." % (row['SAC_Sensor_Type_Abbreviation'].strip(), data['mission_sensor'])
            m = SensorType(**data)
            m.save()

    #################################
    #
    # AcquisitionMode
    #
    # Note: there is no way to map from AcquisitionMode to SensorType in the spreadsheet
    #       the approach is only to upadte existing records.
    #
    #################################
    print '-' * 40
    print "Importing AcquisitionMode objects..."
    print '-' * 40
    obj = {}
    for m in csv.DictReader(open(CSV_FOLDER + '/AcquisitionMode.csv'), delimiter='\t', quotechar='"'):
        obj["%s:%s" % (m['SAC_Acquisition_Mode_Abbreviation'].strip(),  m['Sensor_Abbreviation'].strip())] = m

    imported = []
    for row in AcquisitionMode.objects.all():
        key = "%s:%s" % (row.abbreviation, row.sensor_type.mission_sensor.operator_abbreviation)
        # Check if already in DB
        try:
            m = obj[key]
            print "\tFound\t\t%s: updating..." % m['Acquisition_Mode_Abbreviation'].strip()
            # Assign data
            row.operator_abbreviation = m['Acquisition_Mode_Abbreviation'].strip()
            row.name = m['Acquisition_Mode_Name'].strip()
            row.save()
        except KeyError:
            print "\tNot found\t%s: skipping..." % key


    #################################
    #
    # ProcessingLevel
    #
    # Note:
    #     * many fields are missing in the DB and hence ignored
    #     * there seems to be a relation with MissionSensor (which does not exists in the DB)
    #       this leads to many duplicated rows that are just skipped
    #
    #################################
    print '-' * 40
    print "Importing ProcessingLevel objects..."
    print '-' * 40
    obj = []
    obj_keys = []
    for m in csv.DictReader(open(CSV_FOLDER + '/ProcessingLevel.csv'), delimiter='\t', quotechar='"'):
        obj.append(m)
        obj_keys.append(m['SAC_Processing_Level_Abbreviation'].strip())

    # Check that the DB does not contain any additional entry, abort if yes
    obj_extra = []
    for st in ProcessingLevel.objects.all():
        if not st.abbreviation in obj_keys:
            obj_extra.append(st)
    #import ipy; ipy.shell()
    if len(obj_extra):
        for m in obj_extra:
            print 'Extra ProcessingLevel: %s' % m
        if ABORT_ON_EXTRA_VALUES:
            raise Exception, 'ProcessingLevel contains extra values.'
        else:
            print '[WARNING] ProcessingLevel contains extra values.'

    for row in obj:
        # Map fields
        name = row['Processing_Level_Name'].strip()
        if len(name) > 255:
            print '[WARNING] level %s longer than 255 chars, truncated.' % row['SAC_Processing_Level_Abbreviation'].strip()
            name = name[:255]
            #print name
        data = {
            'abbreviation' : row['SAC_Processing_Level_Abbreviation'].strip(),
            'name' : name,
        }
        # Check if already in DB
        if row['SAC_Processing_Level_Abbreviation'].strip() in imported:
            print '[WARNING] ProcessingLevel %s abbreviation was already processed, skipping.' % row['SAC_Processing_Level_Abbreviation']
            continue
        imported.append(row['SAC_Processing_Level_Abbreviation'].strip())
        try:
            m = ProcessingLevel.objects.get(abbreviation=row['SAC_Processing_Level_Abbreviation'].strip())
            print "\tFound\t\t%s: updating..." % m.abbreviation
            # Assign data
            for k in data.keys():
                setattr(m, k, data[k])
            m.save()

        except ProcessingLevel.DoesNotExist:
            if len(row['SAC_Processing_Level_Abbreviation'].strip()) > 4:
                print '[WARNING] ProcessingLevel %s abbreviation longer than 4 chars, skipping.' % row['SAC_Processing_Level_Abbreviation']
                continue
            print "\tNot found\t%s: creating..." % row['SAC_Processing_Level_Abbreviation'].strip()
            m = ProcessingLevel(**data)
            m.save()




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
