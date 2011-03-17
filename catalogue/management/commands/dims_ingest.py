"""
Dims ingestion command

Ingestion of DIMS SPOT-5 OpticalProduct only

"""

import os
import glob
import re
from optparse import make_option
from osgeo import gdal
import tempfile
from subprocess import call

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.geos import Polygon
from django.contrib.gis.gdal import SpatialReference

from catalogue.models import *
from catalogue.dims_lib import dimsReader


class Command(BaseCommand):
  help = "Import into the catalogue all DIMS packages in a given folder, SPOT-5 OpticalProduct only"
  option_list = BaseCommand.option_list + (
      make_option('--folder', '-f', dest='folder', action='store',
          help='Scan the given folder, defaults to current.', default=os.getcwd()),
      make_option('--store_image', '-i', dest='store_image', action='store_true',
          help='Store the original image data extracted from the package.', default=True),
      make_option('--glob', '-g', dest='glob', action='store',
          help='A shell glob pattern for files to ingest.', default='*.tar.gz'),
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB.', default=False),
      make_option('--owner', '-o', dest='owner', action='store',
          help='Name of the Institution package owner. Metadata will be used if available, the program will fail if no metadata are available and no name is provided.', default=None),
      make_option('--creating_software', '-s', dest='creating_software', action='store',
          help='Name of the creating software. Defaults to: SARMES1', default='SARMES1'),
      make_option('--license', '-l', dest='license', action='store', default='SAC Commercial License',
          help='Name of the license. Defaults to: SAC Commercial License'),
      make_option('--keep', '-k', dest='keep', action='store_true', default=False,
          help='Do not delete the package after a successful import.'),
  )

  @transaction.commit_manually
  def handle(self, *args, **options):
    """ command execution """
    folder        = options.get('folder')
    globparm      = options.get('glob')
    test_only     = options.get('test_only')
    store_image   = options.get('store_image')
    verbose       = int(options.get('verbosity'))
    license       = options.get('license')
    owner         = options.get('owner')
    software      = options.get('creating_software')
    keep          = options.get('keep')

    def verblog(msg, level = 1):
      if verbose > level:
        print msg

    verblog('Getting verbose (level=%s)... ' % verbose)
    verblog('Creating software: %s' % software)
    verblog('Owner: %s' % owner)
    verblog('License: %s' % license)

    # Get the params
    try:
      software = CreatingSoftware.objects.get_or_create(name=software, defaults={'version' : 0})[0]
    except CreatingSoftware.DoesNotExists:
      raise CommandError, 'Creating Software %s does not exists and cannot create: aborting' % software
    try:
      license = License.objects.get_or_create(name=license, defaults={'type' : License.LICENSE_TYPE_COMMERCIAL, 'details' : license})[0]
    except License.DoesNotExists:
      raise  CommandError, 'License %s does not exists and cannot create: aborting' % license

    # Institution is optional
    if owner:
      try:
        owner = Institution.objects.get_or_create(name=owner, defaults={'address1': '','address2': '','address3': '','post_code': '', })[0]
      except Institution.DoesNotExist:
        verblog('Institution %s does not exists and cannot be created, it will be read from metadata.' % owner)
    else:
      verblog('Institution was not specified, it will be read from metadata.')

    # Build the path
    path          = os.path.join(folder, globparm)
    package_list  = glob.glob(path)

    verblog("Found %d packages in %s" % (len(package_list), path))

    try:
      for package in package_list:
        verblog("Ingesting %s" % package)
        reader = dimsReader(package)
        products = reader.get_products()
        verblog("Found %d products" % len(products))

        for product_code, product_data in products.items():
          verblog("Product %s" % product_code)
          verblog(product_data, 2)

          verblog("Processing product %s" % product_code)

          # Extracts data from imagery
          temp_main_image = tempfile.mktemp('.tif')
          fh = open(temp_main_image, 'wb+')
          fh.write(product_data['image'].read())
          fh.close()
          dataset = gdal.Open(temp_main_image)
          gcps = dataset.GetGCPs()
          if gcps is None or len(gcps) == 0:
              raise CommandError('No GCPs found on file ' + filename)
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

          # Retrieve
          # GDAL data type http://www.gdal.org/gdal_8h-source.html
          GDT_dict = {
            #GDT_Unknown =
            0 : 0,
            #GDT_Byte =
            1 : 8,
            #GDT_UInt16 =
            2 : 16,
            #GDT_Int16 =
            3 : 16,
            #GDT_UInt32 =
            4 : 32,
            #GDT_Int32 =
            5 : 32,
            #GDT_Float32 =
            6 : 32,
            #GDT_Float64 =
            7 :64,
            #GDT_CInt16 =
            8 :16,
            #GDT_CInt32 =
            9 : 32,
            #GDT_CFloat32 =
            10 : 32,
            #GDT_CFloat64 =
            11 : 64,
            #GDT_TypeCount = 12 : ,
          }

          # Reads Institution details from metadata, name is mandatory
          # Creates Institution if not found
          if not owner:
            try:
              record_owner = Institution.objects.get_or_create(name=product_data['metadata']['institution_name'], defaults={
                    'address1' : product_data['metadata'].get('institution_address', ''),
                    'address2' : product_data['metadata'].get('institution_city', ''),
                    'address3' : "%s %s" % (product_data['metadata'].get('institution_region', ''),  product_data['metadata'].get('institution_country', '')),
                    'post_code' : product_data['metadata'].get('institution_postcode', ''),
                })[0]
            except KeyError, e:
              raise CommandError('Cannot create Institution record for product id %s (%s)' % (product_code, e))

          else:

            record_owner = owner

          data = {
            'metadata' : product_data['xml'].read(),
            'spatial_coverage' : product_data.get('spatial_coverage'),
            'product_id' : product_data['metadata'].get('file_identifier')[:58],
            'radiometric_resolution' : GDT_dict[dataset.GetRasterBand(1).DataType],
            'band_count' : dataset.RasterCount,
            'cloud_cover' : product_data['metadata'].get('cloud_cover'),
            'owner' : record_owner,
            'license' : license,
            'creating_software' : software,
            'quality' : Quality.objects.get_or_create(name=product_data['metadata'].get('image_quality_code'))[0],
          }

          # Read spatial_coverage from gdal if none
          if not data.get('spatial_coverage'):
            poly_points = [(gcp.GCPX, gcp.GCPY) for gcp in gcps]
            poly_points.append(poly_points[0])
            data['spatial_coverage'] = Polygon(poly_points)
            # Used here only, main record projection is set from product_id
            srs = SpatialReference(dataset.GetGCPProjection())
            data['spatial_coverage'].set_srid(srs.srid)
            verblog('Got spatial_coverage from image: %s' % data['spatial_coverage'].ewkt)


          # Close dataset
          dataset = None

          verblog('Ingesting data:', 3)
          verblog(data, 3)

          # Check if it's already in catalogue:
          try:
            op = OpticalProduct.objects.get(product_id=data.get('product_id')).getConcreteInstance()
            verblog('Alredy in catalogue: updating')
            is_new = False
            op.__dict__.update(data)
          except ObjectDoesNotExist:
            op = OpticalProduct(**data)
            verblog('Not in catalogue: creating')
            is_new = True
            try:
              op.productIdReverse(True)
            except Exception, e:
              transaction.rollback()
              raise CommandError('Cannot get all mandatory data from product id %s (%s)' % (product_code, e))
              # ?? op.setSacProductId()

          try:
            op.save()
            # Store thumbnail
            thumbnails_folder = os.path.join(settings.THUMBS_ROOT, op.thumbnailPath())
            try:
              os.makedirs(thumbnails_folder)
            except:
              pass
            jpeg_thumb = os.path.join(thumbnails_folder, op.product_id + ".jpg")
            handle = open(jpeg_thumb, 'wb+')
            handle.write(product_data['thumbnail'].read())
            handle.close()
            # Store .wld file
            jpeg_wld   =  os.path.join(thumbnails_folder, op.product_id + ".wld")
            handle = open(jpeg_wld, 'w+')
            handle.write(wld)
            handle.close()
            # Store main image
            if store_image:
              main_image_folder = os.path.join(settings.IMAGERY_ROOT, op.imagePath())
              try:
                os.makedirs(main_image_folder)
              except:
                pass
              main_image = os.path.join(main_image_folder, op.product_id + ".tif")
              os.rename(temp_main_image, main_image)
              # -f option: overwrites existing
              call(["bzip2", "-f", main_image])
              verblog("Storing main image for product %s: %s" % (product_code, main_image))
            else:
              # Remove imagery
              os.remove(temp_main_image)
            if is_new:
              print 'Product %s imported.' % product_code
            else:
              print 'Product %s updated.' % product_code
            # Remove the package
            if keep:
              verblog('Keep flag is set: do not delete the package')
            else:
              os.remove(package)
              verblog('Package removed: %s' % product_data['path'])
          except Exception, e:
            # Raise
            transaction.rollback()
            raise CommandError('Cannot import: %s' % e)

      if test_only:
        transaction.rollback()
        verblog("Testing only: transaction rollback.")
      else:
        transaction.commit()
        verblog("Committing transaction.")
    except Exception, e:
      transaction.rollback()
      raise CommandError('Uncaught exception: %s' % e)


