"""
Dims ingestion command
"""

import os
import glob
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError

from catalogue.models import *
from catalogue.dims_lib import dimsReader

class Command(BaseCommand):
  help = "Import into the catalogue all dims packages in a given folder"
  option_list = BaseCommand.option_list + (
      make_option('--folder', '-f', dest='folder', action='store',
          help='Scan the given folder, defaults to current.', default = os.getcwd()),
      make_option('--glob', '-g', dest='glob', action='store',
          help='A shell glob pattern for files to ingest.', default = '*.tar.gz'),
      make_option('--test_only', '-t', dest='test_only', action='store_true',
          help='Just test, nothing will be written into the DB. ', default = False),
  )

  def handle(self, *args, **options):
    """ command execution """
    folder        = options.get('folder')
    globparm      = options.get('glob')
    test_only     = options.get('test_only')
    verbose       = options.get('verbosity')

    # Build the path
    path          = os.path.join(folder, globparm)
    package_list  = glob.glob(path)

    if verbose:
      print "found %d packages in %s" % (len(package_list), path)

    for package in package_list:

      if verbose:
        print "ingesting %s" % package
      reader = dimsReader(package)
      products = reader.get_products()
      if verbose:
        print "found %d products" % len(products)

      for product_code, product_data in products.items():
        if verbose:
          print "product %s" % product_code
          if verbose > 1:
            print product_data

        if not test_only:
          if verbose:
            print "processing product %s" % product_code
            # Do the ingestion here....
            for p in ['product_date',
                      'processing_level',
                      'owner',
                      'license',
                      'spatial_coverage',
                      'projection',
                      'quality',
                      'creating_software',
                      'product_id',
                      'remote_thumbnail_url',
                      'mission',
                      'mission_sensor',
                      'sensor_type',
                      'acquisition_mode',
                      'product_acquisition_start',
                      'geometric_resolution_x',
                      'geometric_resolution_y']:
                pass

            op = OpticalProduct()

        else:
          if verbose:
            print "testing only: processing %s skipped" % product_code



