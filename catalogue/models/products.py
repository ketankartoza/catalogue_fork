from django.contrib.gis.db import models
from dictionaries import *
import logging
import os
import re
import datetime
import urllib2
from django.conf import settings
#for translation
from django.core.exceptions import ObjectDoesNotExist
# PIL and os needed for making small thumbs
from PIL import Image, ImageFilter, ImageOps

from django_dag.models import node_factory, edge_factory

from functools import wraps

from catalogue.utmzonecalc import utmZoneFromLatLon

# Read from settings
CATALOGUE_SCENES_PATH = getattr(settings, 'CATALOGUE_SCENES_PATH', "/mnt/cataloguestorage/scenes_out_projected_sorted/")

def runconcrete(func):
  """
  This decorator calls the method in the concrete subclass
  and raise an exception if the method is found only in a base
  GenericProduct abstract class
  """
  @wraps(func)
  def wrapper(self, *args, **kwargs):
    if [d for d in set(self.getConcreteInstance().__class__.__mro__).difference([self.__class__]) if func.__name__ in d.__dict__ and getattr(d, 'concrete', False)]:
      return getattr(self.getConcreteInstance(), func.__name__)(*args, **kwargs)
    raise NotImplementedError()
  return wrapper

class GenericProduct( node_factory('catalogue.ProductLink', base_model = models.Model ) ):
  """
  A generic model (following R-5.1-160 of DIMS system architecture document).

  @NOTE: this is not an abstract base class since we are using django multi-table
  inheritance. See http://docs.djangoproject.com/en/dev/topics/db/models/#id7

  see: signals, to set defaults product_acquisition_start
  """
  product_date          = models.DateTimeField(db_index=True)
  processing_level      = models.ForeignKey( ProcessingLevel )
  owner                 = models.ForeignKey( Institution )
  license               = models.ForeignKey( License )
  spatial_coverage      = models.PolygonField( srid=4326, help_text="Image footprint")
  projection            = models.ForeignKey( Projection )
  quality               = models.ForeignKey( Quality )
  creating_software     = models.ForeignKey( CreatingSoftware, null=False,blank=False )
  original_product_id   = models.CharField( max_length="255", null=True,blank=True )
  product_id            = models.CharField( help_text="SAC Formatted product ID", max_length="255", db_index=True,unique=True )
  product_revision      = models.CharField( max_length="255",null=True,blank=True )
  local_storage_path    = models.CharField( max_length=255, help_text="Location on local storage if this product is offered for immediate download.", null=True,blank=True)
  metadata              = models.TextField(help_text="An xml document describing all known metadata for this product.")
  remote_thumbnail_url  = models.TextField( max_length=255,null=True,blank=True, help_text="Location on a remote server where this product's thumbnail resides. The value in this field will be nulled when a local copy is made of the thumbnail.")

  # We need a flag to tell if this Product class can have instances (if it is not abstract)
  # this flas is also used in admin back-end to get the list of classes for OrderNotificationRecipients
  concrete              = False

  objects               = models.GeoManager()

  class Meta:
    """This is not an abstract base class although you should avoid dealing directly with it
    see http://docs.djangoproject.com/en/dev/topics/db/models/#id7
    """
    app_label= 'catalogue'
    abstract = False
    ordering = ('product_date',)

  def __unicode__( self ):
     if self.product_id:
        return u"%s" % self.product_id
     return u"Internal ID: %d" % self.pk

  @runconcrete
  def thumbnailPath( self ):
    """Returns the path (relative to whatever parent dir it is in) for the
      thumb for this file following the scheme <Sensor>/<YYYY>/<MM>/<DD>/
      The thumb itself will exist under this dir as <product_id>.jpg
    """
    pass

  def thumbnail(self, theSize):
    """Return a thumbnail for this product of size "small" - 16x16, "medium" - 200x200 or "large" - 400x400
        If a cached copy of the resampled thumb exists, that will be returned directly
        @param a string "small","medium" or "large" - defaults to small
        @return a PIL image object.
    """
    if theSize not in ["medium","large"]: theSize = "small"
    mySize = 16
    if theSize == "medium":
      mySize = 200
    elif theSize == "large":
      mySize = 400

    logging.info("showThumb : id " + self.product_id)
    myImageFile = os.path.join( self.thumbnailPath(), self.product_id + ".jpg" )
    myFileName = str(settings.THUMBS_ROOT) + "/" + myImageFile
    myThumbDir = os.path.join( settings.THUMBS_ROOT, self.thumbnailPath() )
    # Paths for cache of scaled down thumbs (to reduce processing load)
    myCacheThumbDir = os.path.join( settings.THUMBS_ROOT, "cache", theSize, self.thumbnailPath() )
    myCacheImage = os.path.join( myCacheThumbDir, self.product_id + ".jpg" )
    #
    # Check if there is a scaled down version already cached and just return that if there is
    #
    if os.path.isfile( myCacheImage ):
      myImage = Image.open( myCacheImage )
      return ( myImage )

    #
    # Cached minified thumb not available so lets make it!
    #

    # Hack to automatically fetch spot or other non local thumbs from their catalogue
    # and store them locally
    if self.remote_thumbnail_url:
      if not os.path.isdir( myThumbDir  ):
        logging.debug("Creating dir: %s" % myThumbDir)
        try:
          os.makedirs( myThumbDir )
        except OSError:
          logging.debug("Failed to make output directory...quitting")
          return "Failed to make output dir."
      logging.debug("Fetching image: %s" % self.remote_thumbnail_url)
      myOpener = urllib2.build_opener()
      myImagePage = myOpener.open(self.remote_thumbnail_url)
      myImage = myImagePage.read()
      logging.debug("Image fetched, saving as %s" % myImageFile)
      myWriter = open(os.path.join(settings.THUMBS_ROOT,myImageFile), "wb")
      myWriter.write(myImage)
      myWriter.close()
      self.remote_thumbnail_url=""
      self.save()
    # hack ends

    # Specify background colour, should be the same as div background
    myBackgroundColour = ( 255,255,255 )
    myAngle = 0
    myShadowFlag = False
    logging.info ( "Creating thumbnail of : " + myFileName )
    logging.info('Thumbnail path:   ' + str(settings.THUMBS_ROOT))
    logging.info('Media path    :   ' + str(settings.MEDIA_ROOT))
    logging.info('Project root path:' + str(settings.ROOT_PROJECT_FOLDER))
    myImage = None
    if not os.path.isfile(myFileName):
      #file does not exist so show an error icon
      #return HttpResponse("%s not found" % myFileName)
      myFileName = os.path.join(settings.MEDIA_ROOT, 'images','block_16.png')
      myImage = Image.open( myFileName )
      return ( myImage )

    try:
      myImage = Image.open( myFileName )
    except:
      #file is not valid for some reason so show an error icon
      myFileName = os.path.join(settings.MEDIA_ROOT, 'images','block_16.png')
      myImage = Image.open( myFileName )
      return ( myImage )

    if len( myImage.getbands() ) < 3:
      myImage = ImageOps.expand( myImage, border = 5, fill = ( 255 ) )
    else:
      myImage = ImageOps.expand( myImage, border = 5, fill = ( 255, 255, 255 ) )
    myBackground = None
    if myShadowFlag:
      myImage = dropShadow( myImage.convert( 'RGBA' ) ).rotate( myAngle , expand = 1 )
      myBackground = Image.new( 'RGBA', myImage.size, myBackgroundColour )
      myBackground.paste( myImage, ( 0, 0 ) , myImage )
    else:
      myBackground = Image.new( 'RGBA', myImage.size, myBackgroundColour )
      myBackground.paste( myImage, ( 0, 0 ) )
    myBackground.thumbnail( ( mySize, mySize ), Image.ANTIALIAS)

    # Now cache the scaled thumb for faster access next time...
    if not os.path.isdir( myCacheThumbDir  ):
      logging.debug("Creating dir: %s" % myCacheThumbDir)
      try:
        os.makedirs( myCacheThumbDir )
      except OSError:
        logging.debug("Failed to make output directory...quitting")
        return "Failed to make output dir"
    logging.debug( "Caching image : %s" % myCacheImage )
    myBackground.save( myCacheImage )
    return ( myBackground )

  def dropShadow(
    theImage,
    myOffset=( 5, 5 ),
    theBackground=( 49, 89, 125 ),
    theShadow=( 0, 0, 0, 100 ),
    theBorder = 8,
    theIterations = 5 ):

    # Create the myBackgrounddrop image -- a box in the theBackground colour with a
    # theShadow on it.
    myTotalWidth = theImage.size[ 0 ] + abs( myOffset[ 0 ] ) + 2 * theBorder
    myTotalHeight = theImage.size[ 1 ] + abs( myOffset[ 1 ] ) + 2 * theBorder
    myBackground = Image.new( theImage.mode, ( myTotalWidth, myTotalHeight ), theBackground )

    # Place the theShadow, taking into account the myOffset from the image
    theShadowLeft = theBorder + max( myOffset[ 0 ], 0 )
    theShadowTop = theBorder + max( myOffset[ 1 ], 0 )
    myBackground.paste(theShadow, [ theShadowLeft, theShadowTop, theShadowLeft + theImage.size[ 0 ], theShadowTop + theImage.size[ 1 ] ] )

    # Apply the filter to blur the edges of the theShadow.  Since a small kernel
    # is used, the filter must be applied repeatedly to get a decent blur.
    n = 0
    while n < theIterations:
      myBackground = myBackground.filter( ImageFilter.BLUR )
      n += 1

    # Paste the input image onto the theShadow myBackgrounddrop
    myImageLeft = theBorder - min( myOffset[ 0 ], 0 )
    myImageTop = theBorder - min( myOffset[ 1 ], 0 )
    myBackground.paste( theImage, ( myImageLeft, myImageTop ) )

    return myBackground

  @runconcrete
  def imagePath( self ):
    """
    Returns the path (relative to whatever parent dir it is in) for the
    image itself following the scheme <Sensor>/<processinglevel>/<YYYY>/<MM>/<DD>/
    The image itself will exist under this dir as <product_id>.tif.bz2
    """
    # Checks method is in concrete class
    pass

  def imageUrl( self ):
    """Returns a path to the actual imagery data as a url. You need to have
    apache set up so share this directory. If no file is encountered at the computed path,
    None will be returned"""
    myUrl = settings.IMAGERY_URL_ROOT + self.imagePath() + "/" + self.product_id + ".tif.bz2"
    myPath = os.path.join( settings.IMAGERY_ROOT, self.imagePath(), self.product_id + ".tif.bz2" )
    if os.path.isfile( myPath ):
      return myUrl
    else:
      return None

  def rawImageUrl( self ):
    """Returns a path to the actual RAW imagery data as a url. You need to have
    apache set up so share this directory. If no file is encountered at the computed path,
    None will be returned"""
    myPath = os.path.join( settings.IMAGERY_ROOT, self.imagePath(), self.product_id + ".bz2" )
    myLevel = self.processing_level.abbreviation
    myLevel = myLevel.replace( "L","" )
    myPath = myPath.replace( myLevel, "1Aa" )
    myUrl = settings.IMAGERY_URL_ROOT + self.imagePath() + "/" + self.product_id + ".bz2"
    myUrl = myUrl.replace( myLevel, "1Aa" )
    logging.info("Raw Image Path: %s" % myPath )
    logging.info("Raw Image Url: %s" % myUrl )
    if os.path.isfile( myPath ):
      return myUrl
    else:
      return None

  def getConcreteProduct( self ):
    """ Downcast a product to its subtype using technique described here:
        http://docs.djangoproject.com/en/dev/topics/db/models/#id7
        @return Object, String :
        Object : A concrete subtype of GenericProduct e.g an OpticalProduct
        or a RadarProduct etc. None returned if the object could not be found.
        String : e.g. "Optical", "Radar" etc representing what type of
        object was found.
        """
    try:
      return self.genericimageryproduct.genericsensorproduct.opticalproduct, "Optical"
    except:
      pass
    try:
      return self.genericimageryproduct.genericsensorproduct.radarproduct, "Radar"
    except:
      pass
    try:
      return self.genericimageryproduct, "Imagery"
    except:
      pass
    try:
      return self.geospatialproduct.ordinalproduct, "Ordinal"
    except:
      pass
    try:
      return self.geospatialproduct.continuousproduct, "Continuous"
    except:
      pass

    # ABP: raise exception instead of returning None, "Error - product not found"
    raise ObjectDoesNotExist()


  def getConcreteInstance( self ):
    """
    Returns the concrete product instance
    """
    return self.getConcreteProduct()[0]

  @runconcrete
  def setSacProductId( self ):
    """A sac product id adheres to the following format:

    SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL

    """
    pass

  @runconcrete
  def productIdReverse(self, force=False):
    """
    Parse a product_id and populates instance fields
    If force is set, the procedure will try to create
    missing bits
    """
    pass

  def tidySacId( self ):
    """Return a tidy version of the SAC ID for use on web pages etc.

       Normal: S5-_HRG_J--_CAM2_0118-_00_0418-_00_090403_085811_L1A-_ORBIT-

       Tidy:   S5 HRG J CAM2 0118 00 0418  00 090403 085811

       This is so that we can wrap the id nicely in small spaces etc."""
    myTokens = self.product_id.split("_")
    myUsedTokens = myTokens[0:9]
    myNewString = " ".join(myUsedTokens).replace("-","")
    return myNewString

  def pad( self, theString, theLength):
    myLength = len (theString)
    myString = theString + "-"*(theLength-myLength)
    return myString

  def zeroPad( self, theString, theLength):
    myLength = len (theString)
    myString = "0"*(theLength-myLength) + theString
    return myString

  def getUTMZones(self,theBuffer=0):
    """ return UTM zones which overlap this product
    theBuffer - specifies how many adjecent zones to return"""

    return set(utmZoneFromLatLon(*self.spatial_coverage.extent[:2],theBuffer=theBuffer)+utmZoneFromLatLon(*self.spatial_coverage.extent[2:],theBuffer=theBuffer))


