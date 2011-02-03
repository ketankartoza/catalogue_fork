from django.db import models
from django.conf import settings
from django.contrib.gis.db import models
#for translation
from django.utils.translation import ugettext_lazy as _
#for user id foreign keys
from django.contrib.auth.models import User
import os

import logging
import datetime
# for generating globally unique id's - I think python 2.5 is required
import uuid

# for product_date soft trigger
import datetime

# Helper classes
from catalogue.geoiputils import *
from catalogue.nosubclassmanager import NoSubclassManager
from userprofile.models import BaseProfile

# for reflection
from django.contrib.contenttypes.models import ContentType

# PIL and os needed for making small thumbs
from PIL import Image, ImageFilter, ImageOps

###############################################################################
# Product related model ancilliary tables
###############################################################################

class Mission( models.Model ):
  """Satellite or Mission"""
  abbreviation = models.CharField( max_length="3", unique=True )
  name = models.CharField( max_length="255" )
  def __unicode__(self):
     return self.name

###############################################################################

class MissionSensor( models.Model ):
  """MissionSensor on the mission or satellite - e.g. HRV"""
  abbreviation = models.CharField( max_length="3", unique=True )
  name = models.CharField( max_length="255" )
  description = models.TextField()
  has_data = models.BooleanField(help_text='Mark false if there is no data for this sensor')
  def __unicode__(self):
     return self.name

###############################################################################

class AcquisitionMode( models.Model ):
  """Acquisition mode.
     @note: mode examples:
           J = Multispectral 10m
           P/M = Panchromatic 10m
           A/B = Panchromatic 5m
           T = Panchromatic 2.5m
           X = Multispectral 20m
           JT = Pansharpened 2.5m Multispectral"""
  abbreviation = models.CharField( max_length="4", unique=True )
  name = models.CharField( max_length="255" )
  geometric_resolution = models.IntegerField(help_text="Geometric resolution in mm")
  band_count = models.IntegerField()
  def __unicode__(self):
     return self.name

###############################################################################

class SensorType( models.Model ):
  """Sensor type / camera number e.g. CAM1"""
  abbreviation = models.CharField( max_length="4", unique=True )
  name = models.CharField( max_length="255" )
  def __unicode__(self):
     return self.name

###############################################################################

class ProcessingLevel( models.Model ):
  """Processing level e.g. L3Aa"""
  abbreviation = models.CharField( max_length="4", unique=True )
  name = models.CharField( max_length="255" )

  def __unicode__(self):
     return self.name

  class Meta:
    verbose_name = _('Processing Level')
    verbose_name_plural = _('Processing Levels')

  class Admin:
    pass


###############################################################################

class Projection( models.Model ):
  epsg_code = models.IntegerField()
  name = models.CharField('Name', max_length=128, db_index=True,unique=True)

  def __unicode__(self):
    return "EPSG:" + str( self.epsg_code ) + " " + self.name

  class Meta:
    verbose_name = _('Projection')
    verbose_name_plural = _('Projections')
    ordering = ('epsg_code', 'name')


  class Admin:
    pass

###############################################################################
# These models are not used in generating the sac id
###############################################################################

class Institution( models.Model ):
  name = models.CharField( max_length="255" )
  address1 = models.CharField( max_length="255" )
  address2 = models.CharField( max_length="255" )
  address3 = models.CharField( max_length="255" )
  post_code = models.CharField( max_length="255" )
  def __unicode__(self):
     return self.name


###############################################################################

class License( models.Model ):
  name = models.CharField( max_length="255" )
  details = models.TextField()
  def __unicode__(self):
     return self.name


###############################################################################

class Quality( models.Model ):
  name = models.CharField( max_length="255" )
  def __unicode__(self):
     return self.name
  class Meta:
    verbose_name = _('Quality')
    verbose_name_plural = _('Qualities')

###############################################################################

class CreatingSoftware( models.Model ):
  name = models.CharField( max_length="255" )
  version = models.CharField( max_length="100" )
  def __unicode__(self):
     return self.name

###############################################################################

