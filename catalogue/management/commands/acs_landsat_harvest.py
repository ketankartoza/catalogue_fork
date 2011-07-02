"""
Tool for harvesting landsat data from the legacy acs catalogue
"""

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
from informix import Informix


class Command(BaseCommand):
  help = "Imports ACS Landsat records into the SAC catalogue"
  option_list = BaseCommand.option_list + (
      make_option('--download-thumbs', '-d', dest='download_thumbs', action='store',
          help='Whether thumbnails should be fetched too. If not fetched now they will be fetched on demand as needed.', default=False),
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
  )
  informix = Informix()

  def frameForLocalization( self, theLocalizationId ):
    """Return a frame record given a localization record. Record returned will 
    look something like this:
           {'ordinal': 20, 
          'ur_lon': 22.040000915527344, 
          'lr_lat': -32.759998321533203, 
          'ul_lat': -30.75, 
          'll_lon': 19.569999694824219, 
          'segment_id': 163777, 
          'frame': 82, 
          'ul_lon': 20.049999237060547, 
          'll_lat': -32.459999084472656, 
          'lr_lon': 21.600000381469727, 
          'begin_time_cod': 21995.346796739504, 
          'localization_id': 1219163, 
          'processable': True, 
          'ur_lat': -31.040000915527344, 
          'cloud_mean': 0, 
          'track_orbit': 174, 
          'end_time_cod': 21995.347094024386, 
          'cloud': '0000****'}"""
    myFrameQuery = "select * from t_frame_common where localization_id=%i;" % theLocalizationId
    myFrameRows = self.informix.runQuery( myFrameQuery )
    # There should only be one record
    if len( myFrameRows ) > 1:
      raise Exception("FrameRows","Too many framerows returned for localization (received %s, expected 1)" % len(myFrameRows) )
    if len( myFrameRows ) < 1:
      raise Exception("FrameRows","Too few framerows returned for localization (received 0, expected 1)" )
    myFrameRow = myFrameRows[0]
    return myFrameRow

  def segmentForFrame( self, theSegmentId ):
    """Return a segment record given a frame id. Return should look 
    something liks this:
    {'sensor_id': 2, 
      'mission': 5, 
      'ascending_flag': False, 
      'satellite_id': 1, 
      'i_lon_max': 28.443050384521484, 
      'displayed_orbit': 138589, 
      'id': 163777, 
      'start_feet': 0, 
      'i_lon_min': 18.360977172851562, 
      'start_block': 0, 
      'time_stamp': datetime.datetime(2010, 4, 1, 9, 35, 44), 
      'end_block': 0, 
      'first_address': 20, 
      'insertion_date': 22005.361816053242, 
      'beg_record_date': 21995.341348495371, 
      'station_id': 19, 
      'geo_shape': 'POLYGON((26.733053 -2.30708, 26.2 -4.8, 25.89 -6.24, 25.58 -7.69, 25.26 -9.14, 24.94 -10.58, 24.62 -12.03, 24.3 -13.47, 23.97 -14.91, 23.64 -16.36, 23.31 -17.8, 22.97 -19.24, 22.63 -20.68, 22.28 -22.13, 21.92 -23.57, 21.56 -25, 21.2 -26.44, 20.82 -27.88, 20.44 -29.32, 20.05 -30.75, 19.65 -32.18, 19.24 -33.62, 18.360977 -36.550076, 20.507157 -36.867314, 21.3 -33.92, 21.68 -32.48, 22.04 -31.04, 22.41 -29.6, 22.76 -28.16, 23.11 -26.72, 23.45 -25.28, 23.79 -23.84, 24.13 -22.39, 24.46 -20.95, 24.78 -19.51, 25.1 -18.06, 25.42 -16.62, 25.74 -15.17, 26.06 -13.73, 26.37 -12.28, 26.68 -10.83, 26.99 -9.39, 27.3 -7.94, 27.6 -6.49, 27.91 -5.04, 28.443051 -2.5631083, 26.733053 -2.30708))', 
      'end_feet': 0, 
      'cycle': 138589, 
      'displayed_medium': '1927', 
      'medium_id': 163777, 
      'end_record_date': 21995.347863935185, 
      'i_lat_max': -2.3070800304412842, 
      'i_lat_min': -36.867313385009766, 
      'npass': 1, 
      'orbit': 174, 
      'displayed_track': '174', 
      'second_address': 22}"""


    mySegmentQuery = "select * from t_segment_common where id=%i;" % theSegmentId
    mySegmentRows = self.informix.runQuery( mySegmentQuery )
    # There should only be one record
    if len( mySegmentRows ) > 1:
      raise Exception("SegmentRows","Too many segment rows returned for frame (received %s, expected 1)" % len(mySegmentRows) )
    if len( mySegmentRows ) < 1:
      raise Exception("SegmentRows","Too few segment rows returned for frame (received 0, expected 1)" )
    mySegmentRow = mySegmentRows[0]
    return mySegmentRow



  def auxfileForSegment( self, theSegmentId ):
    """ Return an auxfile for a segment. An auxfile is the thing that 
    actually contains the quicklook blob in it."""
    myAuxFileQuery = "select * from t_aux_files where common_id=%i;" % theSegmentId
    myAuxFileRows = self.informix.runQuery( myAuxFileQuery )
    # There should only be one record
    if len( myAuxFileRows ) > 1:
      raise Exception("AuxFileRows","Too many auxfile rows returned for segment (received %s, expected 1)" % len(myAuxFileRows) )
    if len( myAuxFileRows ) < 1:
      raise Exception("AuxFileRows","Too few auxfile rows returned for segment (received 0, expected 1)" )
    myAuxFileRow = myAuxFileRows[0]
    return myAuxFileRow



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
    test_only             = options.get('test_only')
    verbose               = int(options.get('verbosity'))
    license               = options.get('license')
    owner                 = options.get('owner')
    software              = options.get('creating_software')
    area                  = options.get('area')
    quality               = options.get('quality')
    processing_level      = options.get('processing_level')

    area_of_interest  = None


    verblog('Getting verbose (level=%s)... ' % verbose, 2)
    if test_only:
        verblog('Testing mode activated.', 2)

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
        imported = 0
        updated = 0
        created = 0
        verblog('Starting index dowload...', 2)
        myQuery = "select * from t_localization where id=1219163;"
        myRows = self.informix.runQuery( myQuery )
        # There should only be one record
        if len( myRows ) > 1:
          raise Exception("LocalizationRows","Too many localization rows returned for localization (received %s, expected 1)" % len(myRows) )
        for myRow in myRows:
          print myRow
          # e.g. {'object_supertype': 1, 'time_stamp': datetime.datetime(2010, 4, 1, 9, 35, 46), 
          #       'id': 1219163, 
          # 'refresh_rate': 0, 
          # 'geo_time_info': 
          # 'POLYGON((21.6 -32.76, 22.04 -31.04, 20.05 -30.75, 19.57 -32.46, 21.6 -32.76))'} 
          myFrameRow = self.frameForLocalization( myRow['id'] )  
          mySegmentRow = self.segmentForFrame( myFrameRow['segment_id'] )
          myAuxfileRow = self.auxfileForSegment( myFrameRow['segment_id'] )

          print myFrameRow
          print mySegmentRow
          print myAuxfileRow


        verblog("%s packages imported" % imported)

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

