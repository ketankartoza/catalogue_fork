"""
Ingest MISR HDF packages from a local folder

http://196.35.94.243/misr/

Main page
http://eosweb.larc.nasa.gov/PRODOCS/misr/table_misr.html

Strategy:
  * scan the three folders:
      MB2LME MISR Level 1B2 Local Mode Ellipsoid Radiance Data Ellipsoid projected TOA parameters for the single local mode scene, resampled to WGS84 ellipsoid. HDF-EOS Grid (Local mode)
      MB2LMT MISR Level 1B2 Local Mode Terrain Radiance Data Terrain-projected TOA radiance for the single local mode scene, resampled at the surface and topographically corrected. HDF-EOS Grid (Local mode)
      MI1B2E MISR Level 1B2 Ellipsoid Data Contains the ellipsoid projected TOA radiance, resampled to WGS84 ellipsoid corrected. (Global Mode)
  * sort the list of dated ascending
  * if the last scanned date for the folder is set, start from the next date
  * import nadir AN
  * create thumbnail for AN (will be used for all other images
  * parse metadata to get the footprint
  * get row and path from file name
  * import all other cameras (set the same footprint)

"""


import os
import tempfile
import subprocess
import shutil
import re

from optparse import make_option
from mercurial import lock, error

from osgeo import gdal, osr
from osgeo.gdalconst import *

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import Polygon

from catalogue.models import *
from catalogue.dims_lib import dimsWriter


# Hardcoded constants
PROJECTION            = 'ORBIT'
BAND_COUNT            = 5
RADIOMETRIC_RESOLUTION= 16
MISSION               = 'TER' # Terra
MISSION_SENSOR        = 'MIS'
SENSOR_TYPE           = 'VNI'
ACQUISITION_MODE      = ('LM', 'GM') # vary: Cam_mode -> 0=local 1=global
GEOMETRIC_RESOLUTION  = 275 # ... vary: http://www-misr.jpl.nasa.gov/Mission/misrInstrument/spatialResolution/
RC_FILE               = 'misr_ingest.rc'
MAX_BLOCK_FOR_THUMB   = 4 # Do not create thumbs for (globalmode) images with more than 4 blocks

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
FOLDERS               = ('MB2LME.002', 'MB2LMT.002', 'MI1B2E.003')

def GDALInfoReportCorner( dataset, x, y ):
  # From: http://svn.osgeo.org/gdal/trunk/gdal/swig/python/samples/gdalinfo.py
  adfGeoTransform = dataset.GetGeoTransform()
  if adfGeoTransform is not None:
    dfGeoX = adfGeoTransform[0] + adfGeoTransform[1] * x + adfGeoTransform[2] * y
    dfGeoY = adfGeoTransform[3] + adfGeoTransform[4] * x + adfGeoTransform[5] * y
    return dfGeoX, dfGeoY
  else:
    return x, y

def GetMetadataFromCore(metadata, name):
  """
  Scan the core metadata for values
  """
  found = False
  for l in metadata.get('coremetadata').split('\n'):
    if found and l.find(' VALUE ') != -1:
      try:
        return re.search(r'\s=\s["\(]?([^"\)]+)', l).groups()[0]
      except:
        raise CommandError, 'Cannot find core metadata value for %s' % name
    if l.find(name) != -1:
      found = True
  return ''