class GenericProduct( models.Model ):
  """A generic model (following R-5.1-160 of DIMS system architecture document).
  @NOTE: this is not an abstract base class since we are using django multi-table
  inheritance. See http://docs.djangoproject.com/en/dev/topics/db/models/#id7"""
  product_date = models.DateTimeField(null=False,blank=False,db_index=True)
  processing_level = models.ForeignKey( ProcessingLevel )
  owner = models.ForeignKey( Institution )
  license = models.ForeignKey( License )
  spatial_coverage = models.PolygonField( srid=4326, help_text="Image footprint", null=False,blank=False )
  projection = models.ForeignKey( Projection )
  quality = models.ForeignKey( Quality )
  creating_software = models.ForeignKey( CreatingSoftware, null=False,blank=False )
  original_product_id = models.CharField( max_length="255", null=True,blank=True )
  product_id = models.CharField( help_text="SAC Formatted product ID", max_length="255", null=False,blank=True, db_index=True,unique=True )
  product_revision = models.CharField( max_length="255",null=True,blank=True )
  local_storage_path = models.CharField( max_length=255, help_text="Location on local storage if this product is offered for immediate download.", null=True,blank=True)
  metadata = models.TextField(help_text=_("An xml document describing all known metadata for this sensor."))
  remote_thumbnail_url =  models.TextField( max_length=255, help_text="Location on a remote server where this product's thumbnail resides. The value in this field will be nulled when a local copy is made of the thumbnail.")
  objects = models.GeoManager()

  def __unicode__( self ):
     return self.product_id

  class Meta:
    """This is not an abstract base class although you should avoid dealing directly with it
    see http://docs.djangoproject.com/en/dev/topics/db/models/#id7
    """
    abstract = False
    ordering = ('product_date',)


  def thumbnailPath( self ):
    """Returns the path (relative to whatever parent dir it is in) for the
      thumb for this file following the scheme <Sensor>/<YYYY>/<MM>/<DD>/
      The thumb itself will exist under this dir as <product_id>.jpg"""
    try:
        return self.getConcreteInstance().thumbnailPath()
    except:
        raise NotImplementedError()

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

  def imagePath( self ):
    """Returns the path (relative to whatever parent dir it is in) for the
      image itself following the scheme <Sensor>/<processinglevel>/<YYYY>/<MM>/<DD>/
      The image itself will exist under this dir as <product_id>.tif.bz2"""
    try:
        return self.getConcreteInstance().imagePath()
    except:
        raise NotImplementedError()

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
      if self.genericsensorproduct.opticalproduct:
        myObject = self.genericsensorproduct.opticalproduct
        return myObject, "Optical"
      elif self.genericsensorproduct.radarproduct:
        myObject = self.genericsensorproduct.radarproduct
        return myObject, "Radar"
      elif self.geospatialproduct:
        myObject = self.geospatialproduct
        return myObject, "Geospatial"
    except:
      return None, "Error - product not found"


  def getConcreteInstance( self ):
    """
    Returns the concrete product instance
    """
    return self.getConcreteProduct()[0]


  def setSacProductId( self ):
    """A sac product id adheres to the following format:

    SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL

    """
    try:
        return self.getConcreteInstance().setSacProductId()
    except:
        raise NotImplementedError()

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




###############################################################################