class ProductLink (edge_factory('catalogue.GenericProduct', concrete = False, base_model = models.Model)):
  """
  Links between products
  """
  class Meta:
    app_label= 'catalogue'


###############################################################################

class GenericImageryProduct( GenericProduct ):
  """
  Generic Imagery product, it is always a composite aggregated products
  see: signals, to set geometric_resolution defaults and average
  """
  geometric_resolution                = models.FloatField( help_text="Geometric resolution")
  geometric_resolution_x              = models.FloatField( help_text="Geometric resolution in mm (x direction)")
  geometric_resolution_y              = models.FloatField( help_text="Geometric resolution in mm (y direction)")
  radiometric_resolution              = models.IntegerField( help_text="Bit depth of image e.g. 16bit")
  band_count                          = models.IntegerField( help_text="Number of spectral bands in product")

  # We need a flag to tell if this Product class can have instances (if it is not abstract)
  concrete              = True

  class Meta:
    app_label= 'catalogue'

###############################################################################

class GenericSensorProduct( GenericImageryProduct ):
  """
  Multitable inheritance class to hold common fields for satellite imagery
  """
  acquisition_mode                    = models.ForeignKey(AcquisitionMode ) #e.g. M X T J etc
  product_acquisition_start           = models.DateTimeField(db_index=True)
  product_acquisition_end             = models.DateTimeField(null=True, blank=True, db_index=True)
  geometric_accuracy_mean             = models.FloatField(null=True, blank=True )
  geometric_accuracy_1sigma           = models.FloatField(null=True, blank=True )
  geometric_accuracy_2sigma           = models.FloatField(null=True, blank=True )
  radiometric_signal_to_noise_ratio   = models.FloatField(null=True, blank=True )
  radiometric_percentage_error        = models.FloatField(null=True, blank=True )
  spectral_accuracy                   = models.FloatField( help_text="Wavelength Deviation", null=True, blank=True )
  orbit_number                        = models.IntegerField(null=True, blank=True)
  path                                = models.IntegerField(null=True, blank=True) #K Path Orbit
  path_offset                         = models.IntegerField(null=True, blank=True)
  row                                 = models.IntegerField(null=True, blank=True) #J Frame Row
  row_offset                          = models.IntegerField(null=True, blank=True)
  offline_storage_medium_id           = models.CharField(max_length=12, help_text="Identifier for the offline tape or other medium on which this scene is stored", null=True,blank=True )
  online_storage_medium_id            = models.CharField(max_length=36, help_text="DIMS Product Id as defined by Werum e.g. S5_G2_J_MX_200902160841252_FG_001822",null=True,blank=True )

  # We need a flag to tell if this Product class can have instances (if it is not abstract)
  concrete              = False

  class Meta:
    """This is not an abstract base class although you should avoid dealing directly with it
    see http://docs.djangoproject.com/en/dev/topics/db/models/#id7
    """
    app_label= 'catalogue'
    abstract = False

  def imagePath( self ):
    """Returns the path (relative to whatever parent dir it is in) for the
      image itself following the scheme <Sensor>/<processinglevel>/<YYYY>/<MM>/<DD>/
      The image itself will exist under this dir as <product_id>.tif.bz2"""
    return os.path.join( self.acquisition_mode.sensor_type.mission_sensor.mission.abbreviation,
                    str( self.processing_level.abbreviation),
                    str( self.product_acquisition_start.year ),
                    str( self.product_acquisition_start.month ),
                    str( self.product_acquisition_start.day ) )


  def thumbnailPath( self ):
    """Returns the path (relative to whatever parent dir it is in) for the
      thumb for this file following the scheme <Sensor>/<YYYY>/<MM>/<DD>/
      The thumb itself will exist under this dir as <product_id>.jpg"""
    return os.path.join( self.acquisition_mode.sensor_type.mission_sensor.mission.abbreviation,
                    str( self.product_acquisition_start.year ),
                    str( self.product_acquisition_start.month ),
                    str( self.product_acquisition_start.day ) )

  def setSacProductId( self ):
    """
      #A sac product id adheres to the following format:

      #SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL

      Where:
      SAT    Satellite or mission          mandatory
      SEN    Sensor                        mandatory
      MOD    Acquisition mode              mandatory
      TYP    Type                          mandatory
      KKKK   Orbit path reference          optional?
      KS     Path shift                    optional?
      JJJJ   Orbit row reference           optional?
      JS     Row shift                     optional?
      YYMMDD Acquisition date              mandatory
      HHMMSS Scene centre acquisition time mandatory
      LEVL   Processing level              mandatory
      PROJTN Projection                    mandatory

      Examples:

      S5-_HRG_J--_CAM2_0118-_00_0418-_00_090403_085811_L1A-_ORBIT-
      S5-_HRG_J--_CAM2_0118-_00_0418-_00_090403_085811_L3Aa_UTM34S

      When this function is called it will also check if there is a
      thumbnail for this scene and rename it from the old thumb
      prefix to the new one.
      """
    myPreviousId = self.product_id #store for thumb renaming just now
    myList = []
    myList.append( self.pad( self.acquisition_mode.sensor_type.mission_sensor.mission.abbreviation, 3 ) )
    myList.append( self.pad( self.acquisition_mode.sensor_type.mission_sensor.abbreviation, 3 ) )
    myList.append( self.pad( self.acquisition_mode.abbreviation, 3 ) )
    myList.append( self.pad( self.acquisition_mode.sensor_type.abbreviation, 3 ) )
    myList.append( self.zeroPad( str( self.path ),4 ) )
    myList.append( self.zeroPad( str( self.path_offset ),2 ) )
    myList.append( self.zeroPad( str( self.row ),4 ) )
    myList.append( self.zeroPad( str( self.row_offset ),2 ) )
    myDate = str( self.product_acquisition_start.year )[2:4]
    myDate += self.zeroPad( str( self.product_acquisition_start.month ),2 )
    myDate += self.zeroPad( str( self.product_acquisition_start.day ),2 )
    myList.append( myDate )
    myTime = self.zeroPad( str( self.product_acquisition_start.hour ),2)
    myTime += self.zeroPad( str( self.product_acquisition_start.minute ),2)
    myTime += self.zeroPad( str( self.product_acquisition_start.second ),2)
    myList.append( myTime )
    myList.append( "L" + self.pad( self.processing_level.abbreviation, 3 ) )
    # ABP: changed from 4 to 6 (why was it 4 ? UTM34S is 6 chars)
    myList.append( self.pad( self.projection.name,6 ) )
    #print "Product SAC ID %s" % "_".join(myList)
    myNewId = "_".join(myList)
    self.product_id = myNewId

    #
    # Rename the thumb from the old name to the new name (if present):
    #
    if myPreviousId == None or myPreviousId == "":
      # This is a new record
      return
    if myPreviousId == myNewId:
      #it already has the correct name
      return

    # Make a copy of the thumb all filed away nicely by sensor / yy / mm / dd
    # the thumb was saved as: myJpegThumbnail = os.path.join(mInScenesPath, str( theFrame.id ) + "-rectified-clipped.jpg")
    myJpegThumbnail = os.path.join(CATALOGUE_SCENES_PATH, str( myPreviousId ) + ".jpg")
    myWorldFile = os.path.join(CATALOGUE_SCENES_PATH, str( myPreviousId ) + ".wld")
    #print "myJpegThumbnail %s" % myJpegThumbnail
    myOutputPath = os.path.join( CATALOGUE_SCENES_PATH, self.thumbnailPath() )
    if not os.path.isdir( myOutputPath ):
      #print "Creating dir: %s" % myOutputPath
      try:
        os.makedirs( myOutputPath )
      except OSError:
        logging.debug("Failed to make output directory (%s) ...quitting" % myOutputPath)
        return "False"
    else:
      #print "Exists: %s" % myOutputPath
      pass
    # now everything is ready do the actual renaming
    try:
      myNewJpgFile =  os.path.join( myOutputPath, myNewId+ ".jpg" )
      myNewWorldFile =  os.path.join( myOutputPath, myNewId + ".wld" )
      #print "New filename: %s" % myNewJpgFile
      shutil.move( myJpegThumbnail, myNewJpgFile )
      shutil.move( myWorldFile, myNewWorldFile )
    except:
      logging.debug("Failed to move the thumbnail" )
    return

  def productIdReverse(self, force=False):
    """
    Parse a product_id and populates instance fields

    If force is set, try to create missing pieces

     S5-_HRG_J--_CAM2_0172_+1_0388_00_110124_070818_L1A-_ORBIT--Vers.0.01
    #SAT_SEN_TYP__MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL_PROJTN

    Where:
    SAT    Satellite or mission          mandatory
    SEN    Sensor                        mandatory
    MOD    Acquisition mode              mandatory
    TYP    Type                          mandatory
    KKKK   Orbit path reference          optional?
    KS     Path shift                    optional?
    JJJJ   Orbit row reference           optional?
    JS     Row shift                     optional?
    YYMMDD Acquisition date              mandatory
    HHMMSS Scene centre acquisition time mandatory
    LEVL   Processing level              mandatory
    PROJTN Projection                    mandatory
    """
    parts = self.product_id.replace('-', '').split('_')
    # Searches for an existing acquisition_mode,
    # raise an error if do not match
    try:
      self.acquisition_mode = AcquisitionMode.objects.get(
          sensor_type__mission_sensor__mission__abbreviation=parts[0],
          sensor_type__mission_sensor__abbreviation=parts[1],
          abbreviation=parts[2],
          sensor_type__abbreviation=parts[3]
        )
    except ObjectDoesNotExist:
      if not force:
        raise
      # Create missing pieces of the chain
      mission = Mission.objects.get_or_create(abbreviation=parts[0], defaults={'mission_group':MissionGroup.objects.all()[0]})[0]
      mission_sensor = MissionSensor.objects.get_or_create(abbreviation=parts[1],mission=mission)[0]
      sensor_type = SensorType.objects.get_or_create(abbreviation=parts[3],mission_sensor=mission_sensor)[0]
      self.acquisition_mode = AcquisitionMode.objects.get_or_create(abbreviation=parts[2], sensor_type=sensor_type, defaults={'geometric_resolution':0, 'band_count':1})[0]

    try:
      self.projection = Projection.objects.get(name=parts[11][:6])
    except Projection.DoesNotExist:
      if not force:
        raise
      # Create Projection
      self.projection = Projection.objects.get_or_create(name=parts[11][:6], defaults={'epsg_code':0})


    # Skip L
    self.processing_level = ProcessingLevel.objects.get(abbreviation=re.sub(r'^L', '', parts[10]))
    self.path = int(parts[4]) #K Path Orbit
    self.path_offset = int(parts[5])
    self.row = int(parts[6]) #J Frame Row
    self.row_offset = int(parts[7])
    d = parts[8]
    t = parts[9]
    self.product_acquisition_start = datetime.datetime(int('20'+d[:2]), int(d[2:4]), int(d[-2:]), int(t[:2]), int(t[2:4]), int(t[-2:]))