def GetFootPrintFromKML(path, block):
  """
  Reads the KML and returns the polygon points
  """
  kml = open(os.path.join(settings.ROOT_PROJECT_FOLDER, 'resources', 'misr_paths.kml'))
  lines = kml.readlines()
  for l in range(0, len(lines)):
    if lines[l].find('MISR Path %s Block %s' % (path, block)) != -1:
      return [map(float, line[:-5].split(',')) for line in lines[l+5:l+10]]
  return None

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
    creating_software     = options.get('creating_software')
    maxproducts           = int(options.get('maxproducts'))

    # Hardcoded
    projection            = PROJECTION
    band_count            = BAND_COUNT
    radiometric_resolution= RADIOMETRIC_RESOLUTION
    sensor_type           = SENSOR_TYPE
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
        creating_software = CreatingSoftware.objects.get_or_create(name=creating_software, defaults={'version': 0})[0]
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
        # Reads ini file
        last_date_list = {}
        if not rcfileskip:
          try:
            rc = open(RC_FILE, 'r')
            for l in iter(rc):
              lf, ld = l[:-1].split('=')[1].split('/')
              last_date_list[lf] = ld
              verblog('Last package: %s/%s' % (lf, ld), 2)
            rc.close()
          except:
            verblog('Cannot read rcfile %s' % RC_FILE, 2)
        else:
          verblog('Skipping rc file.', 2)

        # Stores last scanned date and file for each main folder
        last_processed = {}
        imported = 0
        # Get first level dir
        for main_folder in FOLDERS:
          verblog('Processing main folder : %s' % main_folder, 2)
          # Get second level dir (dates)
          date_list = os.listdir(os.path.join(base_path, main_folder))
          if not date_list:
            verblog('No dates in %s' % os.path.join(base_path, main_folder))
          date_list.sort()
          # Seek to saved date
          try:
            date_list = date_list[date_list.index(last_date_list[main_folder]) + 1:]
          except (KeyError, ValueError):
            verblog('Cannot find last_date in date list for folder %s' % main_folder, 2)

          for date_folder in date_list:
            #verblog('Maxproducts %s, imported %s' % (maxproducts, imported), 2)
            if maxproducts and imported >= maxproducts:
              verblog("Maxproducts %s exceeded: exiting" % maxproducts, 2)
              break
            date_folder = os.path.split(date_folder)[-1]
            last_processed[main_folder] = date_folder
            verblog('Scanning folder: %s' % date_folder, 2)
            # Main package
            packages = [d for d in os.listdir(os.path.join(base_path, main_folder, date_folder)) if d[-3:] == 'hdf']
            if not packages:
              verblog('No packages in %s' % os.path.join(base_path, main_folder, date_folder))
              continue
            package = packages[0]
            # Select main camera nadir
            package = [p for p in packages if p.find('_AN_') != -1][0]

            verblog("Ingesting %s" % package, 2)
            # Open
            img = gdal.Open(os.path.join(base_path, main_folder, date_folder, package), GA_ReadOnly)
            assert img is not None, 'gdal cannot open temporary image'
            # Points to first subdataset:
            sds = gdal.Open(img.GetSubDatasets()[0][0], GA_ReadOnly)
            metadata = sds.GetMetadata()
            # Polygon
            path = int(img.GetMetadata()['Path_number'])
            row = int(GetMetadataFromCore(metadata, 'ORBITNUMBER'))
            start_block = int(img.GetMetadata()['Start_block'])
            end_block = int(img.GetMetadata()['End block']) + 1
            verblog("Reading polygon from KML path %s, block %s" % (path, start_block), 2)
            footprint = Polygon(GetFootPrintFromKML(path, start_block))
            for block in range(start_block + 1, end_block):
              verblog("Reading polygon from KML path %s, block %s" % (path, block), 2)
              footprint = footprint.union(Polygon(GetFootPrintFromKML(path, block)))

            footprint.set_srid(4326)

            # Mission
            mission = MISSION
            mission_sensor = MISSION_SENSOR
            # Extract from metadata
            verblog("Extracting metadata...", 2)
            acquisition_mode = ACQUISITION_MODE[int(metadata.get('Cam_mode'))]
            geometric_resolution_x = int(metadata.get('Block_size.resolution_x')[:metadata.get('Block_size.resolution_x').find(',')])
            geometric_resolution_y = int(metadata.get('Block_size.resolution_y')[:metadata.get('Block_size.resolution_y').find(',')])
            product_acquisition_end = datetime.datetime.strptime(GetMetadataFromCore(metadata, 'RANGEENDINGDATE') + \
                                      GetMetadataFromCore(metadata, 'RANGEENDINGTIME'),'%Y-%m-%d%H:%M:%S.%fZ')
            product_acquisition_start = datetime.datetime.strptime(GetMetadataFromCore(metadata, 'RANGEBEGINNINGDATE') + \
                                      GetMetadataFromCore(metadata, 'RANGEBEGINNINGTIME'),'%Y-%m-%d%H:%M:%S.%fZ')

            # Row/Path
            #path, path_shift, row, row_shift = get_row_path_from_polygon(footprint, no_compass=True)
            # Assigned from file name (see above)
            path_shift = '0'
            row_shift = '0'

            # Fills the the product_id
            verblog("Filling product_id...", 2)
            #SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL_PROJTN
            product_id = "%(SAT)s_%(SEN)s_%(TYP)s_%(MOD)s_%(KKKK)s_%(KS)s_%(JJJJ)s_%(JS)s_%(YYMMDD)s_%(HHMMSS)s_%(LEVL)s_%(PROJTN)s" % \
            {
              'SAT': mission.ljust(3, '-'),
              'SEN': mission_sensor.ljust(3, '-'),
              'TYP': sensor_type.ljust(3, '-'),
              'MOD': acquisition_mode.ljust(4, '-'),
              'KKKK': str(path).rjust(4, '0'),
              'KS': path_shift.rjust(2, '0'),
              'JJJJ': str(row).rjust(4, '0'),
              'JS': row_shift.rjust(2, '0'),
              'YYMMDD': product_acquisition_start.strftime('%y%m%d'),
              'HHMMSS': product_acquisition_start.strftime('%H%M%S'),
              'LEVL' : processing_level.ljust(4, '-'),
              'PROJTN': projection.ljust(6, '-')
            }
            assert len(product_id) == 58, 'Wrong len in product_id'

            verblog("Product ID %s" % product_id, 2)

            # Do the ingestion here...
            data = {
              'metadata': '\n'.join(metadata),
              'spatial_coverage': footprint,
              'product_id': product_id,
              'radiometric_resolution': radiometric_resolution,
              'band_count': band_count,
              'owner': owner,
              'license': license,
              'creating_software': creating_software,
              'quality': quality,
              'original_product_id': package,
              'geometric_resolution_x': geometric_resolution_x,
              'geometric_resolution_y': geometric_resolution_y,
              'product_acquisition_end': datetime.datetime.strptime(GetMetadataFromCore(metadata, 'RANGEENDINGDATE') + ' ' + GetMetadataFromCore(metadata, 'RANGEENDINGTIME'), '%Y-%m-%d %H:%M:%S.%fZ'),
              'product_acquisition_end' : product_acquisition_end
            }
            #verblog(data, 2)

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

              temp_tif_list = []
              if int(img.GetMetadata()['End block']) - int(img.GetMetadata()['Start_block']) + 1 <= MAX_BLOCK_FOR_THUMB:
                # Creates a thumbnail on the fly mapping band 1 of the first 3 subdatasets to BGR
                outx= 100
                outy = 400
                inx = 512
                iny = 2048

                drv = gdal.GetDriverByName('GTiff')
                temp_tif = tempfile.mktemp()
                # Note that the underscore is missing in "End block"...
                for rast_band in range(int(img.GetMetadata()['Start_block']), int(img.GetMetadata()['End block']) + 1):
                  # Invert x, y: need to transpose
                  temp_tif_list.append('%s_%s.tif' % (temp_tif, rast_band))
                  dst_ds = drv.Create('%s_%s.tif' % (temp_tif, rast_band), outy, outx, 3, gdal.GDT_UInt16)

                  for dataset_number in (0, 1, 2):
                    sds = gdal.Open(img.GetSubDatasets()[dataset_number][0], GA_ReadOnly)
                    band = sds.GetRasterBand(rast_band)
                    a = band.ReadAsArray(0, 0, buf_xsize=outx, buf_ysize=outy)
                    a = a.transpose()
                    dst_ds.GetRasterBand(3 - dataset_number).WriteArray(a, 0, 0)
                    sds = None

                  srs = osr.SpatialReference()
                  srs.SetWellKnownGeogCS('WGS84')
                  dst_ds.SetProjection(srs.ExportToWkt())

                  points = GetFootPrintFromKML(int(img.GetMetadata()['Path_number']), rast_band)
                  gcps = []
                  gcps.append(gdal.GCP(points[0][0], points[0][1], 0, 0, 0))
                  gcps.append(gdal.GCP(points[1][0], points[1][1], 0, dst_ds.RasterXSize, 0))
                  gcps.append(gdal.GCP(points[2][0], points[2][1], 0, dst_ds.RasterXSize, dst_ds.RasterYSize))
                  gcps.append(gdal.GCP(points[3][0], points[3][1], 0, 0, dst_ds.RasterYSize))
                  dst_ds.SetGeoTransform(gdal.GCPsToGeoTransform(gcps))
                  dst_ds = None

                # Merge sub images
                tiff_thumb = os.path.join(thumbnails_folder, op.product_id + ".tiff")
                cmd = ["gdal_merge.py", "-o", tiff_thumb, "-q"]
                cmd.extend(temp_tif_list)
                subprocess.check_call(cmd)
                # Transforms the tiff thumb into a jpeg
                jpeg_thumb = os.path.join(thumbnails_folder, op.product_id + ".jpg")
                subprocess.check_call(["gdal_translate", "-ot", "Byte", "-scale", "-q", "-co", "worldfile=on", "-of", "JPEG", tiff_thumb, jpeg_thumb])
                # Removes xml and temporary images
                os.remove("%s.%s" % (jpeg_thumb, 'aux.xml'))
                os.remove(tiff_thumb)

                img = None
              else:
                verblog('Skipping thumbnail creation: too many blocks.', 2)

              if store_image:
                main_image_folder = os.path.join(settings.IMAGERY_ROOT, op.imagePath())
                try:
                  os.makedirs(main_image_folder)
                except:
                  pass
                verblog("Storing main image for product %s: %s" % (product_id, main_image_folder), 2)
                # Save in local_storage_path
                cmd = ["tar", "cjf", os.path.join(main_image_folder, "%s.tar.bz2" % product_id), "-C" , os.path.join(base_path, main_folder, date_folder)] + packages
                subprocess.check_call(cmd)
                op.local_storage_path = os.path.join(op.imagePath(), "%s.tar.bz2" % product_id)
                verblog('Package saved as %s' % os.path.join(op.imagePath(), "%s.tar.bz2" % product_id))
                op.save()
              if is_new:
                verblog('Product %s imported.' % product_id)
              else:
                verblog('Product %s updated.' % product_id)
              imported = imported + 1
              # Updates .ini file
              if not rcfileskip:
                rc = open(RC_FILE, 'w+')
                # main_folder date_folder
                for mf, df in last_processed.items():
                  rc.write('last_date=%s/%s\n' % (mf, df))
                rc.close()
                verblog('Wrote rcfile %s.' % RC_FILE, 2)
              else:
                verblog('Skipping rcfile write.', 2)
            except Exception, e:
              raise CommandError('Cannot import: %s' % e)
            finally:
              img = None
              # Removes temporary tif stripes
              for i in (temp_tif_list,):
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

