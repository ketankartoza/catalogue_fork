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


['CAT_ID',
 'IT_CAT_ID',
 'UDP',
 'CCP',
 'BFP',
 'TILE_ID',
 'SUNAZMT',
 'SUNELVN',
 'ACQ_DATE',
 'IND_ANGLE',
 'AZMT_ANGLE',
 'HORZ_UNCER',
 'CRAFT_ID',
 'VW_ANGLE',
 'BAND1',
 'BAND2',
 'BAND3',
 'BAND4',
 'BAND5',
 'PATH']


"""
#import os
#import glob
#import re
from optparse import make_option
#from osgeo import gdal
import tempfile
#from subprocess import call

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.geometries import Polygon

from catalogue.models import *
from catalogue.dims_lib import dimsWriter


class Command(BaseCommand):
  help = "Import into the catalogue all RapidEye packages"
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
          help='Name of the Institution package owner. Defaults to: RapidEye.', default='RapidEye'),
      make_option('--creating_software', '-s', dest='creating_software', action='store',
          help='Name of the creating software. Defaults to: RapidEye.', default='RapidEye'),
      make_option('--year', '-y', dest='year', action='store',
          help='Year to ingest (4 digits). Defaults to: current year', default=datetime.datetime.strftime(datetime.datetime.now(), '%Y')),
      make_option('--day', '-d', dest='day', action='store',
          help='Day to ingest (2 digits). Defaults to None', default=None),
      make_option('--month', '-m', dest='month', action='store',
          help='Month to ingest (2 digits). Defaults to: current month', default=datetime.datetime.strftime(datetime.datetime.now(),'%m')),
      make_option('--license', '-l', dest='license', action='store', default='SAC Commercial License',
          help='Name of the license. Defaults to: SAC Commercial License'),
      make_option('--area', '-a', dest='polygon', action='store',
          help='Area of interest, images which are external to this area will not be imported (WKT Polygon, SRID=4326)'),
      make_option('--quality', '-q', dest='quality', action='store',
          help='Quality code (will be created if does not exists). Defaults to: Unknown'),
      make_option('--processing_level', '-r', dest='processing_level', action='store',
          help='Processing level code (will be created if does not exists). Defaults to: 3A'),
  )


  @staticmethod
  def build_product_id(package):
    """
    Creates the product_id
    """
    import ipy; ipy.shell()


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
    username          = options.get('username')
    password          = options.get('password')
    base_url          = options.get('base_url')
    year              = options.get('year')
    day               = options.get('day')
    month             = options.get('month')
    test_only         = options.get('test_only')
    verbose           = int(options.get('verbosity'))
    license           = options.get('license')
    owner             = options.get('owner')
    software          = options.get('creating_software')
    clip              = options.get('polygon')
    quality           = options.get('quality')
    processing_level  = options.get('processing_level')

    area_of_interest  = None

    def verblog(msg, level = 1):
      if verbose > level:
        print msg

    verblog('Getting verbose (level=%s)... ' % verbose)

    try:
      # Try connection
      try:
        verblog('Opening connection...')
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, base_url, username, password)
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        opener.open(base_url)
        urllib2.install_opener(opener)
        verblog('Connection open.')
      except urllib2.HTTPError, e:
        raise CommandError('Unable to establish a connection: %s.' % e)

      # Validate area_of_interest
      if clip:
        try:
          area_of_interest = Polygon(clip)
          if not area_of_interest.area:
            raise CommandError('Unable to create the area of interest polygon: invalid polygon.')
          if not area_of_interest.geom_type.name == 'Polygon':
            raise CommandError('Unable to create the area of interest polygon: not a polygon.')
        except Exception, e:
          raise CommandError('Unable to create the area of interest polygon: %s.' % e)
        verblog('Area of interest filtering activated.')

      # Get the params
      try:
        software = CreatingSoftware.objects.get_or_create(name=software, defaults={'version' : 0})[0]
      except CreatingSoftware.DoesNotExists:
        raise CommandError, 'Creating Software %s does not exists and cannot create: aborting' % software
      try:
        license = License.objects.get_or_create(name=license, defaults={'type' : License.LICENSE_TYPE_COMMERCIAL, 'details' : license})[0]
      except License.DoesNotExists:
        raise CommandError, 'License %s does not exists and cannot create: aborting' % license

      try:
        owner = Institution.objects.get_or_create(name=owner, defaults={'address1': '','address2': '','address3': '','post_code': '', })[0]
      except Institution.DoesNotExist:
        verblog('Institution %s does not exists and cannot be created.' % owner)
        raise CommandError, 'Institution %s does not exists and cannot create: aborting' % owner

      try:
        quality = Quality.objects.get_or_create(name=quality)[0]
      except Quality.DoesNotExist:
        verblog('Quality %s does not exists and cannot be creates, it will be read from metadata.' % quality)
        raise CommandError, 'Quality %s does not exists and cannot be created: aborting' % quality

      try:
        processing_level = ProcessingLevel.objects.get_or_create(abbreviation=processing_level, defaults={'name' : "Level %s" % processing_level})[0]
      except ProcessingLevel.DoesNotExist:
        verblog('ProcessingLevel %s does not exists and cannot be created.' % processing_level)
        raise CommandError, 'ProcessingLevel %s does not exists and cannot create: aborting' % processing_level

      # Builds the path:  https://delivery.rapideye.de/catalogue/shapes/2011/03/accum_itt_shape_2011-03.shp
      if day:
        base_index_url = os.path.join(base_url, 'shapes', year, month, day, 'itt_shape_%s-%s' % (year, month))
        verblog('Day filtering activated.')
        base_index_url = "%s-%s" % (base_index_url,day)
      else:
        base_index_url = os.path.join(base_url, 'shapes', year, month, 'accum_itt_shape_%s-%s' % (year, month))

      verblog('Index base url: %s. (+ extension)' % base_index_url)

      try:
        imported = 0
        for package in Command.fetch_geometries(base_index_url, area_of_interest):
          verblog("Ingesting %s" % package)

          # Do the ingestion here...
          data = {
            'metadata' : '',
            'spatial_coverage' : package.geom,
            'product_id' : Command.build_product_id(package),
            'radiometric_resolution' : 16,
            'band_count' : 5,
            'cloud_cover' : package.fields['CCP'],
            'owner' : record_owner,
            'license' : license,
            'creating_software' : software,
            'quality' : quality,
            'processing_level' : processing_level,
          }

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

          try:
            op.save()
            # Store thumbnail
            thumbnails_folder = os.path.join(settings.THUMBS_ROOT, op.thumbnailPath())
            try:
              os.makedirs(thumbnails_folder)
            except:
              pass
            # Download original geotiff thumbnail and creates a thumbnail

            jpeg_thumb = os.path.join(thumbnails_folder, op.product_id + ".jpg")
            handle = open(jpeg_thumb, 'wb+')
            thumbnail.urllib2.urlopen(feature['PATH'])
            handle.write(thumbnail.read())
            thumbnail.close()
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
            imported = imported + 1
          except Exception, e:
            raise CommandError('Cannot import: %s' % e)


        verblog("%s packages imported" % imported)

        if test_only:
          transaction.rollback()
          verblog("Testing only: transaction rollback.")
        else:
          transaction.commit()
          verblog("Committing transaction.")
      except Exception, e:
        raise CommandError('Uncaught exception: %s' % e)


    except Exception, e:
      transaction.rollback()
      raise CommandError("%s" % e)