###############################################################################

class OpticalProduct( GenericSensorProduct ):
  """We are using multitable inheritance so you can do this to get this
  class instance from an GenericProduct :
  myOpticalProduct = GenericProduct.objects.get(id=1).opticalproduct
  See http://docs.djangoproject.com/en/dev/topics/db/models/#id7 for more info."""
  ##Descriptors for optical products
  cloud_cover = models.IntegerField(null=True,blank=True)
  sensor_inclination_angle = models.FloatField(null=True,blank=True)
  sensor_viewing_angle = models.FloatField(null=True,blank=True)
  gain_name = models.CharField( max_length=200, null=True,blank=True)
  gain_value_per_channel = models.CharField( max_length=200, help_text="Comma separated list of gain values", null=True,blank=True )
  gain_change_per_channel = models.CharField( max_length=200, help_text="Comma separated list of gain change values", null=True,blank=True )
  bias_per_channel = models.CharField( max_length=200, help_text="Comma separated list of bias values", null=True,blank=True )
  solar_zenith_angle = models.FloatField(null=True,blank=True)
  solar_azimuth_angle = models.FloatField(null=True,blank=True)
  earth_sun_distance = models.FloatField(null=True,blank=True)
  objects = models.GeoManager()
  # We need a flag to tell if this Product class can have instances (if it is not abstract)
  concrete              = True
  class Meta:
    app_label= 'catalogue'


