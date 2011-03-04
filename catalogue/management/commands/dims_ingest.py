"""
Dims ingestion command

Ingestion of DIMS SPOT-5 OpticalProduct only

"""

import os
import glob
import re
from optparse import make_option
from PIL import Image
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from catalogue.models import *
from catalogue.dims_lib import dimsReader



class Command(BaseCommand):
  help = "Import into the catalogue all DIMS packages in a given folder, SPOT-5 OpticalProduct only"
  option_list = BaseCommand.option_list + (
      make_option('--folder', '-f', dest='folder', action='store',
          help='Scan the given folder, defaults to current.', default = os.getcwd()),
      make_option('--store_image', '-s', dest='store_image', action='store_true',
          help='Store the original image data extracted from the package.', default = os.getcwd()),
      make_option('--glob', '-g', dest='glob', action='store',
          help='A shell glob pattern for files to ingest.', default = '*.tar.gz'),
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB. ', default = False),
      make_option('--defaults', '-d', dest='defaults', action='store',
          help='Default key value pairs comma separated.'),
  )

  def handle(self, *args, **options):
    """ command execution """
    folder        = options.get('folder')
    globparm      = options.get('glob')
    test_only     = options.get('test_only')
    store_image   = options.get('store_image')
    verbose       = options.get('verbosity')

    def verblog(msg, level = 1):
      if verbose >= level:
        print msg

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
        verblog(product_data, 2)

        if not test_only:
          verblog("processing product %s" % product_code)

          # Extracts data from imagery
          # Dictionary
          mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}
          img = Image.open(product_data['image'])
          bands = img.getbands()

          # Retrieve
          data = {
            'metadata' : product_data['xml'].read(),
            'spatial_coverage' : product_data['metadata']['spatial_coverage'],
            'product_id' : product_data['metadata']['file_identifier'][:57],
            'radiometric_resolution' : mode_to_bpp[bands[0]],
            'band_count' : len(bands),
          }

          op = OpticalProduct(**data)
          op.productIdReverse()

          try:
            op.setSacProductId()
            op.save()
            # Store thumbnail
            thumb_dir = os.path.join(settings.THUMBS_ROOT, os.thumbnailPath())
            jpeg_thumb = os.path.join(thumb_dir, op.product_id + ".jpg")
            handle = open(jpeg_thumb, '+wb')
            handle.write(product_data['thumbnail'].read())
            handle.close()
            # Build .wld file
            tiff_thumb = os.path.join(thumb_dir, op.product_id + ".tif")
            cmd = "gdal_translate -of JPEG -co WORLDFILE=YES %s %s" % ( tiff_thumb, jpeg_thumb)
            os.system(cmd)
            # Clean away the tiff
            os.remove(tiff_thumb)
            # Store main image
            if store_image:
              main_image = ''
              verblog("storing main image for product %s: %s" % (product_code, main_image))
          except:

            raise

        else:
          if verbose:
            print "testing only: processing %s skipped" % product_code



