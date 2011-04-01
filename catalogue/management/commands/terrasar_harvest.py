"""
Terrasar harvesting

Ingestion of terrasar catalogue

img_mod: String (254.0)
pol_mod: String (254.0)
pol_chan: String (254.0)
beam_id: String (254.0)
start_time: String (254.0)
path_dir: String (254.0)
rel_orbit: Real (33.31)
inc_min: Real (33.31)
inc_max: Real (33.31)
resolution: String (254.0)


Sensor types
78	HSS	HighResSpotLightSingle	High Resolution Spot Light Single Polarisation	1	1	39	SAR	SAR-TSX1
79	HSD	HighResSpotLightDual	High Resolution Spot Light Dual Polarisation	2	2	39	SAR	SAR-TSX1
80	HS3	HS300	High Resolution Spot Light 300 MHz	0,6	1	39	SAR	SAR-TSX1
81	SLS	SpotLightSingle	Spot Light Single Polarisation	1,5	1	39	SAR	SAR-TSX1
82	SLD	SpotLightDual	Spot Light Dual Polarisation	2,5	2	39	SAR	SAR-TSX1
83	SMS	StripMapSingle	Strip Map Single Polarisation	3	1	39	SAR	SAR-TSX1
84	SMD	StripMapDual	Strip Map Dual Polarisation	6	2	39	SAR	SAR-TSX1
85	SMQ	StripMapQuad	Strip Map Quad Polarisation	6	4	39	SAR	SAR-TSX1
86	SCS	ScanSAR	Scan SAR	16	1	39	SAR	SAR-TSX1

Acquisition mode
60	VV	VV	Vertical Vertical Polarisation	39	SAR	SAR-TSX1
61	HH	HH	Horizontal Horizontal Polarisation	39	SAR	SAR-TSX1
62	VVVH	VVVH	Vertical Vertical Vertical Horizontal Polarisation	39	SAR	SAR-TSX1
63	HHHV	HHHV	Horizontal Horizontal Horizontal Vertical Polarisation	39	SAR	SAR-TSX1
64	HHVV	HHVV	Horizontal Horizontal Vertical Vertical Polarisation	39	SAR	SAR-TSX1
65	HHHV	HHHV	Horizontal Horizontal Horizontal Vertical Polarisation	39	SAR	SAR-TSX1
66	QUAD	HH-VV-HV-VH	Horizontal Horizontal Vertical Vertical Horizontal Vertical Vertical Horizontal Quad Polarisation	39	SAR	SAR-TSX1


"""

import os
from optparse import make_option
import tempfile
import urllib2
import zipfile
import shutil
import subprocess
import re
from mercurial import lock, error

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.geometries import Polygon

from catalogue.models import *


