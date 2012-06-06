# Added by Tim for syncing from informix db
import sys
import informixdb  # import the InformixDB module
# Models and forms for our app
from acscatalogue.models import *
# python logging support to django logging middleware
import logging
# for printing stac traces
import traceback


logging.basicConfig(level=logging.INFO,
    format='%(message)s',
    filename= "/tmp/informix.log",
    filemode='w'
    )


class Informix:

    def __init__(self):
        self.mConnection = informixdb.connect('catalogue@catalog2', user='informix', password='')
        self.mCursor = self.mConnection.cursor(rowformat = informixdb.ROW_AS_DICT)
        self.mHaltOnError = True
        # set informix output format to 4 (WKT)
        myWktSql="update GeoParam set value = 4 where id=3;"
        self.mCursor.execute(myWktSql)
        logging.info("Constructor called")
        return

    def __del__(self):
        # Dont use logging.* in dtor - it truncates the log file deleting all other messages
        print ("Destructor called")
        # set informix output format to 0 (Geodetic / Informix native)
        myWktSql="update GeoParam set value = 0 where id=3;"
        self.mCursor.execute(myWktSql)
        self.mConnection.close()
        return

    def haltOnError(self, theFlag):
        self.mHaltOnError = theFlag

    def runImport(self):
        ''' This method is more intended to be used from
        the manage shell'''
        self.syncSuperclass()
        self.syncDatamode()
        self.syncEllipsoidType()
        self.syncErsCompMode()
        self.syncFileType()
        self.syncHeaderType()
        self.syncSatellite()
        self.syncSensor()
        self.syncSpotAcquisitionMode()
        self.syncStation()
        #
        #  Ok thats the end of the lookup tables, now the real data.
        #  we load them in dependency order so we dont get any
        #  fkey constraint errors.
        #
        self.syncMedium()
        self.syncLocalization()
        self.syncSegment()
        # Must be done after segment and localization
        self.syncFrameCommon()
        self.syncAuxFile()
        self.syncSpotSegment()
        self.syncSpotFrame()
        self.syncLandsatSegment()
        self.syncLandsatFrame()
        self.syncErsFrame()
        self.syncNoaaFrame()
        self.syncOrbviewFrame()
        self.syncOtherFrame()

    def runUpdate(self):
        ''' This method is more intended to be used from
        the manage shell and run to update the database only
        use runImport to do a full import'''
        #
        #  Ok thats the end of the lookup tables, now the real data.
        #  we load them in dependency order so we dont get any
        #  fkey constraint errors.
        #
        self.syncMedium()
        self.syncLocalization()
        self.syncSegment()
        # Must be done after segment and localization
        self.syncFrameCommon()
        self.syncAuxFile()
        self.syncSpotSegment()
        self.syncSpotFrame()
        self.syncLandsatSegment()
        self.syncLandsatFrame()
        self.syncErsFrame()
        self.syncNoaaFrame()
        self.syncOrbviewFrame()
        self.syncOtherFrame()


    def syncDatamode(self):
        # ----------------------------------
        # Sync datamode table
        # ----------------------------------
        self.mCursor.execute('select * from t_data_mode')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = DataMode()
            myObject.original_id = myRow['id']
            myObject.name = myRow['name']
            myObject.save()
        myResult = "DataMode - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult


    def syncEllipsoidType(self):
        # ----------------------------------
        # Sync EllipsoidType table
        # ----------------------------------
        self.mCursor.execute('select * from t_ellipsoid_type')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = EllipsoidType()
            myObject.original_id = myRow['id']
            myObject.description = myRow['description']
            myObject.save()
        myResult = "EllipsoidType - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult


    def syncErsCompMode(self):
        # ----------------------------------
        # Sync ErsCompMode table
        # ----------------------------------
        self.mCursor.execute('select * from t_ers_comp_mode')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = ErsCompMode()
            myObject.original_id = myRow['id']
            myObject.description = myRow['description']
            myObject.save()
        myResult = "ErsCompMode - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult

    def syncFileType(self):
        # ----------------------------------
        # Sync filetype table
        # ----------------------------------
        self.mCursor.execute('select * from t_file_types')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = FileType()
            myObject.original_id = myRow['id']
            myObject.fileTypeName = myRow['file_type_name']
            myObject.save()
        myResult = "FileType - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult

    def syncHeaderType(self):
        # ----------------------------------
        # Sync HeaderType table
        # ----------------------------------
        self.mCursor.execute('select * from t_header_type')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = HeaderType()
            myObject.original_id = myRow['id']
            myObject.name = myRow['name']
            myObject.save()
        myResult = "HeaderType - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult

    def syncSatellite(self):
        # ----------------------------------
        # Sync Satellite table
        # ----------------------------------
        self.mCursor.execute('select * from t_satellites')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = Satellite()
            myObject.original_id = myRow['id']
            myObject.name = myRow['name']
            myObject.save()
        myResult = "Satellte - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult

    def syncSensor(self):
        # ----------------------------------
        # Sync Sensor table
        # ----------------------------------
        self.mCursor.execute('select * from t_sensors')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = Sensor()
            myObject.original_id = myRow['id']
            myObject.name = myRow['name']
            myObject.save()
        myResult = "Satellite - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult

    def syncSpotAcquisitionMode(self):
        # ----------------------------------
        # Sync SpotAcquisitionMode table
        # ----------------------------------
        self.mCursor.execute('select * from t_spot_acq_mode')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = SpotAcquisitionMode()
            myObject.original_id = myRow['id']
            myObject.name = myRow['name']
            myObject.save()
        myResult = "SpotAcquisitionMode - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult


    def syncStation(self):
        # ----------------------------------
        # Sync Station table
        # ----------------------------------
        self.mCursor.execute('select * from t_stations')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = Station()
            myObject.original_id = myRow['id']
            myObject.name = myRow['name']
            myObject.save()
        myResult = "Station - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult

    def syncSuperclass(self):
        # ----------------------------------
        # Sync Superclass table
        # ----------------------------------
        self.mCursor.execute('select * from t_superclasses')
        myCounter = 0
        for myRow in self.mCursor:
            myCounter = myCounter + 1
            myObject = Superclass()
            myObject.original_id = myRow['id']
            myObject.name = myRow['name']
            myObject.save()
        myResult = "Superclasses - OK " + `myCounter` + " Records"
        logging.info(myResult)
        return myResult


    def syncMedium(self):
        # ----------------------------------
        # Sync Medium table
        # ----------------------------------
        myMedium = None
        if Medium.objects.all().count() > 0:
            myMedium = Medium.objects.all().order_by('-original_id')[0]
        if myMedium:
            logging.info("Fetching most recent medium files only!")
            mySQL = 'select * from t_medium where id > ' + str(myMedium.original_id)
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            logging.info("Fetching all medium records!")
            self.mCursor.execute('select * from t_medium')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            myObject = Medium()
            myObject.original_id = myRow['id']
            myObject.medium = myRow['mediumid']
            myObject.mediumType = myRow['medium_type']
            myObject.numOfPasses = myRow['num_of_passes']
            myObject.timeCodeType = myRow['time_code_type']
            myObject.storageStation = myRow['storage_station']
            myObject.mediumLoc = myRow['medium_loc']
            myObject.density = myRow['density']
            myObject.model = myRow['model']
            try:
                myHeaderType = HeaderType.objects.get(original_id=int(myRow['header_type']))
                myObject.headerType = myHeaderType
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myResult = "Medium - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info("Couldnt find a matching header type for : " + str(myRow['header_type']))
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "Medium - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        return myResult

    def syncLocalization(self):
        logging.info("Sync Localization called")
        # ----------------------------------
        # Sync Localization table
        # ----------------------------------
        # set informix output format to 3 (WKT)
        #myWktSql="update GeoParam set value = 4 where id=3;"
        # above query is disabled for now as informix throws
        # a wobbly. Instead you should manually run the above
        # query on the server before initiating this batch job.
        #self.mCursor.execute(myWktSql)
        # Get the localization records
        #self.mCursor.execute('select  FIRST 10 * from t_localization')
        myLocalization = None
        if Localization.objects.all().count() > 0:
            myLocalization = Localization.objects.all().order_by('-original_id')[0]
        if myLocalization:
            logging.info("Fetching most recent localization files only!")
            mySQL = 'select *, Begin(TimeRange(geo_time_info)) as propertimestamp from t_localization where id > ' + str(myLocalization.original_id)
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            logging.info("Fetching all localization records!")
            self.mCursor.execute('select *, Begin(TimeRange(geo_time_info)) as propertimestamp from t_localization')
        myCounter = 0
        myFailureCount = 0
        myFailureMessages = []
        for myRow in self.mCursor:
            myObject = Localization()
            myObject.original_id = myRow['id']
            #if Localization.objects.get(original_id = myRow['id']):
            #  """Dont bother going on since object was previously imported"""
            #  myObject = None
            #  continue
            try:
                myObject.geometry = "SRID=4326;" + myRow['geo_time_info']
            except Exception, exception:
                myFailureMessages.append("<br>" + myRow['geo_time_info'])
                logging.info("Couldnt insert geometry: " + str(myRow['geo_time_info']))
                myResult = "Localization - Failed: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(str(exception))
                logging.info(myResult)
                if self.mHaltOnError:
                    raise SystemExit
                else:
                    continue
            myObject.refreshRate = myRow['refresh_rate']
            myObject.timeStamp = myRow['propertimestamp']
            try:
                mySuperclass = Superclass.objects.get(original_id=int(myRow['object_supertype']))
                myObject.supertype = mySuperclass
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                logging.info("Localization: Couldnt find matching supertype: " + str(myRow['object_supertype']))
                logging.info(str(exception))
                myResult = "Localization - Failed: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                if self.mHaltOnError:
                    raise SystemExit
                else:
                    logging.info("Continuing")
                    continue
            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                logging.info("Localization: Couldnt save record:")
                logging.info("Geometry was: " + str(myRow['geo_time_info']))
                logging.info(str(exception))
                myResult = "Localization - Failed: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                if self.mHaltOnError:
                    raise SystemExit
                else:
                    logging.info("Continuing")
                    continue

            myObject = None
        # set informix output format to 0 (informix native)
        #myInformixSql="update GeoParam set value = 0 where id =3;"
        # above query is disabled for now as informix throws
        # a wobbly. Instead you should manually run the above
        # query on the server after initiating this batch job.
        #self.mCursor.execute(myInformixSql)
        myResult = "Localization - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        for myFailureMessage in myFailureMessages:
            myResult = myResult + myFailureMessage
        logging.info(myResult)
        return myResult


    def syncSegment(self):
        logging.info("Sync Segment Called...")
        # ----------------------------------
        # Sync Segment table
        # ----------------------------------
        # set informix output format to 3 (WKT)
        myWktSql="update GeoParam set value = 4 where id=3;"
        # above query is disabled for now as informix throws
        # a wobbly. Instead you should manually run the above
        # query on the server before initiating this batch job.
        # self.mCursor.execute(myWktSql)
        # Get the localization records
        mySegmentCommon = None
        if SegmentCommon.objects.all().count() > 0:
            mySegmentCommon = SegmentCommon.objects.all().order_by('-original_id')[0]
            print "Syncing all segment objects greater than original_id of " + str(mySegmentCommon.original_id)
        if mySegmentCommon:
            logging.info("Fetching most recent segment_common files only!")
            mySQL = 'select *, Begin(TimeRange(geo_shape)) as propertimestamp from t_segment_common where id > ' + str(mySegmentCommon.original_id)
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            logging.info("Fetching all segments!")
            self.mCursor.execute('select *, Begin(TimeRange(geo_shape)) as propertimestamp from t_segment_common')
        myCounter = 0
        myFailureCount = 0
        myFailureMessages = []
        for myRow in self.mCursor:
            myObject = SegmentCommon()
            myObject.original_id = myRow['id']
            #if SegmentCommon.objects.get(original_id = myRow['id']):
            #  """Dont bother going on since object was previously imported"""
            #  myObject = None
            #  continue
            try:
                mySatellite = Satellite.objects.get(original_id=int(myRow['satellite_id']))
                myObject.satellite = mySatellite
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                myFailureMessages.append("<br> For satellite : " + str(myRow['satellite_id']))
                if self.mHaltOnError:
                    raise SystemExit
            myObject.mission = int(myRow['mission'])
            try:
                mySensor = Sensor.objects.get(original_id=int(myRow['sensor_id']))
                myObject.sensor = mySensor
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                myFailureMessages.append("<br> For sensor: " + str(myRow['sensor_id']))
                if self.mHaltOnError:
                    raise SystemExit
            try:
                myMedium = Medium.objects.get(original_id=int(myRow['medium_id']))
                myObject.medium = myMedium
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                myFailureMessages.append("<br> For medium: " + str(myRow['medium_id']))
                if self.mHaltOnError:
                    raise SystemExit
            myObject.ascendingFlag
            myObject.geometry = "SRID=4326;" + myRow['geo_shape']
            try:
                myStation = Station.objects.get(original_id=int(myRow['station_id']))
                myObject.station = myStation
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                myFailureMessages.append("<br> For station: " + str(myRow['station_id']))
                logging.info("Couldnt insert geometry: " + str(myRow['geo_time_info']))
                logging.info(myResult)
                logging.info(str(exception))
                myResult = "Localization - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                if self.mHaltOnError:
                    raise SystemExit
                else:
                    continue
            myObject.insertionDate = informixdb.TimestampFromTicks(myRow['insertion_date'])
            myObject.begRecordDate = informixdb.TimestampFromTicks(myRow['beg_record_date'])
            myObject.endRecordDate = informixdb.TimestampFromTicks(myRow['end_record_date'])
            #myFailureMessages.append("Insertion Date: " + str(myObject.insertionDate) + "<br/>")
            #myFailureMessages.append("Begin Date: " + str(myObject.begRecordDate) + "<br/>")
            #myFailureMessages.append("End Date: " + str(myObject.endRecordDate) + "<br/>")
            myObject.orbit = myRow['orbit']
            myObject.cycle = myRow['cycle']
            myObject.iLatMin = myRow['i_lat_min']
            myObject.iLonMin = myRow['i_lon_min']
            myObject.iLatMax = myRow['i_lat_max']
            myObject.iLonMax = myRow['i_lon_max']
            myObject.firstAddress = myRow['first_address']
            myObject.secondAddress = myRow['second_address']
            myObject.displayedTrack = myRow['displayed_track']
            myObject.displayedOrbit = myRow['displayed_orbit']
            myObject.displayedMedium = myRow['displayed_medium']
            myObject.npass = myRow['npass']
            myObject.timeStamp = myRow['propertimestamp']
            #myFailureMessages.append("Time Stamp: " + str(myObject.timeStamp) + "<br/>")
            myObject.startBlock = myRow['start_block']
            myObject.endBlock = myRow['end_block']
            myObject.startFeet = myRow['start_feet']
            myObject.endFeet = myRow['end_feet']
            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                #myFailureMessages.append("<br>" + str(informixdb.TimestampFromTicks(myRow['insertion_date'])))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        # set informix output format to 0 (informix native)
        myInformixSql="update GeoParam set value = 0 where id =3;"
        # above query is disabled for now as informix throws
        # a wobbly. Instead you should manually run the above
        # query on the server after initiating this batch job.
        #self.mCursor.execute(myInformixSql)
        mySegmentCommon = SegmentCommon.objects.all().order_by('-original_id')[0]
        print "Synced all segment objects new greatest original_id of " + str(mySegmentCommon.original_id)
        myResult = "SegmentCommon - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        for myFailureMessage in myFailureMessages:
            myResult = myResult + myFailureMessage
        logging.info(myResult)
        return myResult



    def syncFrameCommon(self):
        logging.info("Sync Frame Common called")
        """
        Sync frame common table

        This must be done *after* segment and localisation tables
        are populated since it makes fkey references to both of these

        Table model as it exists on informix:

        Column name          Type                                    Nulls

        localization_id      integer                                 no
        segment_id           integer                                 no
        cloud                nchar(8)                                no
        cloud_mean           smallint                                no
        track_orbit          smallint                                no
        frame                smallint                                no
        ordinal              smallint                                no
        ll_lat               smallfloat                              no
        ur_lon               smallfloat                              no
        ur_lat               smallfloat                              no
        ul_lon               smallfloat                              no
        ul_lat               smallfloat                              no
        ll_lon               smallfloat                              no
        lr_lat               smallfloat                              no
        lr_lon               smallfloat                              no
        processable          boolean                                 no
        begin_time_cod       float                                   no
        end_time_cod         float                                   no

        Note that the framecommon has no primary key - it is a join table
        between localization and segment.
        """

        try:
            # As you can see from the above listing, framecommon on the original
            # informix db has no primary key based on a sequence so we have
            # a problem if we only want to update newly added records rather than
            # syncing the whole table.

            # I also tried adding a unique constraint on segment and localization ids
            # on the framecommon but that doesnt work because even those paired arent
            # guaranteed to be unique.

            # So instead we do this:
            # Find the greatest segement and localization id's on the framecommon table
            # and then import everything >= those. We use >= to ensure that we dont miss
            # frames that were half way loaded during the update.
            myMaxSegment = None
            myMaxLocalization = None
            myFrame = None
            myFrameCount = FrameCommon.objects.all().count()
            if myFrameCount > 0:
                myFrame = FrameCommon.objects.all().order_by('-segment')[0]
                print "Syncing all framecommon objects before count " + str( myFrameCount )
                mySegment = myFrame.segment
                myMaxSegment = mySegment.original_id
                myMaxLocalization = FrameCommon.objects.all().order_by('localization')[0].localization.original_id
                logging.info("syncFrameCommon using maxSegment: " + str(myMaxSegment) +
                  " and maxLocalization " + str(myMaxLocalization))

            if myMaxLocalization and myMaxSegment:
                logging.info("Fetching most recent frame_common files only!")
                mySQL = '''select * from t_frame_common where segment_id >= ''' + str(myMaxSegment) + ''' and localization_id >= ''' + str(myMaxLocalization) + ''';'''
                logging.info(mySQL)
                self.mCursor.execute(mySQL)
            else:
                logging.info("Fetching all frames!")
                self.mCursor.execute('select * from t_frame_common')
        except Exception, exception:
            logging.info("FrameCommon cursor failed to initialise")
            traceback.print_exc()
            logging.info(str(exception))
            if self.mHaltOnError:
                raise SystemExit
            else:
                return
        myCounter = 0
        myFailureCount = 0
        myFailureMessages = []
        for myRow in self.mCursor:
            myObject = FrameCommon()
            try:
                mySegment = SegmentCommon.objects.get(original_id=int(myRow['segment_id']))
                myObject.segment = mySegment
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                if self.mHaltOnError:
                    logging.info('Failure Count - segment mapping error ' + str(myRow['segment_id']) + " does not exist")
                    logging.info(str(exception))
                    raise SystemExit
                else:
                    continue
            try:
                #logging.info("Setting localization id: " + str(myRow['localization_id']))
                myLocalization = Localization.objects.get(original_id=int(myRow['localization_id']))
                #logging.info("Retrieved localization object: " + str(myLocalizationId))
                myObject.localization = myLocalization
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                myFailureMessages.append("<br> For frame common finding matching localization failed for localization: " + str(myRow['localization_id']))
                if self.mHaltOnError:
                    logging.info('Failure Count - localization mapping error ' + str(myRow['localization_id']) + " does not exist")
                    logging.info(str(exception))
                    raise SystemExit
                else:
                    continue

            try:
                myObject.cloud       = myRow['cloud']
                myObject.cloudMean   = myRow['cloud_mean']
                myObject.trackOrbit  = myRow['track_orbit']
                myObject.frame       = myRow['frame']
                myObject.ordinal     = myRow['ordinal']
                myObject.llLat       = myRow['ll_lat']
                myObject.urLon       = myRow['ur_lon']
                myObject.urLat       = myRow['ur_lat']
                myObject.ulLon       = myRow['ul_lon']
                myObject.ulLat       = myRow['ul_lat']
                myObject.llLon       = myRow['ll_lon']
                myObject.lrLat       = myRow['lr_lat']
                myObject.lrLon       = myRow['lr_lon']
                myObject.processable = myRow['processable']
                myObject.beginTimeCod = myRow['begin_time_cod']
                myObject.endTimeCod   = myRow['end_time_cod']
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                if self.mHaltOnError:
                    logging.info('Failure Count ' + str(myFailureCount))
                    logging.info(str(exception))
                    raise SystemExit
            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myFailureMessages.append("<br>" + str(exception))
                if self.mHaltOnError:
                    logging.info('Failure Count ' + str(myFailureCount))
                    logging.info(str(exception))
                    raise SystemExit
            myObject = None
        myFrameCount = FrameCommon.objects.all().count()
        print "Synced all framecommon objects new count " + str( myFrameCount )
        myResult = "FrameCommon - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        for myFailureMessage in myFailureMessages:
            myResult = myResult + myFailureMessage
        logging.info(myResult)
        return myResult


    def syncAuxFile(self):
        # ----------------------------------
        # Sync AuxFile table
        # ----------------------------------
        # Get the aux_file records
        myAuxFile = None
        if AuxFile.objects.all().count() > 0:
            myAuxFile = AuxFile.objects.all().order_by('-original_id')[0]
            print "Syncing all aux file objects greater than original_id of " + str(myAuxFile.original_id)
        if myAuxFile:
            logging.info("Fetching most recent aux files only!")
            mySQL = 'select * from t_aux_files where id > ' + str(myAuxFile.original_id)
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print "Syncing all aux file objects "
            logging.info("Fetching all aux files!")
            self.mCursor.execute('select * from t_aux_files')
        myCounter = 0
        myFailureCount = 0
        myFailureMessages = []
        for myRow in self.mCursor:
            myObject = AuxFile()
            myObject.original_id = myRow['id']
            #if AuxFile.objects.get(original_id = myRow['id']):
            #  """Dont bother going on since object was previously imported"""
            #  myObject = None
            #  continue
            try:
                mySegment = SegmentCommon.objects.get(original_id=int(myRow['common_id']))
                myObject.segmentCommon = mySegment
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
                else:
                    continue
            try:
                myFileType = FileType.objects.get(original_id=int(myRow['file_type']))
                myObject.fileType = myFileType
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
                else:
                    continue
            myObject.original_id = myRow['id']
            myObject.superType = myRow['object_supertype']
            myObject.fileName = myRow['file_name']
            myObject.fileDescription = myRow['file_description']
            myObject.insertionDate = myRow['insertion_date']
            myObject.visible = myRow['visible']
            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                if self.mHaltOnError:
                    logging.info(str(exception))
                    raise SystemExit
            myObject = None
        myAuxFile = AuxFile.objects.all().order_by('-original_id')[0]
        print "New latest aux file object has original_id of " + str(myAuxFile.original_id)
        myResult = "AuxFile - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        for myFailureMessage in myFailureMessages:
            myResult = myResult + myFailureMessage
        logging.info(myResult)
        return myResult

    def syncSpotSegment(self):
        # ----------------------------------
        # Sync SpotAcquisitionMode table
        # ----------------------------------
        mySpotSegment = None
        myLatestOriginalId = 0
        if SpotSegment.objects.all().count() > 0:
            mySpotSegment = SpotSegment.objects.all().order_by('-original_id')[0]
        if mySpotSegment:
            myLatestOriginalId = mySpotSegment.original_id
            print("Fetching most recent spot segments only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent spot segments only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_spot_segment where segment_common_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all spot segment records!")
            logging.info("Fetching all spot segment records!")
            self.mCursor.execute('select * from t_spot_segment')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            mySegment = None
            myObject = SpotSegment()
            myObject.original_id = myRow['segment_common_id']
            myLatestOriginalId = myRow['segment_common_id']
            try:
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            myObject.segmentNumber = myRow['segment_number']
            myObject.hrvNumber = myRow['hrv_num']
            myObject.mode = myRow['mode']
            myObject.channel = myRow['channel']
            myObject.gain = myRow['gain']
            myObject.begTimeCode = myRow['beg_time_cod']
            myObject.endTimeCode = myRow['end_time_cod']
            myObject.endFormat = myRow['end_format']
            myObject.qualityFactor = myRow['quality_factor']
            myObject.lookingAngle = myRow['looking_angle']
            myObject.firstValidFc = myRow['first_valid_fc']
            myObject.lastValidFc = myRow['last_valid_fc']
            myObject.missingLinesFlag  = myRow['missing_lines_flag']
            myObject.hrvConf = myRow['hrv_conf']
            myObject.mirrorStep = myRow['mirror_step']
            myObject.triodeQfactor = myRow['triode_qfactor']

            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                print myRow
                traceback.print_exc()
                myFailureCount = myFailureCount + 1
                myResult = "SpotSegment - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "SpotSegment - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest spotsegment object has original_id of " + str( myLatestOriginalId )
        return myResult

    def syncSpotFrame(self):
        # ----------------------------------
        # Sync SpotFrame table
        # NOTE: localization_id is the primary key for the spot frame table
        # ----------------------------------
        mySpotFrame = None
        myLatestOriginalId = 0
        if SpotFrame.objects.all().count() > 0:
            mySpotFrame = SpotFrame.objects.all().order_by('-original_id')[0]
        if mySpotFrame:
            myLatestOriginalId = mySpotFrame.original_id
            print("Fetching most recent spot frames only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent spot frames only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_spot_frame where localization_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all spot frame records!")
            logging.info("Fetching all spot frame records!")
            self.mCursor.execute('select * from t_spot_frame')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            myLocalization = None
            mySegment = None
            myObject = SpotFrame()
            # NOTE: localization_id is the primary key for the spot frame table
            myObject.original_id = myRow['localization_id']
            myLatestOriginalId = myRow['localization_id']
            try:
                myObject.localization = Localization.objects.get(original_id=int(myRow['localization_id']))
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            myObject.begFormat = 0 # myRow['beg_format']
            myObject.endFormat = myRow['end_format']
            myObject.firstValidFc = myRow['first_valid_fc']
            myObject.lastValidFc = myRow['last_valid_fc']
            myObject.dummySceneFlag = myRow['dummy_scene_flag']
            myObject.missLines = myRow['miss_lines']
            myObject.satMinVal = myRow['sat_min_val']
            myObject.satMaxVal = myRow['sat_max_val']
            myObject.centerTimeCod = myRow['center_time_cod']
            myObject.scLat = myRow['sc_lat']
            myObject.scLon = myRow['sc_lon']
            myObject.scDevLat = myRow['sc_dev_lat']
            myObject.scDevLon = myRow['sc_dev_lon']
            myObject.incidence = myRow['incidence']
            myObject.orientation = myRow['orientation']
            myObject.sunAz =  myRow['sun_az']
            myObject.sunEl = myRow['sun_el']

            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                print myRow
                myFailureCount = myFailureCount + 1
                myResult = "SpotFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "SpotFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest spotframe object has original_id of " + str( myLatestOriginalId )
        return myResult

    def syncLandsatSegment(self):
        # ----------------------------------
        # Sync LandsatSegment table
        # segment_common_id is the pkey for this table
        # ----------------------------------
        myLandsatSegment = None
        myLatestOriginalId = 0
        if LandsatSegment.objects.all().count() > 0:
            myLandsatSegment = LandsatSegment.objects.all().order_by('-original_id')[0]
        if myLandsatSegment:
            myLatestOriginalId = myLandsatSegment.original_id
            print("Fetching most recent landsat segments only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent landsat segments only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_landsat_segment where segment_common_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all landsat segment records!")
            logging.info("Fetching all landsat segment records!")
            self.mCursor.execute('select * from t_landsat_segment')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            mySegment = None
            myObject = LandsatSegment()
            # NOTE: localization_id is the primary key for the landsat frame table
            myObject.original_id = myRow['segment_common_id']
            myLatestOriginalId = myRow['segment_common_id']
            try:
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            myObject.segmentOrder = myRow['segment_order']
            myObject.begTimeCode = myRow['beg_time_cod']
            myObject.endTimeCode = myRow['end_time_cod']
            myObject.firstFrameFc = myRow['first_frame_fc']
            myObject.lastFrameFc = myRow['last_frame_fc']
            myObject.ellipsoid = myRow['ellipsoid']
            myObject.ellipsParam1 = myRow['ellips_param1']
            myObject.ellipsParam2 = myRow['ellips_param2']
            myObject.ellipsParam3 = myRow['ellips_param3']
            myObject.ellipsParam4 = myRow['ellips_param4']
            myObject.channel = myRow['channel']
            if myRow['metaversionno']:
                myObject.metaVersionNo = int( myRow['metaversionno'] )
            else:
                myObject.metaVersionNo = 0
            myObject.bandpresent = myRow['bandpresent']

            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myResult = "LandsatSegment - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    print myResult
                    traceback.print_exc()
                    raise SystemExit
            myObject = None
        myResult = "LandsatSegment - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest landsatsegment object has original_id of " + str( myLatestOriginalId )
        return myResult


    def syncLandsatFrame(self):
        # ----------------------------------
        # Sync LandsatFrame table
        # NOTE: localization_id is the primary key for the landsat frame table
        # ----------------------------------
        myLandsatFrame = None
        myLatestOriginalId = 0
        if LandsatFrame.objects.all().count() > 0:
            myLandsatFrame = LandsatFrame.objects.all().order_by('-original_id')[0]
        if myLandsatFrame:
            myLatestOriginalId = myLandsatFrame.original_id
            print("Fetching most recent landsat frames only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent landsat frames only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_landsat_frame where localization_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all landsat frame records!")
            logging.info("Fetching all landsat frame records!")
            self.mCursor.execute('select * from t_landsat_frame')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            myLocalization = None
            mySegment = None
            myObject = LandsatFrame()
            # NOTE: localization_id is the primary key for the landsat frame table
            myObject.original_id = myRow['localization_id']
            myLatestOriginalId = myRow['localization_id']
            try:
                myObject.localization = Localization.objects.get(original_id=int(myRow['localization_id']))
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            myObject.centreLat = myRow['centre_lat']
            myObject.centreLon = myRow['centre_lon']
            myObject.centreTime = myRow['centre_time']
            myObject.sunAz = myRow['sun_az']
            myObject.sunElev = myRow['sun_elev']
            myObject.fopScene = myRow['fop_scene']
            myObject.hdShift = myRow['hd_shift']
            myObject.sQuality = myRow['s_quality']
            myObject.sbPresent = myRow['sb_present']
            myObject.bGain = myRow['b_gain']
            myObject.bgChange = myRow['bg_change']
            myObject.bslgainchange = myRow['bslgainchange']

            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myResult = "LandsatFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "LandsatFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest landsatframe object has original_id of " + str( myLatestOriginalId )
        return myResult

    def syncErsFrame(self):
        # ----------------------------------
        # Sync ErsFrame table
        # NOTE: localization_id is the primary key for the ers frame table
        # ----------------------------------
        myErsFrame = None
        myLatestOriginalId = 0
        if ErsFrame.objects.all().count() > 0:
            myErsFrame = ErsFrame.objects.all().order_by('-original_id')[0]
        if myErsFrame:
            myLatestOriginalId = myErsFrame.original_id
            print("Fetching most recent ers frames only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent ers frames only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_ers_frame where localization_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all ers frame records!")
            logging.info("Fetching all ers frame records!")
            self.mCursor.execute('select * from t_ers_frame')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            myLocalization = None
            mySegment = None
            myObject = ErsFrame()
            # NOTE: localization_id is the primary key for the ers frame table
            myObject.original_id = myRow['localization_id']
            myLatestOriginalId = myRow['localization_id']
            try:
                myObject.localization = Localization.objects.get(original_id=int(myRow['localization_id']))
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            myObject.frame = myRow['frame']
            myObject.meanI = myRow['mean_i']
            myObject.meanQ = myRow['mean_q']
            myObject.sdevI = myRow['sdev_i']
            myObject.sdevQ = myRow['sdev_q']
            myObject.missLinPerc = myRow['miss_lin_perc']
            myObject.dopplerCentroid = myRow['doppler_centroid']
            myObject.blockNumber = myRow['block_number']
            myObject.lineNumber = myRow['line_number']
            myObject.maxI = myRow['max_i']
            myObject.maxQ = myRow['max_q']

            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myResult = "ErsFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "ErsFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest ersframe object has original_id of " + str( myLatestOriginalId )
        return myResult

    def syncNoaaFrame(self):
        # ----------------------------------
        # Sync NoaaFrame table
        # NOTE: localization_id is the primary key for the noaa frame table
        # ----------------------------------
        myNoaaFrame = None
        myLatestOriginalId = 0
        if NoaaFrame.objects.all().count() > 0:
            myNoaaFrame = NoaaFrame.objects.all().order_by('-original_id')[0]
        if myNoaaFrame:
            myLatestOriginalId = myNoaaFrame.original_id
            print("Fetching most recent noaa frames only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent noaa frames only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_noaa_frame where localization_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all noaa frame records!")
            logging.info("Fetching all noaa frame records!")
            self.mCursor.execute('select * from t_noaa_frame')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            myLocalization = None
            mySegment = None
            myObject = NoaaFrame()
            # NOTE: localization_id is the primary key for the noaa frame table
            myObject.original_id = myRow['localization_id']
            myLatestOriginalId = myRow['localization_id']
            try:
                myObject.localization = Localization.objects.get(original_id=int(myRow['localization_id']))
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            # no other props for this frame table...
            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myResult = "NoaaFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "NoaaFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest noaaframe object has original_id of " + str( myLatestOriginalId )
        return myResult

    def syncOrbviewFrame(self):
        # ----------------------------------
        # Sync OrbviewFrame table
        # NOTE: localization_id is the primary key for the orbview frame table
        # ----------------------------------
        myOrbviewFrame = None
        myLatestOriginalId = 0
        if OrbviewFrame.objects.all().count() > 0:
            myOrbviewFrame = OrbviewFrame.objects.all().order_by('-original_id')[0]
        if myOrbviewFrame:
            myLatestOriginalId = myOrbviewFrame.original_id
            print("Fetching most recent orbview frames only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent orbview frames only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_orbview_frame where localization_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all orbview frame records!")
            logging.info("Fetching all orbview frame records!")
            self.mCursor.execute('select * from t_orbview_frame')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            myLocalization = None
            mySegment = None
            myObject = OrbviewFrame()
            # NOTE: localization_id is the primary key for the orbview frame table
            myObject.original_id = myRow['localization_id']
            myLatestOriginalId = myRow['localization_id']
            try:
                myObject.localization = Localization.objects.get(original_id=int(myRow['localization_id']))
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            # no other props for this frame table...
            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myResult = "OrbviewFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "OrbviewFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest orbviewframe object has original_id of " + str( myLatestOriginalId )
        return myResult

    def syncOtherFrame(self):
        # ----------------------------------
        # Sync OtherFrame table
        # NOTE: localization_id is the primary key for the other frame table
        # ----------------------------------
        myOtherFrame = None
        myLatestOriginalId = 0
        if OtherFrame.objects.all().count() > 0:
            myOtherFrame = OtherFrame.objects.all().order_by('-original_id')[0]
        if myOtherFrame:
            myLatestOriginalId = myOtherFrame.original_id
            print("Fetching most recent other frames only (> %s)!" % myLatestOriginalId)
            logging.info("Fetching most recent other frames only (> %s)!" % myLatestOriginalId)
            mySQL = 'select * from t_other_frame where localization_id > %s' % myLatestOriginalId
            logging.info(mySQL)
            self.mCursor.execute(mySQL)
        else:
            print("Fetching all other frame records!")
            logging.info("Fetching all other frame records!")
            self.mCursor.execute('select * from t_other_frame')
        myCounter = 0
        myFailureCount = 0
        for myRow in self.mCursor:
            myLocalization = None
            mySegment = None
            myObject = OtherFrame()
            # NOTE: localization_id is the primary key for the other frame table
            myObject.original_id = myRow['localization_id']
            myLatestOriginalId = myRow['localization_id']
            try:
                myObject.localization = Localization.objects.get(original_id=int(myRow['localization_id']))
                myObject.segmentCommon = SegmentCommon.objects.get(original_id=int(myRow['segment_common_id']))
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                continue
            myObject.dataMode = myRow['data_mode']
            myObject.eqCrxTime = myRow['eqcrx_time']
            myObject.eqLon = myRow['eq_lon']
            myObject.procLevel = myRow['proc_level']
            myObject.bandNumber = myRow['band_number']
            myObject.pixFormat = myRow['pix_format']
            try:
                myObject.save()
                myCounter = myCounter + 1
            except Exception, exception:
                myFailureCount = myFailureCount + 1
                myResult = "OtherFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
                logging.info(myResult)
                logging.info(str(exception))
                if self.mHaltOnError:
                    raise SystemExit
            myObject = None
        myResult = "OtherFrame - OK: " + `myCounter` + " Records, Failed:" + `myFailureCount` + " Records."
        logging.info(myResult)
        print "New latest otherframe object has original_id of " + str( myLatestOriginalId )
        return myResult
