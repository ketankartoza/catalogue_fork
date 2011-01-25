import os
from zipfile import ZipFile
from django.contrib.gis.gdal import *
import traceback
from settings import *
# python logging support to django logging middleware
import logging

def getFeaturesFromZipFile( zipfile, geometry, numFeatures = "all"):
  """ Takes a zip archive and extracts N features of the specified geometry type. """
  # inspect the zip file
  zippedShape = None
  try:
    logging.debug('Extracting...%s' % zipfile)
    zippedShape = ZipFile(zipfile)
    logging.debug('extract done...')
  except Exception, e:
    logging.debug( traceback.format_exc() )
    logging.debug("ZipFile Failed: %s" % e)
  # check if the contents of the archive are the usual 3 files with no subdirectories.
  logging.debug('checking zip contents are a shp, shx, dbf...')
  if any([f.endswith('/') for f in zippedShape.namelist()]):
    logging.debug( "Extract failed due to subdirs present" )
    raise RuntimeError('The archive contains subdirectories. Please zip only the shp, .shx, .dbf[, .prj] files.')
  extensionsList = [fullname.split(".")[-1] for fullname in zippedShape.namelist()]
  presentExtensions = set(extensionsList).intersection(set(["shp", "shx", "dbf"]))
  logging.debug('contents ok...')
  if len(presentExtensions) < 3:
    logging.debug( "Extract failed due to less than 3 files present in zip" )
    raise RuntimeError('At least one of .shp, .shx, .dbf is missing.')
  # extract - for Python 2.5. Python 2.6 has a nice ZipFile.extract()
  for each in zippedShape.namelist():
    destinationFile = os.path.join(SHP_UPLOAD_DIR, each)
    data = zippedShape.read(each)
    f = open(destinationFile, 'w')
    f.write(data)
    f.close()
  zippedShape.close()
  
  logging.debug( "Shapefiles written to  %s " % SHP_UPLOAD_DIR )
  shpName = [elem for elem in zippedShape.namelist() if "shp" in elem].pop()
  shpFileOnDiskPath = os.path.join(SHP_UPLOAD_DIR, shpName)
  logging.debug( "Uploaded shp is %s" % shpFileOnDiskPath )
  # load the shapefile in GeoDjango
  dataSource = None
  try:
    logging.debug('loading shapes as a datasource...')
    dataSource = DataSource(shpFileOnDiskPath)
  except Exception, e:
    logging.debug( str(traceback.format_exc()) )
    logging.debug( "datasource loading failed :-(" )
    logging.debug("Failed: %s" % e)
    raise RuntimeError ("Loading shp failed")
  logging.debug( "Datasource loaded ok" )
  
  # extract the first polygon if any
  firstLayer = None
  if dataSource[0].geom_type == geometry:
    logging.debug( "Extracting poly" )
    try:
      firstLayer = dataSource[0]
    except Exception, e:
      logging.debug( traceback.format_exc() )
      logging.debug( "" )
      logging.debug( "Crashed: %s" % e)
    logging.debug( "Extracting poly done" )
  else:
    logging.debug( "Failed - no polygon data" )
    # cleanup before exiting
    for each in zippedShape.namelist():
      logging.debug( "Failed - removing shps" )
      os.remove(os.path.join(SHP_UPLOAD_DIR, each))
    raise RuntimeError('The geometry ' + geometry + ' is not available in this shapefile.')
  
  # some info.
  logging.debug( "Zip archive name: " + zippedShape.filename )
  logging.debug( "Shapefile name: " + shpName )
  logging.debug( "Full datasource name: " + dataSource.name )
  logging.debug( "Number of available features: " + str(dataSource[0].num_feat ))
  logging.debug( "Geometry type: " + firstLayer.geom_type.name )
  logging.debug( "Number of extracted features: " + str(numFeatures) )
  
  # extract the N geometries, otherwise all of them
  if numFeatures != "all":
    geometriesList = [pt.wkt for pt in firstLayer.get_geoms()][0:numFeatures]
  else:
    geometriesList = [pt.wkt for pt in firstLayer.get_geoms()]
  
  # cleanup of dezipped files
  for each in zippedShape.namelist():
    logging.debug( "Failed - removing shps" )
    os.remove(os.path.join(SHP_UPLOAD_DIR, each))

  # return the data
  return geometriesList