# Hardcoded constants
PROJECTION            = 'ORBIT'
BAND_COUNT            = 5
RADIOMETRIC_RESOLUTION= 16 #TODO: check this
MISSION               = 'TSX'
MISSION_SENSOR        = 'SAR'


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
  help = "Imports Terrasar packages into the SAC catalogue"
  option_list = BaseCommand.option_list + (
      make_option('--index_url', '-b', dest='index_url', action='store',
          help='Base catalogue URL. Defaults is read from settings.py.', default=getattr(settings, 'CATALOGUE_TERRASAR_SHP_ZIP_URL', None)),
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB.', default=False),
      make_option('--owner', '-o', dest='owner', action='store',
          help='Name of the Institution package owner. Defaults to: Infoterra.', default='Infoterra'),
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
      make_option('--maxproducts', '-m', dest='maxproducts', action='store',
          help='Import at most n products.', default=0),
      make_option('--force_update', '-f', dest='force_update', action='store_true',
          help='Force an update for exists products, default behavior is to skip exists products.', default=False),
  )

  @staticmethod
  def fetch_geometries(index_url, area_of_interest):
    """
    Download the index and parses it, returns a generator list of features
    """
    try:
      index = urllib2.urlopen(index_url)
      temp_zip_dir = tempfile.mkdtemp()
      tmp_zip_name = os.path.join(temp_zip_dir, 'archive.zip')
      tmp_zip = open(tmp_zip_name, 'wb+')
      tmp_zip.write(index.read())
      tmp_zip.close()
      # Unzip
      archive = zipfile.ZipFile(tmp_zip_name, 'r')
      bad_file = archive.testzip()
      if bad_file:
        archive.close()
        del archive
        raise CommandError, 'Bad zip index file.'
      # Extract
      for zname in archive.namelist():
        outfile = file(os.path.join(temp_zip_dir, zname), 'wb')
        outfile.write(archive.read(zname))
        outfile.close()
      archive.close()
      data_source = DataSource(os.path.join(temp_zip_dir, 'archive.shp'))
    except urllib2.HTTPError, e:
      raise CommandError('Cannot download index (%s): %s.' % (index_url, e))
    except Exception, e:
      raise CommandError("Loading index failed %s" % e)

    for pt in data_source[0]:
      if not area_of_interest or area_of_interest.intersects(pt.geom):
        yield pt

    del(data_source)

    try:
      shutil.rmtree(temp_zip_dir)
    except:
      raise CommandError, 'Cannot delete temporary folder %s.' % temp_zip_dir

  @transaction.commit_manually
  def handle(self, *args, **options):
    """ command execution """

    try:
      lockfile = lock.lock("/tmp/terrasar_harvest.lock", timeout=60)
    except error.LockHeld:
      # couldn't take the lock
      raise CommandError, 'Could not acquire lock.'

    index_url             = options.get('index_url')
    test_only             = options.get('test_only')
    verbose               = int(options.get('verbosity'))
    license               = options.get('license')
    owner                 = options.get('owner')
    software              = options.get('creating_software')
    area                  = options.get('area')
    quality               = options.get('quality')
    maxproducts           = int(options.get('maxproducts'))
    processing_level      = options.get('processing_level')
    force_update          = options.get('force_update')

    # Hardcoded
    projection            = PROJECTION
    band_count            = BAND_COUNT
    radiometric_resolution= RADIOMETRIC_RESOLUTION
    mission_sensor        = MISSION_SENSOR
    mission               = MISSION


    area_of_interest  = None

    def verblog(msg, level=1):
      if verbose >= level:
        print msg

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
        verblog('Starting index dowload...', 2)
        for package in Command.fetch_geometries(index_url, area_of_interest):
          if maxproducts and imported >= maxproducts:
            verblog("Maxproducts %s exceeded: exiting" % maxproducts, 2)
            break

          verblog("Ingesting %s" % package, 2)

          path, path_shift, row, row_shift = get_row_path_from_polygon(package.geom, no_compass=True)

          # Estract metadata
          sensor_type = str(package['img_mod'])[-3:-1] + str(package['pol_mod'])[0]
          acquisition_mode = str(package['pol_chan']).replace('/', '')
          try:
            resolution = str(package['resolution'])
            res_range = map(lambda x: not x or float(x.replace(',', '.')), re.search('(\d+,\d+)[^\d]+(\d+,\d+)?', resolution).groups())
            if type(res_range[0]) == float and type(res_range[1]) == float:
              geometric_resolution = (res_range[1] + res_range[0]) / 2
            elif type(res_range[0]) == float:
              geometric_resolution = res_range[0]
            verblog('Resolution set to %s' % geometric_resolution)
          except:
            verblog('Cannot calculate resolution from %s' % resolution)
            geometric_resolution = None
          orbit_number = int(float(str(package['rel_orbit'])))
          start_time = datetime.datetime.strptime(str(package['start_time'])[:-4], '%Y-%m-%dT%H:%M:%S')
          # Fills the the product_id
          #SAT_SEN_TYP_MODD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL_PROJTN
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
            'YYMMDD': start_time.strftime('%y%m%d'),
            'HHMMSS': start_time.strftime('%H%M%S'),
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
            'owner': owner,
            'license': license,
            'creating_software': software,
            'quality': quality,
            'incidence_angle': (package.get('inc_min') + package.get('inc_max')) / 2,
            'geometric_resolution_x': geometric_resolution,
            'geometric_resolution_y': geometric_resolution,
            'orbit_number': orbit_number,
            'polarising_mode': str(package['pol_mod'])[0],
            'orbit_direction': str(package['path_dir'])[0].upper(),
            'imaging_mode': str(package['img_mod']),
          }
          verblog(data, 2)

          # Check if it's already in catalogue:
          try:
            op = RadarProduct.objects.get(product_id=product_id).getConcreteInstance()
            is_new = False
            #No need to update...
            if force_update:
              verblog('Alredy in catalogue: updating.', 2)
              op.__dict__.update(data)
            else:
              verblog('Alredy in catalogue: skipping.', 2)
          except ObjectDoesNotExist:
            op = RadarProduct(**data)
            verblog('Not in catalogue: creating.', 2)
            is_new = True
            try:
              op.productIdReverse(True)
            except Exception, e:
              raise CommandError('Cannot get all mandatory data from product id %s (%s).' % (product_id, e))
          try:
            op.save()
            imported = imported + 1
          except Exception, e:
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