###############################################################################

#TODO use lookup tables rather?
LOOK_DIRECTION_CHOICES = ( ( 'L','Left' ), ( 'R', 'Right' ) )
RECEIVE_CONFIGURATION_CHOICES = ( ( 'V','Vertical' ), ( 'H','Horizontal' ) )
POLARISING_MODE_CHOICES = ( ('S','Single Pole' ), ( 'D','Dual Pole' ), ( 'Q', 'Quad Pole' ) )
ORBIT_DIRECTION_CHOICES = ( ('A', 'Ascending' ), ('D', 'Descending' ) )

class RadarProduct( GenericSensorProduct ):
  """We are using multitable inheritance so you can do this to get this
  class instance from an GenericProduct :
  myRadarProduct = GenericProduct.objects.get(id=1).radarproduct
  See http://docs.djangoproject.com/en/dev/topics/db/models/#id7 for more info."""
  # Note for radar products row and path will be computed as
  # the Degrees (2 digits) Minutes (2 Digits) and the offset will be used to store seconds (2 digits)
  imaging_mode = models.CharField( max_length=200,null=True,blank=True )
  look_direction = models.CharField( max_length=1, choices=LOOK_DIRECTION_CHOICES,null=True,blank=True )
  antenna_receive_configuration = models.CharField( max_length=1, choices=RECEIVE_CONFIGURATION_CHOICES,null=True,blank=True )
  polarising_mode = models.CharField( max_length=1, choices=POLARISING_MODE_CHOICES,null=True,blank=True )
  polarising_list = models.CharField( max_length=200, help_text="Comma separated list of V/H/VV/VH/HV/HH (vertical and horizontal polarisation.)",null=True,blank=True )
  slant_range_resolution = models.FloatField(null=True,blank=True)
  azimuth_range_resolution = models.FloatField(null=True,blank=True)
  orbit_direction = models.CharField( max_length=1, choices=ORBIT_DIRECTION_CHOICES,null=True,blank=True )
  calibration = models.CharField( max_length = 255,null=True,blank=True )
  incidence_angle = models.FloatField(null=True,blank=True)
  objects = models.GeoManager()
  # We need a flag to tell if this Product class can have instances (if it is not abstract)
  concrete              = True
  class Meta:
    app_label= 'catalogue'

