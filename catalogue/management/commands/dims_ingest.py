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

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from catalogue.models import *
from catalogue.dims_lib import dimsReader

class Command(BaseCommand):
  help = "Import into the catalogue all DIMS packages in a given folder, SPOT-5 OpticalProduct only"
  option_list = BaseCommand.option_list + (
      make_option('--folder', '-f', dest='folder', action='store',
          help='Scan the given folder, defaults to current.', default=os.getcwd()),
      make_option('--store_image', '-i', dest='store_image', action='store_true',
          help='Store the original image data extracted from the package.', default=os.getcwd()),
      make_option('--glob', '-g', dest='glob', action='store',
          help='A shell glob pattern for files to ingest.', default='*.tar.gz'),
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB.', default=False),
      make_option('--owner', '-o', dest='owner', action='store',
          help='Name of the Institution package owner. Defaults to: Satellite Applications Centre', default='Satellite Applications Centre'),
      make_option('--creating_software', '-s', dest='creating_software', action='store',
          help='Name of the creating software. Defaults to: SARMES1', default='SARMES1'),
      make_option('--license', '-l', dest='license', action='store', default='SAC Commercial License',
          help='Name of the license. Defaults to: SAC Commercial License'),
  )

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

    # Get the mandatory params or die!
    try:
      software = CreatingSoftware.objects.get(name=software)
    except CreatingSoftware.DoesNotExists:
      print 'CreatingSoftware %s does not exists: aborting' % software
      return
    try:
      license = License.objects.get(name=license)
    except License.DoesNotExists:
      print 'License %s does not exists: aborting' % license
      return
    try:
      owner = Institution.objects.get(name=owner)
    except Institution.DoesNotExist:
      print 'Institution %s does not exists: aborting' % owner
      return


    def verblog(msg, level = 1):
      if verbose > level:
        print msg

    verblog('Getting verbose (level=%s)... ' % verbose)

    # Build the path
    path          = os.path.join(folder, globparm)
    package_list  = glob.glob(path)

    verblog("found %d packages in %s" % (len(package_list), path))

    for package in package_list:

      verblog("ingesting %s" % package)
      reader = dimsReader(package)
      products = reader.get_products()
      verblog("found %d products" % len(products))

      for product_code, product_data in products.items():
        verblog("product %s" % product_code)
        verblog(product_data, 3)

        verblog("processing product %s" % product_code)

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

        data = {
          'metadata' : product_data['xml'].read(),
          'spatial_coverage' : product_data.get('spatial_coverage'),
          'product_id' : product_data['metadata'].get('file_identifier')[:58],
          'radiometric_resolution' : GDT_dict[dataset.GetRasterBand(1).DataType],
          'band_count' : dataset.RasterCount,
          'cloud_cover' : product_data['metadata'].get('cloud_cover'),
          'owner' : owner,
          'license' : license,
          'creating_software' : software,
          'quality' : Quality.objects.get_or_create(name=product_data['metadata'].get('image_quality_code'))[0],
        }

        # Close dataset
        dataset = None

        verblog('Ingesting data:', 3)
        verblog(data, 3)

        # Check if it's still in catalogue:
        try:
          op = GenericProduct.objects.get(product_id=data.get('product_id')).getConcreteInstance()
          verblog('alredy in catalogue: updating')
          op.__dict__.update(data)
        except ObjectDoesNotExist:
          op = OpticalProduct(**data)
          verblog('not in catalogue: creating')
          try:
            op.productIdReverse(True)
          except Exception, e:
            raise CommandError('Cannot get all mandatory data from product id %s (%s)' % (product_code, e))
            # ?? op.setSacProductId()

        if not test_only:
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
            handle = open(jpeg_thumb, 'w+')
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
              verblog("storing main image for product %s: %s" % (product_code, main_image))
            else:
              # Remove imagery
              os.remove(temp_main_image)
            print 'Product %s imported.' % product_code
          except Exception, e:
            # Raise
            os.remove(temp_main_image)
            raise CommandError('Cannot import: %s' % e)
        else:
          os.remove(temp_main_image)
          verblog("testing only: processing %s skipped" % product_code)


