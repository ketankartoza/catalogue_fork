import os
from optparse import make_option
import tempfile
import subprocess
from mercurial import lock, error

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.geometries import Polygon

from catalogue.models import *
from catalogue.dims_lib import dimsWriter
import traceback
from catalogue.informix import Informix


class Command(BaseCommand):
    """
    Tool for harvesting data from the legacy acs catalogue
    This is a base class - you should overload it for
    each mission that you want to support.
    """

    help = "Imports ACS Landsat records into the SAC catalogue"
    option_list = BaseCommand.option_list + (
        make_option('--download-thumbs', '-d', dest='download_thumbs', action='store',
            help='Whether thumbnails should be fetched too. If not fetched now they will be fetched on demand as needed.', default=False),
        make_option('--start-record', '-b', dest='start_record', action='store',
            help='Start record id to use for import. If none is specified, the last record in the catalogue will be used.', default=None),
        make_option('--max-records', '-m', dest='max_records', action='store',
            help='Maximum number of records to import. If none is specified, a default of 1000 will be used.', default=1000),
        make_option('--test_only', '-t', dest='test_only', action='store_true',
            help='Just test, nothing will be written into the DB.', default=False),
        make_option('--owner', '-o', dest='owner', action='store',
            help='Name of the Institution package owner. Defaults to: Rapideye AG.', default='Rapideye AG'),
        make_option('--creating_software', '-s', dest='creating_software', action='store',
            help='Name of the creating software. Defaults to: Unknown.', default='Unknown'),
        make_option('--license', '-l', dest='license', action='store', default='SAC Commercial License',
            help='Name of the license. Defaults to: SAC Commercial License'),
        make_option('--area', '-a', dest='area', action='store',
            help='Area of interest, images which are external to this area will not be imported (WKT Polygon, SRID=4326)'),
        make_option('--quality', '-q', dest='quality', action='store',
            help='Quality code (will be created if does not exists). Defaults to: Unknown', default='Unknown'),
        make_option('--processing_level', '-r', dest='processing_level', action='store',
            help='Processing level code (will be created if does not exists). Defaults to: 1B', default='1B'),
        make_option('--halt-on-error', '-e', dest='halt_on_error', action='store',
            help='Halt on first error that occurs and print a stacktrace', default=False),
    )
    informix = Informix()


    @transaction.commit_manually
    def handle(self, *args, **options):
        """ command execution """
        def verblog(msg, level=1):
            if verbose >= level:
                print msg

        try:
            lockfile = lock.lock("/tmp/acs_landsat_harvest.lock", timeout=60)
        except error.LockHeld:
            # couldn't take the lock
            raise CommandError, 'Could not acquire lock.'

        download_thumbs       = options.get('download_thumbs')
        start_record          = options.get('start_record')
        max_records           = options.get('max_records')
        test_only             = options.get('test_only')
        verbose               = int(options.get('verbosity'))
        license               = options.get('license')
        owner                 = options.get('owner')
        software              = options.get('creating_software')
        area                  = options.get('area')
        quality               = options.get('quality')
        processing_level      = options.get('processing_level')
        halt_on_error         = options.get('halt_on_error')

        area_of_interest  = None


        verblog('Getting verbose (level=%s)... ' % verbose, 2)
        if test_only:
            verblog('Testing mode activated.', 2)
        verblog( "Max records: %s" % str(max_records), 2 )
        verblog( "Halt on error: %s" % str(halt_on_error), 2 )

        try:
            # Validate area_of_interest
            if area:
                try:
                    area_of_interest = Polygon(area)
                    if not area_of_interest.area:
                        raise CommandError('Unable to create the area of interest polygon: invalid polygon.')
                    if not area_of_interest.geom_type.name == 'Polygon':
                        raise CommandError('Unable to create the area of interest polygon: not a polygon.')
                except Exception, e:
                    raise CommandError('Unable to create the area of interest polygon: %s.' % e)
                verblog('Area of interest filtering activated.', 2)

            # Get the params
            try:
                software = CreatingSoftware.objects.get_or_create(name=software, defaults={'version': 0})[0]
            except CreatingSoftware.DoesNotExist:
                raise CommandError, 'Creating Software %s does not exists and cannot create: aborting' % software
            try:
                license = License.objects.get_or_create(name=license, defaults={'type': License.LICENSE_TYPE_COMMERCIAL, 'details': license})[0]
            except License.DoesNotExist:
                raise CommandError, 'License %s does not exists and cannot create: aborting' % license

            try:
                owner = Institution.objects.get_or_create(name=owner, defaults={'address1': '','address2': '','address3': '','post_code': '', })[0]
            except Institution.DoesNotExist:
                verblog('Institution %s does not exists and cannot be created.' % owner, 2)
                raise CommandError, 'Institution %s does not exists and cannot create: aborting' % owner

            try:
                quality = Quality.objects.get_or_create(name=quality)[0]
            except Quality.DoesNotExist:
                verblog('Quality %s does not exists and cannot be creates, it will be read from metadata.' % quality, 2)
                raise CommandError, 'Quality %s does not exists and cannot be created: aborting' % quality

            try:
                errors = 0
                imported = 0
                updated = 0
                created = 0
                verblog('Starting index dowload...', 2)
                try:
                    if not start_record:
                        #find the id of the last imported landsat record
                        myMissions = Mission.objects.filter(abbreviation__in=['L2','L3','L4','L5','L7'])
                        mySensors = MissionSensor.objects.filter(mission__in=myMissions)
                        myTypes = SensorType.objects.filter(mission_sensor__in=mySensors)
                        myModes = AcquisitionMode.objects.filter(sensor_type__in=myTypes)
                        myLastProduct = OpticalProduct.objects.filter(acquisition_mode__in=myModes).order_by('original_product_id').reverse()[0]
                        start_record = myLastProduct.original_product_id
                    myQuery = 'select FIRST %i * from t_landsat_frame where localization_id > %s' % ( int(max_records), int(start_record) )
                    myRows = self.informix.runQuery( myQuery )
                except:
                    verblog('Initial query to get latest 20 rows failed - aborting!',0)
                    raise

                print sys.path
                for myLandsatRow in myRows:
                    try:
                        verblog("-----------------------------",3)
                        verblog("-----------------------------",3)
                        # landsat row e.g.
                        #{'hd_shift': 589505315, 'sun_elev': 41.93, 'centre_lat': -33.169998168945312, 'b_gain': '###############', 'centre_time': 21995.347222777778, 'segment_common_id': 163777, 'centre_lon': 20.430000305175781, 'localization_id': 1219164, 'fop_scene': '#', 'bg_change': '###############', 'sun_az': 52.740000000000002, 's_quality': 8995, 'sb_present': '###############', 'bslgainchange': '232323232323232323232323232323'}
                        myLocalizationRow = self.informix.localization( myLandsatRow['localization_id'] )
                        myFrameRow = self.informix.frameForLocalization( myLocalizationRow['id'] )
                        mySegmentRow = self.informix.segmentForFrame( myFrameRow['segment_id'] )
                        myAuxFileRow = self.informix.auxfileForSegment( myFrameRow['segment_id'] )
                        myFileTypeRow = self.informix.fileTypeForAuxFile( myAuxFileRow['file_type'] )
                        myImage = self.informix.referencedThumb( myLocalizationRow, myFrameRow, mySegmentRow, myAuxFileRow, myFileTypeRow )

                        verblog("Landsat Frame Properties",3)
                        for myKey,myValue in dict.items(myLandsatRow):
                            verblog( "%s : %s" % (myKey,myValue),3)
                        verblog("Localization Properties",3)
                        for myKey,myValue in dict.items(myLocalizationRow):
                            verblog( "%s : %s" % (myKey,myValue),3)
                        verblog("Frame Properties",3)
                        for myKey,myValue in dict.items(myFrameRow):
                            verblog( "%s : %s" % (myKey,myValue),3)
                        verblog("Segment Properties",3)
                        for myKey,myValue in dict.items(mySegmentRow):
                            verblog( "%s : %s" % (myKey,myValue),3)
                        verblog("File Type Properties",3)
                        for myKey,myValue in dict.items(myFileTypeRow):
                            verblog( "%s : %s" % (myKey,myValue),3)





                        imported += 1
                    except:
                        if halt_on_error:
                            raise
                        errors += 1
                        if errors > 10:
                            verblog('Failure rate too high - more than 10 rows failed to import - aborting!',0)
                            raise

                    myProduct = OpticalProduct.objects.get( original_product_id = myLocalizationRow['localization_id'] )
                    if not myProduct:
                        myProduct = OpticalProduct()


                    # This work is in progress - continue imeplementation here..
                    #      set product properties in informix class generically then subclass this class for landsat etc




                verblog("%s packages imported" % imported)
                verblog("%s errors" % errors)

                if test_only:
                    transaction.rollback()
                    verblog("Testing only: transaction rollback.")
                else:
                    transaction.commit()
                    verblog("Committing transaction.", 2)
            except Exception, e:
                traceback.print_exc(file=sys.stdout)
                raise CommandError('Uncaught exception (%s): %s' % (e.__class__.__name__, e))
        except Exception, e:
            verblog('Rolling back transaction due to exception.')
            if test_only:
                from django.db import connection
                verblog(connection.queries)
            transaction.rollback()
            raise CommandError("%s" % e)
        finally:
            lockfile.release()
