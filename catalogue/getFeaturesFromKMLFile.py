import os
from zipfile import ZipFile
from django.contrib.gis.gdal import *
import traceback
from settings import *
# python logging support to django logging middleware
import logging

def getFeaturesFromKML( zipfile, geometry, numFeatures = "all"):
  """ Takes a KML or KMZ file and extracts N features of the specified geometry type. """
  # inspect the KML file
  myGeomFile=None
  if zipfile.split(".")[1]=='kmz':
    try:
      logging.debug('Extracting...%s' % zipfile)
      tmp_zip = ZipFile(zipfile)
      #read first file in unzipped kmz, which is kml
      myGeomFile = tmp_zip.read(tmp_zip.namelist()[0])
      logging.debug('extract done...')
    except Exception, e:
      logging.debug( traceback.format_exc() )
      logging.debug("ZipFile Failed: %s" % e)
  else:
    #if plain KML file, read data
    tmp_data=open(zipfile,'r')
    myGeomFile=tmp_data.read()
    tmp_data.close()
    
  #temporary store unpacked files
  destinationFile = os.path.join(SHP_UPLOAD_DIR, zipfile)
  f = open(destinationFile, 'w')
  f.write(myGeomFile)
  f.close()
  
  dataSource = None
  try:
    logging.debug('loading KML as a datasource...')
    dataSource = DataSource(destinationFile)
  except Exception, e:
    logging.debug( str(traceback.format_exc()) )
    logging.debug( "datasource loading failed :-(" )
    logging.debug("Failed: %s" % e)
    raise RuntimeError ("Loading KML failed")
  logging.debug( "Datasource loaded ok" )
  
  # find polygon layers (polygon or polygon25d)
  poly_layer = [layer for layer in dataSource if layer.geom_type.name=='Polygon' or layer.geom_type.name=='Polygon25D']
  
  firstLayer = None
  if poly_layer:
    logging.debug( "Extracting poly" )
    try:
      firstLayer = poly_layer[0]
    except Exception, e:
      logging.debug( traceback.format_exc() )
      logging.debug( "" )
      logging.debug( "Crashed: %s" % e)
    logging.debug( "Extracting poly done" )
  else:
    logging.debug( "Failed - no polygon data" )
    os.remove(os.path.join(SHP_UPLOAD_DIR, zipfile))
    raise RuntimeError('The geometry ' + geometry + ' is not available in this KML.')
  
  logging.debug( "Full datasource name: " + dataSource.name )
  logging.debug( "Number of available features: " + str(dataSource[0].num_feat ))
  logging.debug( "Geometry type: " + firstLayer.geom_type.name )
  logging.debug( "Number of extracted features: " + str(numFeatures) )
  
  # extract the N geometries, otherwise all of them
  if numFeatures != "all":
    #if geos=True, geometry will be read as 2D, which is obligatory
    geometriesList = [pt.wkt for pt in firstLayer.get_geoms(geos=True)][0:numFeatures]
  else:
    geometriesList = [pt.wkt for pt in firstLayer.get_geoms(geos=True)]

  #clean up
  os.remove(os.path.join(SHP_UPLOAD_DIR, zipfile))
  # return the data
  return geometriesList
