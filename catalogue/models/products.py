from django.contrib.gis.db import models
from dictionaries import *
import logging
import os
import urllib2
from django.conf import settings
#for translation
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
# PIL and os needed for making small thumbs
from PIL import Image, ImageFilter, ImageOps

from django_dag.models import node_factory, edge_factory



class GenericProduct( node_factory('catalogue.ProductLink', base_model = models.Model ) ):
  """A generic model (following R-5.1-160 of DIMS system architecture document).
  @NOTE: this is not an abstract base class since we are using django multi-table
  inheritance. See http://docs.djangoproject.com/en/dev/topics/db/models/#id7"""
  product_date = models.DateTimeField(db_index=True)
  processing_level = models.ForeignKey( ProcessingLevel )
  owner = models.ForeignKey( Institution )
  license = models.ForeignKey( License )
  spatial_coverage = models.PolygonField( srid=4326, help_text="Image footprint")
  projection = models.ForeignKey( Projection )
  quality = models.ForeignKey( Quality )
  creating_software = models.ForeignKey( CreatingSoftware, null=False,blank=False )
  original_product_id = models.CharField( max_length="255", null=True,blank=True )
  product_id = models.CharField( help_text="SAC Formatted product ID", max_length="255", db_index=True,unique=True )
  product_revision = models.CharField( max_length="255",null=True,blank=True )
  local_storage_path = models.CharField( max_length=255, help_text="Location on local storage if this product is offered for immediate download.", null=True,blank=True)
  metadata = models.TextField(help_text=_("An xml document describing all known metadata for this sensor."))
  remote_thumbnail_url =  models.TextField( max_length=255, help_text="Location on a remote server where this product's thumbnail resides. The value in this field will be nulled when a local copy is made of the thumbnail.")
  objects = models.GeoManager()

  def __unicode__( self ):
     if self.product_id:
        return self.product_id
     return "Internal ID: %d" % self.pk

  def __str__( self ):
     return self.__unicode__()

  class Meta:
    """This is not an abstract base class although you should avoid dealing directly with it
    see http://docs.djangoproject.com/en/dev/topics/db/models/#id7
    """
    app_label= 'catalogue'
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
      return self.genericsensorproduct.opticalproduct, "Optical"
    except:
      pass
    try:
      return self.genericsensorproduct.radarproduct, "Radar"
    except:
      pass
    try:
      return self.geospatialproduct, "Geospatial"
    except:
      pass

    # ABP: raise exception instead of returning None, "Error - product not found"
    raise ObjectDoesNotExist()


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


class ProductLink (edge_factory(GenericProduct, concrete = False, base_model = models.Model)):
  """
  Links between products
  """
  class Meta:
    """This is not an abstract base class although you should avoid dealing directly with it
    see http://docs.djangoproject.com/en/dev/topics/db/models/#id7
    """
    app_label= 'catalogue'


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
    app_label= 'catalogue'
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
    """
      A sac product id adheres to the following format:

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

  objects = models.GeoManager()
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
  class Meta:
    app_label= 'catalogue'