###############################################################################

#ABP: this part will be completed with GeospatialProduct as an "abstract" class and Ordinal/Continuous
#TODO:


GEOSPATIAL_GEOMETRY_TYPE_CHOICES = ( ( 'R','Raster' ), ( 'VP', 'Vector - Points' ), ( 'VL', 'Vector - Lines' ) , ( 'VA', 'Vector - Areas / Polygons' ) )
class GeospatialProduct( GenericProduct ):
  """
  Geospatial product, does not have sensors information. Geospatial products may be rasters
  (that were derived from one or more satellite or other rasters) or vectors.
  """
  name = models.CharField(max_length = 255, null=False, blank=False, help_text="A descriptive name for this dataset");
  data_type = models.CharField( max_length=1, choices=GEOSPATIAL_GEOMETRY_TYPE_CHOICES,null=True,blank=True, help_text="Is this a vector or raster dataset?" )
  scale = models.IntegerField( help_text="The fractional part at the ideal maximum scale for this dataset. For example enter '50000' if it should not be used at scales larger that 1:50 000", null=True, blank=True, default=50000 )
  processing_notes = models.TextField( null=True, blank=True, help_text="Description of how the product was created." )
  # We need a flag to tell if this Product class can have instances (if it is not abstract)
  concrete              = True
  objects = models.GeoManager()
  class Meta:
    app_label= 'catalogue'

