"""
Ingest MISR HDF packages from a local folder


Strategy:
  * scan the three folders:
      MB2LME MISR Level 1B2 Local Mode Ellipsoid Radiance Data Ellipsoid projected TOA parameters for the single local mode scene, resampled to WGS84 ellipsoid. HDF-EOS Grid
      MB2LMT MISR Level 1B2 Local Mode Terrain Radiance Data Terrain-projected TOA radiance for the single local mode scene, resampled at the surface and topographically corrected. HDF-EOS Grid
      MI1B2E MISR Level 1B2 Ellipsoid Data Contains the ellipsoid projected TOA radiance, resampled to WGS84 ellipsoid corrected.
  * sort the list of dated ascending
  * if the last scanned date for the folder is set, start from the next date
  * import nadir AN
  * create thumbnail for AN (will be used for all other images
  * parse metadata to get the footprint
  * get row and path from file name
  * import all other cameras (set the same footprint)

"""


import os
from optparse import make_option
import tempfile
import subprocess
from mercurial import lock, error
import shutil
from osgeo import gdal

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
MISSION               = 'TER' # Terra
MISSION_SENSOR        = 'MIS'
SENSOR_TYPE           = 'VNI'
ACQUISITION_MODE      = 'LM' # vary:
GEOMETRIC_RESOLUTION  = 275 # ... vary: http://www-misr.jpl.nasa.gov/Mission/misrInstrument/spatialResolution/
PRODUCT_ACQUISITION_START_TIME = '0900'
RC_FILE               = 'misr_ingest.rc'
SENSOR_VIEWING_ANGLE  = { # Azimuth
  'AN': 0.0,
  'AA': 26.1,
  'AF': 26.1,
  'BA': 45.6,
  'BF': 45.6,
  'CA': 60.0,
  'CF': 60.0,
  'DA': 70.5,
  'DF': 70.5,
}


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
  help = "Imports MISR packages into the SAC catalogue"
  option_list = BaseCommand.option_list + (
      make_option('--base_path', '-b', dest='base_path', action='store',
          help='Base catalogue path. Default is read from settings.py.', default=getattr(settings, 'MISR_ROOT')),
      make_option('--store_image', '-i', dest='store_image', action='store_true',
          help='Store the original image data extracted from the package.', default=True),
      make_option('--maxproducts', '-m', dest='maxproducts', action='store',
          help='Import at most n products.', default=0),
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB.', default=False),
      make_option('--rcfileskip', '-k', dest='rcfileskip', action='store_true',
          help='Do not read or write the run control file.', default=False),
      make_option('--owner', '-o', dest='owner', action='store',
          help='Name of the Institution package owner. Defaults to: MISR.', default='MISR'),
      make_option('--creating_software', '-s', dest='creating_software', action='store',
          help='Name of the creating software. Defaults to: Unknown.', default='Unknown'),
      make_option('--license', '-l', dest='license', action='store', default='SAC Commercial License',
          help='Name of the license. Defaults to: SAC Commercial License'),
      make_option('--quality', '-q', dest='quality', action='store',
          help='Quality code (will be created if does not exists). Defaults to: Unknown', default='Unknown'),
      make_option('--processing_level', '-r', dest='processing_level', action='store',
          help='Processing level code (will be created if does not exists). Defaults to: 1B2', default='1B2'),
  )


  @transaction.commit_manually
  def handle(self, *args, **options):
    """ command execution """

    try:
      lockfile = lock.lock("/tmp/modis_harvest.lock", timeout=60)
    except error.LockHeld:
      # couldn't take the lock
      raise CommandError, 'Could not acquire lock.'

    base_path             = options.get('base_path')
    store_image           = options.get('store_image')
    test_only             = options.get('test_only')
    verbose               = int(options.get('verbosity'))
    license               = options.get('license')
    owner                 = options.get('owner')
    quality               = options.get('quality')
    rcfileskip            = options.get('rcfileskip')
    processing_level      = options.get('processing_level')
    maxproducts           = int(options.get('maxproducts'))

    # Hardcoded
    projection            = PROJECTION
    band_count            = BAND_COUNT
    radiometric_resolution= RADIOMETRIC_RESOLUTION
    sensor_type           = SENSOR_TYPE
    acquisition_mode      = ACQUISITION_MODE
    geometric_resolution  = GEOMETRIC_RESOLUTION


    def verblog(msg, level=1):
      if verbose >= level:
        print msg

    verblog('Getting verbose (level=%s)... ' % verbose, 2)
    if test_only:
        verblog('Testing mode activated.', 2)

    def add_directory(line):
      if line.startswith('d'):
        bits = line.split()
        dirname = bits[7]
        verblog('Adding folder %s' % dirname, 2)
        directories.append(dirname)


    try:
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
        # Stores last scanned date and file for each main folder
        last_processed = {}
        imported = 0
        # Get first level dir
        for l0_folder in os.listdir(base_path):
          verblog('Found main folder : %s' % l0_folder, 2)
          #
          # Get second level dir (date)
          for l1_folder in os.listdir(os.path.join(base_path, l0_folder)):
            l1_folder = os.path.split(l1_folder)[-1]
            #
            level_1_folder = l1_folder

            verblog('Scanning folder: %s' % l1_folder, 2)
            package_list = os.listdir(os.path.join(base_path, l0_folder, l1_folder))
            #verblog('package_list: %s' % package_list, 2)
            package_list.sort()
            # Seek to last_package position
            try:
              package_list = package_list[package_list.index(last_package) + 1:]
            except:
              verblog('Cannot find last_package in list', 2)


            for package in package_list:
              #import ipy; ipy.shell()
              #verblog('Maxproducts %s, imported %s' % (maxproducts, imported), 2)
              if maxproducts and imported >= maxproducts:
                verblog("Maxproducts %s exceeded: exiting" % maxproducts, 2)
                break
              verblog("Ingesting %s" % package, 2)
              last_package = package
              # Save to tmp
              tmp_image = tempfile.mktemp('.hdf')
              verblog("Copying to temporary %s, %s" % (tmp_image, package), 2)
              shutil.copy(os.path.join(base_path, l0_folder, l1_folder, package), tmp_image)

              # Parse metadata with GDAL
              img = gdal.Open(tmp_image)
              metadata = img.GetMetadata_Dict()
              import ipy; ipy.shell()
              # Mission
              mission = MISSION
              mission_sensor = MISSION_SENSOR

              # Polygon
              lon = metadata['GRINGPOINTLONGITUDE']
              lon = [float(l) for l in lon.split(', ')]
              lat = metadata['GRINGPOINTLATITUDE']
              lat = [float(l) for l in lat.split(', ')]
              points = zip(lon, lat)
              points.append((lon[0], lat[0]))
              footprint = Polygon(points)

              # Row/Path
              path, path_shift, row, row_shift = get_row_path_from_polygon(footprint, no_compass=True)

              # Fills the the product_id
              #SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL_PROJTN
              product_id = "%(SAT)s_%(SEN)s_%(TYP)s_%(MOD)s_%(KKKK)s_%(KS)s_%(JJJJ)s_%(JS)s_%(YYMMDD)s_%(HHMMSS)s_%(LEVL)s_%(PROJTN)s" % \
              {
                'SAT': mission.ljust(3, '-'),
                'SEN': mission_sensor.ljust(3, '-'),
                'TYP': sensor_type.ljust(3, '-'),
                'MOD': acquisition_mode.ljust(3, '-'),
                'KKKK': path.rjust(4, '0'),
                'KS': path_shift.rjust(2, '0'),
                'JJJJ': row.rjust(4, '0'),
                'JS': row_shift.rjust(2, '0'),
                'YYMMDD': datetime.datetime.strptime(metadata['RANGEBEGINNINGDATE'],'%Y-%m-%d').strftime('%y%m%d'),
                'HHMMSS': ''.join(metadata['RANGEBEGINNINGTIME'].split(':'))[:6],
                'LEVL' : processing_level.ljust(4, '-'),
                'PROJTN': projection.ljust(6, '-')
              }

              verblog("Product ID %s" % product_id, 2)

              # Store original metadata XML into catalogue metadata field
              original_metadata = []
              ftp.retrlines('RETR %s' % package + '.xml', original_metadata.append)

              # Do the ingestion here...
              data = {
                'metadata': '\n'.join(original_metadata),
                'spatial_coverage': footprint,
                'product_id': product_id,
                'radiometric_resolution': radiometric_resolution,
                'band_count': band_count,
                'owner': owner,
                'license': license,
                'creating_software': creating_software,
                'quality': quality,
                'original_product_id': metadata['LOCALGRANULEID'],
                'geometric_resolution_x': geometric_resolution,
                'geometric_resolution_y': geometric_resolution,
                'product_acquisition_end': datetime.datetime.strptime(metadata['RANGEENDINGDATE'] + ' ' + metadata['RANGEENDINGTIME'], '%Y-%m-%d %H:%M:%S.%f'),
                'sensor_viewing_angle': SENSOR_VIEWING_ANGLE[package[39:41], # Get it from the image name
              }
              verblog(data, 2)

              # Check if it's already in catalogue:
              try:
                op = OpticalProduct.objects.get(product_id=data.get('product_id')).getConcreteInstance()
                verblog('Already in catalogue: updating.', 2)
                is_new = False
                op.__dict__.update(data)
              except OpticalProduct.DoesNotExist:
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
                  # Get thumbnail from nadir (AN), copy if exists
                  thumbnails_folder = os.path.join(settings.THUMBS_ROOT, op.thumbnailPath())
                  try:
                    os.makedirs(thumbnails_folder)
                  except:
                    pass
                  # Extract sub images
                  # gdal_translate -sds -of GTiff MCD43A2.A2011057.h00v08.005.2011077192640.hdf MCD43A2.A2011057.h00v08.005.2011077192640.tif
                  tiff_thumb = tmp_image.replace('hdf', 'tif')
                  assert band_count == 4
                  tiff_1 = tiff_thumb + '1'
                  tiff_2 = tiff_thumb + '2'
                  tiff_3 = tiff_thumb + '3'
                  tiff_4 = tiff_thumb + '4'
                  #import ipy; ipy.shell()
                  try:
                    boundary = footprint[0]
                    subprocess.check_call(["gdal_translate", "-q", "-of", "GTiff", "-sds", "-a_srs", 'EPSG:4326', "-gcp", "0", "2400", "%s" % boundary[0][0], "%s" % boundary[0][1], "-gcp", "0", "0", "%s" % boundary[1][0], "%s" % boundary[1][1], "-gcp", "2400", "0", "%s" % boundary[2][0], "%s" % boundary[2][1],  "-gcp", "2400", "2400", "%s" % boundary[3][0], "%s" % boundary[3][1], tmp_image, tiff_thumb])
                  except subprocess.CalledProcessError:
                    # Check if the files are there
                    if not (os.path.isfile(tiff_1) and os.path.isfile(tiff_2) and os.path.isfile(tiff_3) and os.path.isfile(tiff_4)):
                      raise CommandError('gdal_translate -sds error.')
                  # Compose thumbnail
                  subprocess.check_call(["gdal_merge.py", "-q", "-separate",  tiff_1, tiff_4, tiff_3, "-o", tiff_thumb])
                  # Transform and store .wld file
                  # gdal_translate -co worldfile=on -outsize 400 400 -of JPEG composite.tif composite.jpg
                  jpeg_thumb = os.path.join(thumbnails_folder, op.product_id + ".jpg")
                  subprocess.check_call(["gdal_translate", "-outsize", '400', '400', "-q", "-of", "JPEG", tiff_thumb, jpeg_thumb])

                  dataset = gdal.Open(tiff_1)
                  gcps = dataset.GetGCPs()
                  if gcps is None or len(gcps) == 0:
                      raise CommandError('No GCPs found on file ' + tiff_1)
                  geotransform = gdal.GCPsToGeoTransform(gcps)
                  if geotransform is None:
                      raise CommandError('Unable to extract a geotransform.')

                  # Make the world file
                  wld = "%s\n%s\n%s\n%s\n%s\n%s\n" % (
                      geotransform[1],
                      geotransform[4],
                      geotransform[2],
                      geotransform[5],
                      geotransform[0] + 0.5 * geotransform[1] + 0.5 * geotransform[2],
                      geotransform[3] + 0.5 * geotransform[4] + 0.5 * geotransform[5],
                    )
                  # Store .wld file
                  jpeg_wld   =  os.path.join(thumbnails_folder, op.product_id + ".wld")
                  handle = open(jpeg_wld, 'w+')
                  handle.write(wld)
                  handle.close()

                  if store_image:
                    main_image_folder = os.path.join(settings.IMAGERY_ROOT, op.imagePath())
                    try:
                      os.makedirs(main_image_folder)
                    except:
                      pass
                    main_image = os.path.join(main_image_folder, op.product_id + ".hdf")
                    shutil.copy(tmp_image, main_image)
                    subprocess.check_call(["bzip2", "-f", main_image])
                    verblog("Storing main image for product %s: %s" % (product_id, main_image), 2)
                    # Save in local_storage_path
                    op.local_storage_path = os.path.join(op.imagePath(), op.product_id + ".hdf" + '.bz2')
                    op.save()
                if is_new:
                  verblog('Product %s imported.' % product_id)
                else:
                  verblog('Product %s updated.' % product_id)
                imported = imported + 1
                # Updates .ini file
                if not rcfileskip:
                  rc = open(RC_FILE, 'w+')
                  for md, lp in last_processed.items():
                    rc.write('last_package=%s/%s/%s\n' % (md, lp[0], lp[1]))
                  rc.close()
                  verblog('Wrote rcfile %s.' % RC_FILE, 2)
                else:
                  verblog('Skipping rcfile write.', 2)
              except Exception, e:
                raise CommandError('Cannot import: %s' % e)
              finally:
                assert band_count == 4
                for i in (tmp_image, tiff_thumb, tiff_1, tiff_2, tiff_3, tiff_4):
                  try:
                    os.remove(i)
                  except:
                    pass

        verblog("%s packages imported" % imported)

        if test_only:
          transaction.rollback()
          verblog("Testing only: transaction rollback.")
        else:
          transaction.commit()
          verblog("Committing transaction.", 2)
      except Exception, e:
        raise CommandError('Uncaught exception: %s' % e)
    except Exception, e:
      verblog('Rolling back transaction due to exception.')
      if test_only:
        from django.db import connection
        verblog(connection.queries)
      transaction.rollback()
      raise CommandError("%s" % e)
    finally:
      lockfile.release()