class GenericSensorProduct( GenericProduct ):
  """
  Multitable inheritance class to hold common fields for satellite imagery
  """
  mission = models.ForeignKey( 'catalogue.Mission' ) # e.g. S5
  mission_sensor = models.ForeignKey( MissionSensor ) # e.g. HRV
  sensor_type = models.ForeignKey( SensorType ) #e.g. CAM1
  acquisition_mode = models.ForeignKey( AcquisitionMode ) #e.g. M X T J etc
  product_acquisition_start = models.DateTimeField(null=False,blank=False,db_index=True)
  product_acquisition_end = models.DateTimeField(null=True,blank=True,db_index=True)
  geometric_accuracy_mean = models.FloatField ( null=True,blank=True )
  geometric_accuracy_1sigma = models.FloatField ( null=True,blank=True )
  geometric_accuracy_2sigma = models.FloatField ( null=True,blank=True )
  radiometric_signal_to_noise_ratio = models.FloatField( null=True,blank=True )
  radiometric_percentage_error = models.FloatField( null=True,blank=True )
  radiometric_resolution = models.IntegerField( help_text="Bit depth of image e.g. 16bit", null=False,blank=False  )
  geometric_resolution_x = models.FloatField( help_text="Geometric resolution in mm (x direction)", null=False,blank=False )
  geometric_resolution_y = models.FloatField( help_text="Geometric resolution in mm (y direction)", null=False,blank=False )
  spectral_resolution = models.IntegerField( help_text="Number of spectral bands in product" , null=False,blank=False)
  spectral_accuracy = models.FloatField( help_text="Wavelength Deviation",null=True,blank=True )
  orbit_number = models.IntegerField(null=True,blank=True)
  path = models.IntegerField(null=True,blank=True) #K Path Orbit
  path_offset = models.IntegerField(null=True,blank=True)
  row = models.IntegerField(null=True,blank=True) #J Frame Row
  row_offset = models.IntegerField(null=True,blank=True)
  offline_storage_medium_id = models.CharField( max_length=12, help_text="Identifier for the offline tape or other medium on which this scene is stored", null=True,blank=True )
  online_storage_medium_id = models.CharField( max_length=36, help_text="DIMS Product Id as defined by Werum e.g. S5_G2_J_MX_200902160841252_FG_001822",null=True,blank=True )

  class Meta:
    """This is not an abstract base class although you should avoid dealing directly with it
    see http://docs.djangoproject.com/en/dev/topics/db/models/#id7
    """
    abstract = False

  def imagePath( self ):
    """Returns the path (relative to whatever parent dir it is in) for the
      image itself following the scheme <Sensor>/<processinglevel>/<YYYY>/<MM>/<DD>/
      The image itself will exist under this dir as <product_id>.tif.bz2"""
    return os.path.join( self.mission.abbreviation,
                    str( self.processing_level.abbreviation),
                    str( self.product_acquisition_start.year ),
                    str( self.product_acquisition_start.month ),
                    str( self.product_acquisition_start.day ) )


  def thumbnailPath( self ):
    """Returns the path (relative to whatever parent dir it is in) for the
      thumb for this file following the scheme <Sensor>/<YYYY>/<MM>/<DD>/
      The thumb itself will exist under this dir as <product_id>.jpg"""
    return os.path.join( self.mission.abbreviation,
                    str( self.product_acquisition_start.year ),
                    str( self.product_acquisition_start.month ),
                    str( self.product_acquisition_start.day ) )

  def setSacProductId( self ):
    """A sac product id adheres to the following format:

      SAT_SEN_TYP_MOD_KKKK_KS_JJJJ_JS_YYMMDD_HHMMSS_LEVL

      Where:
      SAT    Satellite or mission          mandatory
      SEN    Sensor                        mandatory
      MOD    Acquisition mode              mandatory?
      TYP    Type                          mandatory?
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
    myList.append( self.pad( self.mission.abbreviation, 3 ) )
    myList.append( self.pad( self.mission_sensor.abbreviation, 3 ) )
    myList.append( self.pad( self.acquisition_mode.abbreviation, 3 ) )
    myList.append( self.pad( self.sensor_type.abbreviation, 3 ) )
    myList.append( self.zeroPad( str( self.path ),4 ) )
    myList.append( self.zeroPad( str( self.path_offset ),2 ) )
    myList.append(  self.zeroPad( str( self.row ),4 ) )
    myList.append(  self.zeroPad( str( self.row_offset ),2 ) )
    myDate = str( self.product_acquisition_start.year )[2:4]
    myDate += self.zeroPad( str( self.product_acquisition_start.month ),2 )
    myDate += self.zeroPad( str( self.product_acquisition_start.day ),2 )
    myList.append( myDate )
    myTime = self.zeroPad( str( self.product_acquisition_start.hour ),2)
    myTime += self.zeroPad( str( self.product_acquisition_start.minute ),2)
    myTime += self.zeroPad( str( self.product_acquisition_start.second ),2)
    myList.append( myTime )
    myList.append( "L" + self.pad( self.processing_level.abbreviation, 3 ) )
    myList.append( self.pad( self.projection.name,4 ) )
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

    # TODO: softcode this into settings
    mScenesPath = "/mnt/cataloguestorage/scenes_out_projected_sorted/"

    # Make a copy of the thumb all filed away nicely by sensor / yy / mm / dd
    # the thumb was saved as: myJpegThumbnail = os.path.join(mInScenesPath, str( theFrame.id ) + "-rectified-clipped.jpg")
    myJpegThumbnail = os.path.join(mScenesPath, str( myPreviousId ) + ".jpg")
    myWorldFile = os.path.join(mScenesPath, str( myPreviousId ) + ".wld")
    #print "myJpegThumbnail %s" % myJpegThumbnail
    myOutputPath = os.path.join( mScenesPath, self.thumbnailPath() )
    if not os.path.isdir( myOutputPath ):
      #print "Creating dir: %s" % myOutputPath
      try:
        os.makedirs( myOutputPath )
      except OSError:
        logging.debug("Failed to make output directory...quitting" )
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

  def __unicode__(self):
     return self.product_id

###############################################################################


###############################################################################

class GeospatialProduct( GenericProduct ):
    """
    Geospatial product, does not have sensors information
    """
    name = models.CharField(max_length = 255);





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


###############################################################################
#
# Next bunch of models all relate to order management
#
###############################################################################

class Datum(models.Model):

  name = models.CharField('Name', max_length=128, db_index=True,unique=True)

  class Meta:
    verbose_name = _('Datums')
    verbose_name_plural = _('Datums')

  def __unicode__(self):
    return self.name

  class Admin:
    pass

###############################################################################


class ResamplingMethod(models.Model):

  name = models.CharField('Name', max_length=128, db_index=True,unique=True)


  class Meta:
    verbose_name = _('Resampling Method')
    verbose_name_plural = _('Resampling Methods')

  def __unicode__(self):
    return self.name

  class Admin:
    pass

###############################################################################


class FileFormat(models.Model):

  name = models.CharField('Name', max_length=128, db_index=True,unique=True)


  class Meta:
    verbose_name = _('File Format')
    verbose_name_plural = _('File Formats')

  def __unicode__(self):
    return self.name

  class Admin:
    pass

###############################################################################


class OrderStatus(models.Model):

  name = models.CharField('Name', max_length=128, db_index=True,unique=True)


  class Meta:
    verbose_name = _('Order Status')
    verbose_name_plural = _('Order Status List')

  def __unicode__(self):
    return self.name

  class Admin:
    pass

###############################################################################

class DeliveryMethod(models.Model):

  name = models.CharField('Name', max_length=128, db_index=True,unique=True)


  class Meta:
    verbose_name = _('Delivery Method')
    verbose_name_plural = _('Delivery Methods')

  def __unicode__(self):
    return self.name

  class Admin:
    pass


###############################################################################

class Order(models.Model):
  user = models.ForeignKey(User)
  notes = models.TextField(help_text=_("Make a note of any special requirements or processing instructions you may need. Please note that in the case of free products and priority products, they will only be supplied with default options."),null=True,blank=True)
  processing_level = models.ForeignKey(ProcessingLevel,verbose_name="Processing Level",default=3)
  projection = models.ForeignKey(Projection,verbose_name="Projection",default=3)
  datum = models.ForeignKey(Datum, verbose_name="Datum",default=1)
  resampling_method = models.ForeignKey(ResamplingMethod, verbose_name="Resampling Method",default=2) #cubic conv#cubic conv
  file_format = models.ForeignKey(FileFormat, verbose_name="File Format",default=1)
  order_status = models.ForeignKey(OrderStatus,verbose_name="Order Status",default=1)
  delivery_method = models.ForeignKey(DeliveryMethod, verbose_name="Delivery Method", default=1)
  order_date = models.DateTimeField(verbose_name="Order Date", auto_now=True, auto_now_add=True,
      help_text = "When the order was placed - not shown to users")
  #default manager
  objects = models.Manager()
  # A model can have more than one manager. Above will be used as default
  # see: http://docs.djangoproject.com/en/dev/topics/db/managers/
  # Also use a custom manager so that we can get
  # orders that have no subclass instances (since
  # we want to be able to list product orders while excluding
  # their TaskingRequest subclasses
  base_objects = NoSubclassManager() #see catalogue/nosubclassmanager.py

  class Meta:
    verbose_name = _('Order')
    verbose_name_plural = _('Orders')

  def __unicode__(self):
    return str(self.id)

  class Admin:
    pass

###############################################################################

class TaskingRequest( Order ):
  """A tasking request inherits from the order model and adds
  three fields: geometry, target date  and sensor. The tasking
  request is used by end users to queue up acquisition requests
  for a given sensor."""
  geometry = models.PolygonField( srid=4326, help_text="Requested coverage area", null=False,blank=False )
  target_date = models.DateTimeField(verbose_name="Target Date", auto_now=True, auto_now_add=True,
      help_text = "When the image should be acquired (as close as possible to this date).")
  mission_sensor = models.ForeignKey( MissionSensor ) # e.g. Spot5
  objects = models.GeoManager()


  class Meta:
    verbose_name = _('Tasking Request')
    verbose_name_plural = _('Tasking Requests')

  def __unicode__(self):
    return str(self.id)

  class Admin:
    pass


###############################################################################

class SearchRecord(models.Model):
  """ A class used for returning search results to a web page in a normalised
  way, regardless of which sensor was used etc.

  Normally the SearchRecord.save() method will only be called if you want to add
  an item to and order to the cart.

  By definition, cart items have no order ID, but do have a user id.

  Order items on the other hand will have both a user id and a order id.

  When the user creates a new order, all current search records that do not have
  an order id should be added to it.

  """
  user = models.ForeignKey(User)
  order = models.ForeignKey( Order, null=True, blank=True )
  product = models.ForeignKey( GenericProduct, null=False, blank=False )
  # Required because genericproduct fkey references a table with geometry
  objects = models.GeoManager()

  class Meta:
    verbose_name = _('Record')
    verbose_name_plural = _('Records')

  def __unicode__(self):
      return self.product.product_id

  def create( self, theUser, theProduct ):
    """Python has no support for overloading ctors"""
    myRecord = None
    # in future this could be other product types e.g. atmospheric or radar
    # which is wy search record is not modelled with a fkey ref to optical product
    myRecord = SearchRecord()
    myRecord.user = theUser
    myRecord.product = theProduct

    return myRecord

  class Admin:
    pass

class OrderStatusHistory(models.Model):
  '''Used to maintain provenance of all status changes that happen to an order'''
  user = models.ForeignKey(User)
  order = models.ForeignKey(Order)
  order_change_date = models.DateTimeField(verbose_name="Date", auto_now=True, auto_now_add=True,
      help_text = "When the order status was changed")
  notes = models.TextField()
  old_order_status = models.ForeignKey(OrderStatus,verbose_name="Old Order Status",related_name="old_order_status")
  new_order_status = models.ForeignKey(OrderStatus,verbose_name="New Order Status",related_name="new_order_status")

  def __unicode__(self):
     return self.notes[:25]

  class Meta:
    verbose_name = _('Order Status History')
    verbose_name_plural = _('Order Status History')
    ordering = ('-order_change_date',)

  class Admin:
    pass

###############################################################################
#
# Every search a user does we will keep a record of
#
###############################################################################

class Search(models.Model):
  """
  Stores search results
  """

  #ABP: added to store which product to search
  # Values for the search_type parameter
  PRODUCT_SEARCH_GENERIC       = 0  # default in case of blank/null/0
  PRODUCT_SEARCH_OPTICAL       = 1
  PRODUCT_SEARCH_RADAR         = 2
  PRODUCT_SEARCH_GEOSPATIAL    = 3

  PRODUCT_SEARCH_TYPES = (
    (PRODUCT_SEARCH_GENERIC,    'Generic product search'),
    (PRODUCT_SEARCH_OPTICAL,    'Optical product search'),
    (PRODUCT_SEARCH_RADAR,      'Radar product search'),
    (PRODUCT_SEARCH_GEOSPATIAL, 'Geospatial product search'),
  )

  search_type = models.IntegerField('Search type', default = 0, choices = PRODUCT_SEARCH_TYPES, db_index = True)
  user = models.ForeignKey(User)
  keywords = models.CharField('Keywords', max_length=255,blank=True)
  # foreign keys require the first arg to the be the relation name
  # so we explicitly have to use verbose_name for the user friendly name
  sensors = models.ManyToManyField(MissionSensor, verbose_name='Sensors', null=True,blank=True,
      help_text='Choosing one or more sensor is required. Use ctrl-click to select more than one.')
  geometry = models.PolygonField(srid=4326, null=True, blank=True,
      help_text='Digitising an area of interest is not required but is recommended.')
  k_orbit_path_min = models.IntegerField('Path(K) min',
      blank=True,
      null=True,
      help_text='Path (K) value. If specified here, geometry will be ignored. Must be a value between 1 and 233. Will be ignored if sensor type does not include J/K metadata.')
  j_frame_row_min = models.IntegerField('Row (J) min',
      blank=True,
      null=True,
      help_text='Row (J) value. If specified here, geometry will be ignored. Must be a value between 1 and 248. Will be ignored if sensor type does not include J/K metadata.')

  k_orbit_path_max = models.IntegerField('Path (K) max',
      blank=True,
      null=True,
      help_text='Path (K) value. If specified here, geometry will be ignored. Must be a value between 1 and 233. Will be ignored if sensor type does not include J/K metadata.')

  j_frame_row_max = models.IntegerField('Row (J) max',
      blank=True,
      null=True,
      help_text='Row (K) value. If specified here, geometry will be ignored. Must be a value between 1 and 248. Will be ignored if sensor type does not include J/K metadata.')

  # let the user upload shp to define their search box
  # uploaded files will end up in media/uploads/2008/10/12 for example
  #geometry_file = models.FileField(null=True,blank=True,upload_to="uploads/%Y/%m/%d")
  ip_position = models.PointField(srid=4326,null=True, blank=True)
  search_date = models.DateTimeField('Search Date', auto_now=True, auto_now_add=True,
      help_text = "When the search was made - not shown to users")
  start_date = models.DateField('Start Date', auto_now=False, auto_now_add=False, null=False, blank=False,
      default = datetime.datetime.now(),
      help_text='Start date is required. YYYY-MM-DD.')
  end_date = models.DateField('End Date', auto_now=False, auto_now_add=False, null=False, blank=True,
      default = datetime.datetime.now(),
      help_text='End date is required. YYYY-MM-DD.')
  # e.g. 16fd2706-8baf-433b-82eb-8c7fada847da
  guid = models.CharField(max_length=40)
  deleted = models.NullBooleanField('Deleted?',
      blank=True,
      null=True,
      default = True,
      help_text='Mark this search as deleted so the user doesn not see it')
  use_cloud_cover = models.BooleanField('Use cloud cover?',
      blank=False,
      null=False,
      default = False,
      help_text='If you want to limit searches to optical products with a certain cloud cover, enable this.')
  cloud_mean = models.IntegerField(null=True, blank=True, default=5, verbose_name="Max Clouds", help_text="Select the maximum permissible cloud cover.", max_length=1)

  # Use the geo manager to handle geometry
  objects = models.GeoManager()

  def save(self):
    #makes a random globally unique id
    if not self.guid or self.guid=='null':
      self.guid = str(uuid.uuid4())
    super(Search, self).save()

  def __unicode__(self):
    return "Start Date: " + str(self.start_date) + " End Date: "  \
           + str(self.end_date) + " Guid: " + self.guid + " User: " + str(self.user)

  def sensorsAsString( self ):
    myList = self.sensors.values_list( 'name',flat=True )
    myString = ", ".join(myList)
    return myString

  class Meta:
    verbose_name = _('Search')
    verbose_name_plural = _('Searches')
    ordering = ('search_date',)

###############################################################################

class Clip( models.Model ):
  """ Stores the information about clip performed by the user. The clip is actually
  done by Lion via urllib, then results saved in /clips/guid and Clip model is
  updated with url and is_completed flag is set to True. User will be notified
  by email and/or via a view that shows all clips and their status."""
  guid = models.CharField(max_length=40)
  owner = models.ForeignKey( User )
  date = models.DateTimeField(verbose_name="Date", auto_now=True, auto_now_add=True, help_text = "Not shown to users")
  ## provisory hardcoded choices for clipped image source.
  image = models.CharField( max_length=20,
                            choices = [(0,"zaSpot2mMosaic2009"),
                                       (1,"zaSpot2mMosaic2008"),
                                       (2,"zaSpot2mMosaic2007")])
  # polygon is the one from the shapefile
  geometry = models.PolygonField( srid = 4326 )
  objects = models.GeoManager()
  status = models.CharField( max_length=20,
                            choices = [(0, "submitted"),
                                       (1, "in process"),
                                       (2, "completed")])
  # the result of the clipping operation is available via a URL that is sent to the user
  result_url =  models.URLField( max_length=1024, verify_exists=True )

  def save(self):
    #makes a random globally unique id
    if not self.guid or self.guid=='null':
      self.guid = str(uuid.uuid4())
    super(Clip, self).save()

  class Meta:
    verbose_name=_("Clip")
    verbose_name_plural=_("Clips")


###############################################################################

class Visit(models.Model):
  """Each time a visitor to the site arrives to the front page we will log their IP address and Lat/Long"""

  city = models.CharField('City', max_length=255)
  country = models.CharField('Country', max_length=255)
  ip_address = models.IPAddressField('IP Address')
  ip_position = models.PointField('IP Lat/Long', srid=4326)
  visit_date = models.DateTimeField('DateAdded', auto_now=True, auto_now_add=False)
  user = models.ForeignKey(User,null=True, blank=True)
  objects = models.GeoManager()

  def customSQL( self, sql_string, qkeys ):
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql_string)
    rows = cursor.fetchall()
    fdicts = []
    for row in rows:
      i = 0
      cur_row = {}
      for key in qkeys:
          cur_row[ key ] = row[ i ]
          i = i+1
      fdicts.append( cur_row )
    return fdicts

  class Meta:
    verbose_name = _('Visit')
    verbose_name_plural = _('Visits')
    ordering = ('visit_date',)


class VisitorReport(models.Model):
  """This is a *special*, *read-only* model intended to
      be used for generating the visitors summary report as kml"""
  visit_count = models.IntegerField()
  geometry = models.PointField(srid=4326,null=True, blank=True)
  country = models.CharField(max_length=64)
  city = models.CharField(max_length=64)
  objects = models.GeoManager()

  def __unicode(self):
    return str(self.city)

  class Meta:
    db_table = u'vw_visitor_report'
    #requires django 1.1
    managed = False

###############################################################################

class SacUserProfile(BaseProfile):
  # See:
  # http://www.djangobook.com/en/1.0/chapter12/#cn222
  # We define extra properties we want to store about users
  # here - in particular if they belong to institutions
  # that have strategic partnerships with SAC so that they may
  # view hires spot data etc.
  #
  # update : 25 May 2010 - add django-profile app for more flexible
  # profile management. See http://code.google.com/p/django-profile/

  # This first field won't be made available to users in their
  # profile forms since admins must set it only if the user is a
  # employee of a sac strategic partner
  strategic_partner = models.BooleanField("Strategic Partner?",help_text="Mark this as true if the person belongs to an institution that is a CSIR/SAC strategic partner")
  firstname = models.CharField("First Name (required)", max_length=255, null=False, blank=False )
  surname = models.CharField("Surname (required)", max_length=255, null=False, blank=False )
  url = models.URLField(blank=True)
  about = models.TextField(blank=True)
  address1 = models.CharField("Address 1 (required)", max_length=255, null=False, blank=False )
  address2 = models.CharField("Address 2 (required)", max_length=255, null=False, blank=False )
  address3 = models.CharField(max_length=255, blank=True )
  address4 = models.CharField(max_length=255, blank=True )
  post_code = models.CharField("Post Code (required)", max_length=25, null=False, blank=False )
  organisation = models.CharField("Organisation (required)", max_length=255, null=False, blank=False)
  contact_no = models.CharField("Contact No (required)",max_length=16, null=False, blank=False)

  def __unicode(self):
    return str(self.user.name)


  class Meta:
    verbose_name = _('User Profile')
    verbose_name_plural = _('User Profiles')

class OrderNotificationRecipients(models.Model):
  """This class is used to map which staff members receive
    notifications for which sensors so that the notices when
    orders are placed/updated etc are targeted to the correct
    individuals"""
  user = models.ForeignKey(User)
  sensors = models.ManyToManyField(MissionSensor, verbose_name='Sensors', null=True,blank=True,
      help_text='Choosing one or more sensor is required. Use ctrl-click to select more than one.')

  def __unicode(self):
    return str(self.user.name)

  class Meta:
    verbose_name = _('Order Notification Recipient')
    verbose_name_plural = _('Order Notification Recipients')

###############################################
# Temporary tables for data import only
###############################################

#
# Note all these models are / should be defined in the import schema in the pg
# backend
#
class Spot5(models.Model):
    gid = models.IntegerField(primary_key=True)
    a21 = models.CharField(max_length=25)
    sc_num = models.DecimalField(max_digits=19, decimal_places=0)
    seg_num = models.DecimalField(max_digits=19, decimal_places=0)
    satel = models.SmallIntegerField()
    ang_inc = models.FloatField()
    ang_acq = models.FloatField()
    date_acq = models.CharField(max_length=10)
    month_acq = models.CharField(max_length=2)
    time_acq = models.CharField(max_length=8)
    cloud_quot = models.CharField(max_length=16)
    cloud_per = models.DecimalField(max_digits=2, decimal_places=2)
    snow_quot = models.CharField(max_length=16)
    lat_cen = models.FloatField()
    lon_cen = models.FloatField()
    lat_up_l = models.FloatField()
    lon_up_l = models.FloatField()
    lat_up_r = models.FloatField()
    lon_up_r = models.FloatField()
    lat_lo_l = models.FloatField()
    lon_lo_l = models.FloatField()
    lat_lo_r = models.FloatField()
    lon_lo_r = models.FloatField()
    resol = models.DecimalField(max_digits=8, decimal_places=2)
    mode = models.CharField(max_length=5)
    type = models.CharField(max_length=1)
    url_ql = models.CharField(max_length=169)
    the_geom = models.PolygonField()
    objects = models.GeoManager()
    class Meta:
      db_table = '"import"."spot5"'
      #requires django 1.1
      managed = False

class Sumb(models.Model):
    gid = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    source = models.CharField(max_length=78)
    sceneid = models.CharField(max_length=58)
    k = models.CharField(max_length=4)
    j = models.CharField(max_length=4)
    adate = models.CharField(max_length=6)
    utmzo = models.CharField(max_length=2)
    utmalt = models.CharField(max_length=2)
    the_geom = models.PolygonField()
    objects = models.GeoManager()
    class Meta:
      db_table = '"import"."sumb"'
      #requires django 1.1
      managed = False

class Sacc(models.Model):
    gid = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    source = models.CharField(max_length=78)
    sceneid = models.CharField(max_length=58)
    wrsp = models.CharField(max_length=4)
    wrsr = models.CharField(max_length=4)
    adate = models.CharField(max_length=6)
    utmzo = models.CharField(max_length=2)
    utmalt = models.CharField(max_length=2)
    the_geom = models.PolygonField()
    objects = models.GeoManager()
    class Meta:
      db_table = '"import"."sacc"'
      #requires django 1.1
      managed = False

class Cbers(models.Model):
    gid = models.IntegerField(primary_key=True)
    id = models.IntegerField()
    source = models.CharField(max_length=78)
    sceneid = models.CharField(max_length=58)
    k = models.CharField(max_length=4)
    j = models.CharField(max_length=4)
    adate = models.CharField(max_length=2)
    ayear = models.CharField(max_length=2)
    amonth = models.CharField(max_length=2)
    aday = models.CharField(max_length=2)
    ahour = models.CharField(max_length=2)
    amin = models.CharField(max_length=2)
    asec = models.CharField(max_length=2)
    utmzo = models.CharField(max_length=2)
    utmalt = models.CharField(max_length=2)
    sazia = models.FloatField(max_length=6)
    seleva = models.FloatField(max_length=6)
    the_geom = models.PolygonField()
    objects = models.GeoManager()
    class Meta:
      db_table = '"import"."cbers"'
      #requires django 1.1
      managed = False


def set_generic_product_date(sender, instance, **kw):
  """
  Sets the product_date based on acquisition date
  """
  if instance.product_acquisition_end:
    instance.product_date = datetime.fromordinal(instance.product_acquisition_start.toordinal() \
        + (instance.product_acquisition_end - instance.product_acquisition_end).days)
  else:
    instance.product_date = instance.product_acquisition_start


models.signals.pre_save.connect(set_generic_product_date, sender = GenericSensorProduct)