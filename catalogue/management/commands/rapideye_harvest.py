"""
Rapideye harvesting

Ingestion of rapideye catalogue

(AOI Southern Africa)
RapidEye has provided SAC access to their archive records and given permission
to add these to SAC's own catalogue. All records for Southern Africa (South of
the Equator) need to be added to the catalogue and preferably updated at daily
intervals. The following particulars have been provided by RapidEye to make this
possible.
Your username is: c_0010027
Your password is: 8u3j8csPpI
our Download Catalog as well as to our Online Discovery Tool EyeFind. You may access
here: https://eyefind.rapideye.de Download Catalog can be found here:
https://delivery.rapideye.de/catalogue/


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


# Hardcoded constants
PROJECTION            = 'ORBIT'
BAND_COUNT            = 5
RADIOMETRIC_RESOLUTION= 16
SENSOR_TYPE           = 'VRN'
ACQUISITION_MODE      = 'PB'
MISSION_SENSOR        = 'REI'
GEOMETRIC_RESOLUTION  = 5
PRODUCT_ACQUISITION_START_TIME = '0900'


def get_row_path_from_polygon(poly, as_int=False, no_compass=False):
  """
  Given a polygon, returns row, row_shift, path, path_shift
  informations of the centroid as a string
  As indicated in the docs (8.1.3)
  """
  path, path_shift = ("%.2f" % poly.centroid.x).split('.')
  row, row_shift = ("%.2f" % poly.centroid.y).split('.')
  if as_int:
    return int(path), int(path_shift), int(row), int(row_shift)
  if no_compass:
    return path, path_shift, row, row_shift
  if poly.centroid.x < 0:
    path = "%sW" % path
  else:
    path = "%sE" % path
  if poly.centroid.y < 0:
    row = "%sS" % row
  else:
    row = "%sN" % row
  return path, path_shift, row, row_shift

class Command(BaseCommand):
  help = "Imports RapidEye packages into the SAC catalogue"
  option_list = BaseCommand.option_list + (
      make_option('--username', '-u', dest='username', action='store',
          help='Username for HTTP Authentication. Defaults is read from settings.py.', default=getattr(settings, 'CATALOGUE_RAPIDEYE_USERNAME', None)),
      make_option('--password', '-p', dest='password', action='store',
          help='Password for HTTP Authentication. Defaults is read from settings.py.', default=getattr(settings, 'CATALOGUE_RAPIDEYE_PASSWORD', None)),
      make_option('--base_url', '-b', dest='base_url', action='store',
          help='Base catalogue URL. Defaults is read from settings.py.', default=getattr(settings, 'CATALOGUE_RAPIDEYE_BASE_URL', None)),
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB.', default=False),
      make_option('--owner', '-o', dest='owner', action='store',
          help='Name of the Institution package owner. Defaults to: Rapideye AG.', default='Rapideye AG'),
      make_option('--creating_software', '-s', dest='creating_software', action='store',
          help='Name of the creating software. Defaults to: Unknown.', default='Unknown'),
      make_option('--year', '-y', dest='year', action='store',
          help='Year to ingest (4 digits). Defaults to: current year', default=datetime.datetime.strftime(datetime.datetime.now(), '%Y')),
      make_option('--day', '-d', dest='day', action='store',
          help='Day to ingest (2 digits). Defaults to None', default=None),
      make_option('--month', '-m', dest='month', action='store',
          help='Month to ingest (2 digits). Defaults to: current month', default=datetime.datetime.strftime(datetime.datetime.now(),'%m')),
      make_option('--license', '-l', dest='license', action='store', default='SAC Commercial License',
          help='Name of the license. Defaults to: SAC Commercial License'),
      make_option('--area', '-a', dest='area', action='store',
          help='Area of interest, images which are external to this area will not be imported (WKT Polygon, SRID=4326)'),
      make_option('--quality', '-q', dest='quality', action='store',
          help='Quality code (will be created if does not exists). Defaults to: Unknown', default='Unknown'),
      make_option('--processing_level', '-r', dest='processing_level', action='store',
          help='Processing level code (will be created if does not exists). Defaults to: 1B', default='1B'),
  )

  @staticmethod
  def fetch_geometries(index_url_base, area_of_interest):
    """
    Download the index and parses it, returns a generator list of features
    """
    try:
      temp_base = tempfile.mktemp()
      for ext in ('shp', 'shx', 'dbf'):
        _url = "%s.%s" % (index_url_base, ext)
        _index = urllib2.urlopen(_url)
        _tmp = open("%s.%s" % (temp_base, ext), 'wb+')
        _tmp.write(_index.read())
        _index.close()
        _tmp.close()
      data_source = DataSource("%s.%s" % (temp_base, 'shp'))
    except urllib2.HTTPError, e:
      raise CommandError('Cannot download index (%s): %s.' % (_url, e))
    except Exception, e:
      raise CommandError("Loading index failed %s" % e)

    for pt in data_source[0]:
      if not area_of_interest or area_of_interest.intersects(pt.geom):
        yield pt

    del(data_source)

    for ext in ('shp', 'shx', 'dbf'):
      _f = "%s.%s" % (temp_base, ext)
      try:
        os.remove(_f)
      except:
        print 'Cannot delete temporary file %s.' % _f
        pass

  @transaction.commit_manually
  def handle(self, *args, **options):
    """ command execution """

    try:
      lockfile = lock.lock("/tmp/rapideye_harvest.lock", timeout=60)
    except error.LockHeld:
      # couldn't take the lock
      raise CommandError, 'Could not acquire lock.'

    username              = options.get('username')
    password              = options.get('password')
    base_url              = options.get('base_url')
    year                  = options.get('year')
    day                   = options.get('day')
    month                 = options.get('month')
    test_only             = options.get('test_only')
    verbose               = int(options.get('verbosity'))
    license               = options.get('license')
    owner                 = options.get('owner')
    software              = options.get('creating_software')
    area                  = options.get('area')
    quality               = options.get('quality')
    processing_level      = options.get('processing_level')

    # Hardcoded
    projection            = PROJECTION
    band_count            = BAND_COUNT
    radiometric_resolution= RADIOMETRIC_RESOLUTION
    mission_sensor        = MISSION_SENSOR
    sensor_type           = SENSOR_TYPE
    acquisition_mode      = ACQUISITION_MODE
    geometric_resolution  = GEOMETRIC_RESOLUTION


    area_of_interest  = None

    def verblog(msg, level=1):
      if verbose >= level:
        print msg

    verblog('Getting verbose (level=%s)... ' % verbose, 2)
    if test_only:
        verblog('Testing mode activated.', 2)

    try:
      # Try connection
      try:
        verblog('Opening connection...', 2)
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, base_url, username, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        opener.open(base_url)
        urllib2.install_opener(opener)
        verblog('Connection open.', 2)
      except urllib2.HTTPError, e:
        raise CommandError('Unable to establish a connection: %s.' % e)

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

      # Builds the path:  https://delivery.rapideye.de/catalogue/shapes/2011/03/accum_itt_shape_2011-03.shp
      if day:
        base_index_url = os.path.join(base_url, 'shapes', year, month, day, 'itt_shape_%s-%s' % (year, month))
        verblog('Day filtering activated.', 2)
        base_index_url = "%s-%s" % (base_index_url,day)
      else:
        base_index_url = os.path.join(base_url, 'shapes', year, month, 'accum_itt_shape_%s-%s' % (year, month))

      verblog('Index base url: %s. (+ extension)' % base_index_url, 2)

      try:
        imported = 0
        verblog('Starting index dowload...', 2)
        for package in Command.fetch_geometries(base_index_url, area_of_interest):
          verblog("Ingesting %s" % package, 2)

          path, path_shift, row, row_shift = get_row_path_from_polygon(package.geom, no_compass=True)
          # Gets the mission
          mission_id = package.get('CRAFT_ID')[-1]
          if not int(mission_id) in (1,2,3,4,5):
            raise CommandError('Unknown RapidEye mission number (should be 1-5) %s.' % mission_id)

          # Defaults
          mission = "RE%s" % mission_id

          # Fills the the product_id
          #SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL_PROJTN
          product_id = "%(SAT)s_%(SEN)s_%(TYP)s_%(MOD)s_%(KKKK)s_%(KS)s_%(JJJJ)s_%(JS)s_%(YYMMDD)s_%(HHMMSS)s_%(LEVL)s_%(PROJTN)s" % \
          {
            'SAT': mission.ljust(3, '-'),
            'SEN': mission_sensor.ljust(3, '-'),
            'TYP': sensor_type.ljust(3, '-'),
            'MOD': acquisition_mode.ljust(4, '-'),
            'KKKK': path.rjust(4, '0'),
            'KS': path_shift.rjust(2, '0'),
            'JJJJ': row.rjust(4, '0'),
            'JS': row_shift.rjust(2, '0'),
            'YYMMDD': package.get('ACQ_DATE').strftime('%y%m%d'),
            'HHMMSS': "%s00" % PRODUCT_ACQUISITION_START_TIME,
            'LEVL' : processing_level.ljust(4, '-'),
            'PROJTN': projection.ljust(6, '-')
          }
          assert len(product_id) == 58, 'Wrong len in product_id'

          verblog("Product ID %s" % product_id, 2)

          # Do the ingestion here...
          data = {
            'metadata': '\n'.join(["%s=%s" % (f,package.get(f)) for f in package.fields]),
            'spatial_coverage': package.geom.geos,
            'product_id': product_id,
            'radiometric_resolution': radiometric_resolution,
            'band_count': band_count,
            'cloud_cover': int(package.get('CCP')), # integer percent
            'owner': owner,
            'license': license,
            'creating_software': software,
            'quality': quality,
            'sensor_inclination_angle': package.get('IND_ANGLE'),
            'sensor_viewing_angle': package.get('VW_ANGLE'),
            'original_product_id': package.get('PATH'),
            'solar_zenith_angle': 90 - package.get('SUNELVN'),
            'solar_azimuth_angle': package.get('SUNAZMT'),
            'geometric_resolution_x': geometric_resolution,
            'geometric_resolution_y': geometric_resolution,
          }
          verblog(data, 2)

          # Check if it's already in catalogue:
          try:
            op = OpticalProduct.objects.get(product_id=data.get('product_id')).getConcreteInstance()
            verblog('Alredy in catalogue: updating.', 2)
            is_new = False
            op.__dict__.update(data)
          except ObjectDoesNotExist:
            op = OpticalProduct(**data)
            verblog('Not in catalogue: creating.', 2)
            is_new = True
            try:
              op.productIdReverse(True)
            except Exception, e:
              raise CommandError('Cannot get all mandatory data from product id %s (%s).' % (product_id, e))

          try:
            op.save()
            if test_only:
              verblog('Testing: image not saved.', 2)
            else:
              # Store thumbnail
              thumbnails_folder = os.path.join(settings.THUMBS_ROOT, op.thumbnailDirectory())
              try:
                os.makedirs(thumbnails_folder)
              except:
                pass
              # Download original geotiff thumbnail and creates a thumbnail
              tiff_thumb = os.path.join(thumbnails_folder, op.product_id + ".tiff")
              handle = open(tiff_thumb, 'wb+')
              thumbnail = urllib2.urlopen(package.get('PATH'))
              handle.write(thumbnail.read())
              thumbnail.close()
              handle.close()
              # Transform and store .wld file
              jpeg_thumb = os.path.join(thumbnails_folder, op.product_id + ".jpg")
              # gdal_translate' -co worldfile=on -of JPEG 3259709_2011-03-08_5719804_5719908_browse.tiff 3259709_2011-03-08_5719804_5719908_browse.jpg
              subprocess.check_call(["gdal_translate", "-q", "-co", "worldfile=on", "-of", "JPEG", tiff_thumb, jpeg_thumb])
              # Removes xml
              os.remove("%s.%s" % (jpeg_thumb, 'aux.xml'))
              os.remove(tiff_thumb)
            if is_new:
              verblog('Product %s imported.' % product_id)
            else:
              verblog('Product %s updated.' % product_id)
            imported = imported + 1
          except Exception, e:
            try:
              os.remove(tiff_thumb)
            except:
              pass
            raise CommandError('Cannot import: %s' % e)

        verblog("%s packages imported" % imported)

        if test_only:
          transaction.rollback()
          verblog("Testing only: transaction rollback.")
        else:
          transaction.commit()
          verblog("Committing transaction.", 2)
      except Exception, e:
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

