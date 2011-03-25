"""
OS4EO ordering

http://196.35.94.243/os4eo

"""

import os
from optparse import make_option
import tempfile
import subprocess
from SOAPpy import WSDL

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from catalogue.models import *


# Hardcoded constants
WS_ENDPOINT = 'http://196.35.94.243/os4eo?wsdl'

class Command(BaseCommand):
  help = "Place orders"
  option_list = BaseCommand.option_list + (
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB.', default=False),
  )


  @transaction.commit_manually
  def handle(self, *args, **options):
    """ command execution """
    test_only             = options.get('test_only')
    verbose               = int(options.get('verbosity'))


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
      # Try connection
      try:
        verblog('Opening connection...', 2)
        verblog('FTP: connecting to %s ...' % BASE_DOMAIN, 2)
        ftp = ftplib.FTP(BASE_DOMAIN)
        ftp.login()
        ftp.cwd(BASE_FOLDER)

        # Get index
        verblog('Starting index dowload...', 2)
        directories=[]
        ftp.retrlines('LIST', add_directory)
        directories.sort()
        # Read .ini file
        last_folder = None
        last_package = None
        if not rcfileskip:
          try:
            rc = open(RC_FILE, 'r')
            last_folder = rc.readline().split('=')[1][:-1]
            last_package = rc.readline().split('=')[1][:-1]
            verblog('Last folder: %s' % last_folder, 2)
            verblog('Last package: %s' % last_package, 2)
            rc.close()
            try:
              directories = directories[directories.index(last_folder):]
            except ValueError:
              verblog('Cannot find last_folder %s in list' % last_folder, 2)
          except:
            verblog('Cannot read rcfile %s' % RC_FILE, 2)
        else:
          verblog('Skipping rc file.', 2)

      except Exception, e:
        raise CommandError('Unable to establish a connection: %s.' % e)

      # Get the params
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
        # Get first dir
        for ftp_dir in directories:
          if maxproducts and imported >= maxproducts:
            verblog("Maxproducts %s exceeded: exiting" % maxproducts, 2)
            break
          last_folder = ftp_dir
          # Scan directory
          verblog('Scanning folder: %s' % ftp_dir, 2)
          package_list =  ftp.nlst(ftp_dir)
          #verblog('package_list: %s' % package_list, 2)
          package_list = [f for f in package_list if f.split('.')[-4] in ALLOWED_ZONES and f[-3:] == 'hdf']
          package_list.sort()
          # Seek to last_package position
          try:
            package_list = package_list[package_list.index(last_package) + 1:]
          except ValueError:
            verblog('Cannot find last_package %s in list' % last_package, 2)

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
            ftp.retrbinary('RETR %s' % package, open(tmp_image, 'wb').write)

            # Parse metadata with GDAL
            img = gdal.Open(tmp_image)
            metadata = img.GetMetadata_Dict()

            # Mission
            mission = MISSION_MAP[metadata['ASSOCIATEDPLATFORMSHORTNAME']]
            mission_sensor = MISSION_SENSOR_MAP[metadata['ASSOCIATEDPLATFORMSHORTNAME']]
            software = metadata['HDFEOSVersion']

            try:
              #software = CreatingSoftware.objects.get_or_create(name=software, defaults={'version': 0})[0]
              software = CreatingSoftware.objects.get_or_create(name=software, defaults={'version': 0})[0]
            except CreatingSoftware.DoesNotExist:
              raise CommandError, 'Creating Software %s does not exists and cannot create: aborting' % software

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
              'creating_software': software,
              'quality': quality,
              'original_product_id': metadata['LOCALGRANULEID'],
              'geometric_resolution_x': geometric_resolution,
              'geometric_resolution_y': geometric_resolution,
              'product_acquisition_end': datetime.datetime.strptime(metadata['RANGEENDINGDATE'] + ' ' + metadata['RANGEENDINGTIME'], '%Y-%m-%d %H:%M:%S.%f'),
            }
            verblog(data, 2)

            # Check if it's already in catalogue:
            try:
              op = OpticalProduct.objects.get(product_id=data.get('product_id')).getConcreteInstance()
              verblog('Alredy in catalogue: updating.', 2)
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
                rc.write('last_folder=%s\n' % ftp_dir)
                rc.write('last_package=%s\n' % package)
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

