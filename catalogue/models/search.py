from django.contrib.gis.db import models
# for generating globally unique id's - I think python 2.5 is required
import uuid
import datetime
#for user id foreign keys
from django.contrib.auth.models import User
from orders import Order
from products import GenericProduct
from dictionaries import MissionSensor, AcquisitionMode, License, SensorType, Mission
#for translation

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
    verbose_name = 'Record'
    verbose_name_plural = 'Records'
    app_label= 'catalogue'

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


###############################################################################
#
# Every search a user does we will keep a record of
#
###############################################################################

class Search(models.Model):
  """
  Stores search results
  """

  # ABP: added to store which product to search
  # Values for the search_type parameter
  PRODUCT_SEARCH_GENERIC       = 0  # default in case of blank/null/0 = simple search
  PRODUCT_SEARCH_OPTICAL       = 1
  PRODUCT_SEARCH_RADAR         = 2
  PRODUCT_SEARCH_GEOSPATIAL    = 3
  PRODUCT_SEARCH_IMAGERY       = 4

  PRODUCT_SEARCH_TYPES = (
    (PRODUCT_SEARCH_GENERIC,    'Generic product search'),
    (PRODUCT_SEARCH_OPTICAL,    'Optical product search'),
    (PRODUCT_SEARCH_RADAR,      'Radar product search'),
    (PRODUCT_SEARCH_GEOSPATIAL, 'Geospatial product search'),
    # ABP: has no idea if this make s sense
    #(PRODUCT_SEARCH_IMAGERY,    'Generic imagery product search'),
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
      help_text='Product date is required. YYYY-MM-DD.')
  end_date = models.DateField('End Date', auto_now=False, auto_now_add=False, null=False, blank=False,
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
  cloud_mean = models.IntegerField(null=True, blank=True, default=5, verbose_name="Max Clouds", help_text = "Select the maximum permissible cloud cover.", max_length=1)

  # ABP: new additions
  acquisition_mode                  = models.ForeignKey(AcquisitionMode, blank=True, null=True, help_text = 'Choose the acquisition mode.') #e.g. M X T J etc
  license                           = models.ManyToManyField(License, blank=True, null=True, help_text = 'Choose one or more licenses.')

  # ABP: added to store geometric_accuracy_mean ranges
  # Values for geometric_accuracy_mean
  ACCURACY_MEAN_0               = 0
  ACCURACY_MEAN_1               = 1
  ACCURACY_MEAN_2               = 2
  ACCURACY_MEAN_3               = 3
  ACCURACY_MEAN_4               = 4
  ACCURACY_MEAN_5               = 5

  ACCURACY_MEAN_OPTIONS = (
    (ACCURACY_MEAN_0,   '<= 1m'),
    (ACCURACY_MEAN_1,   '1m - 2m'),
    (ACCURACY_MEAN_2,   '2m - 6m'),
    (ACCURACY_MEAN_3,   '6m - 20m'),
    (ACCURACY_MEAN_4,   '20m - 35m'),
    (ACCURACY_MEAN_5,   '35m - 60m'),
  )

  ACCURACY_MEAN_RANGE = {
    ACCURACY_MEAN_0:   (0.0, 1.0),
    ACCURACY_MEAN_1:   (1.0, 2.0),
    ACCURACY_MEAN_2:   (2.0, 6.0),
    ACCURACY_MEAN_3:   (6.0, 20.0),
    ACCURACY_MEAN_4:   (20.0, 35.0),
    ACCURACY_MEAN_5:   (35.0, 60.0),
  }

  geometric_accuracy_mean           = models.IntegerField(null=True, blank=True, choices = ACCURACY_MEAN_OPTIONS, help_text = 'Select mean resolution class.')
  spectral_resolution               = models.IntegerField(help_text="Number of spectral bands in product", null=True, blank =True)
  # sensor_inclination_angle: range
  sensor_inclination_angle_start    = models.FloatField(null=True, blank=True, help_text = 'Select sensor inclination angle start.')
  sensor_inclination_angle_end      = models.FloatField(null=True, blank=True, help_text = 'Select sensor inclination angle end.')
  # ABP: 2 new FKs
  mission                           = models.ForeignKey( Mission, null=True, blank=True, help_text = 'Select satellite mission.') # e.g. S5
  sensor_type                       = models.ForeignKey( SensorType, null=True, blank=True, related_name = 'search_sensor_type') #e.g. CAM1

  # Use the geo manager to handle geometry
  objects = models.GeoManager()

  def save(self):
    #makes a random globally unique id
    if not self.guid or self.guid=='null':
      self.guid = str(uuid.uuid4())
    super(Search, self).save()

  def __unicode__(self):
    return "Start Date: " + str(self.start_date) + "End Date: " + str(self.end_date) + " Guid: " + self.guid + " User: " + str(self.user)

  @staticmethod
  def getDictionaryMap(parm):
    """
    Returns the right join chain from a Product model to dictionary
    parameter

    for example:
    getSensorDictionaryMap('mission')
    will return
    'acquisition_mode__sensor_type__mission_sensor__mission'
    """
    if parm == 'sensor_type':
      return 'acquisition_mode__sensor_type'
    if parm == 'mission_sensor':
      return 'acquisition_mode__sensor_type__mission_sensor'
    if parm == 'mission':
      return 'acquisition_mode__sensor_type__mission_sensor__mission'
    return parm


  @property
  def isAdvanced(self):
    """
    Checks wether the Search is an advanced Search.
    Condition for being an advanced search is that at least one of the
    advanced parameter is set
    """
    return  self.search_type \
            or self.license.count() \
            or self.sensors.count() \
            or self.keywords \
            or self.k_orbit_path_min \
            or self.j_frame_row_min \
            or self.k_orbit_path_max \
            or self.j_frame_row_max \
            or self.use_cloud_cover \
            or self.acquisition_mode \
            or self.geometric_accuracy_mean \
            or self.spectral_resolution \
            or self.sensor_inclination_angle_start \
            or self.sensor_inclination_angle_end \
            or self.mission \
            or self.sensor_type

  def sensorsAsString( self ):
    myList = self.sensors.values_list( 'name',flat=True )
    myString = ", ".join(myList)
    return myString

  def productIdAsHash(self):
    """
    Returns field values suitable for initial ProductIdSearchForm population
    """
    return {
        'mission':            self.mission_id,
        'sensors':            [m.pk for m in self.sensors.all()],
        'acquisition_mode':   self.acquisition_mode_id,
        'sensor_type':        self.sensor_type_id,
        'start_year':         self.start_date.year,
        'start_month':        self.start_date.month,
        'start_day':          self.start_date.day,
        'end_year':           self.end_date.year,
        'end_month':          self.end_date.month,
        'end_day':            self.end_date.day,
      }

  class Meta:
    app_label= 'catalogue'
    verbose_name = 'Search'
    verbose_name_plural = 'Searches'
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
    app_label= 'catalogue'
    verbose_name="Clip"
    verbose_name_plural="Clips"
