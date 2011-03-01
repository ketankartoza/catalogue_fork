from packagekit.enums import LICENSE_TPL
from django.contrib.gis.db import models

###############################################################################
# Product related model ancilliary tables
###############################################################################

class MissionGroup( models.Model ):
  """Mission Group"""
  name = models.CharField( max_length="255" )
  class Meta:
    app_label= 'catalogue'
  def __unicode__(self):
     return self.name


###############################################################################

class Mission( models.Model ):
  """Satellite or Mission"""
  abbreviation = models.CharField( max_length="3", unique=True )
  name = models.CharField( max_length="255" )
  mission_group = models.ForeignKey(MissionGroup) # e.g. S5
  class Meta:
    app_label= 'catalogue'
  def __unicode__(self):
     return self.name


###############################################################################

class MissionSensor( models.Model ):
  """
  MissionSensor on the mission or satellite - e.g. HRV
  ABP: TODO: get rid of has_data (or auto-update with soft trigger ?)
  """
  abbreviation = models.CharField( max_length="3")
  name = models.CharField( max_length="255" )
  description = models.TextField()
  has_data = models.BooleanField(help_text='Mark false if there is no data for this sensor')
  mission = models.ForeignKey(Mission) # e.g. S5
  class Meta:
    app_label= 'catalogue'
    unique_together = ('mission', 'abbreviation')
  def __unicode__(self):
     return "%s:%s" % (self.abbreviation, self.mission)

###############################################################################

class SensorType( models.Model ):
  """Sensor type / camera number e.g. CAM1"""
  abbreviation = models.CharField( max_length="4")
  name = models.CharField( max_length="255" )
  mission_sensor = models.ForeignKey(MissionSensor ) # e.g. HRV
  is_taskable = models.BooleanField(default=True)
  class Meta:
    app_label= 'catalogue'
    unique_together = ('mission_sensor', 'abbreviation')
  def __unicode__(self):
    return "%s:%s" % (self.abbreviation, self.mission_sensor)

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
  sensor_type = models.ForeignKey(SensorType ) #e.g. CAM1
  abbreviation = models.CharField( max_length="4")
  name = models.CharField( max_length="255" )
  geometric_resolution = models.IntegerField(help_text="Geometric resolution in mm")
  band_count = models.IntegerField()
  is_grayscale = models.BooleanField(default=False)
  class Meta:
    app_label= 'catalogue'
    unique_together = ('sensor_type', 'abbreviation')
  def __unicode__(self):
    return "%s:%s" % (self.abbreviation, self.sensor_type)


###############################################################################

class ProcessingLevel( models.Model ):
  """Processing level e.g. L3Aa"""
  abbreviation = models.CharField( max_length="4", unique=True )
  name = models.CharField( max_length="255" )

  def __unicode__(self):
     return self.name

  class Meta:
    app_label= 'catalogue'
    verbose_name = 'Processing Level'
    verbose_name_plural = 'Processing Levels'

  class Admin:
    pass


###############################################################################

class Projection( models.Model ):
  epsg_code = models.IntegerField()
  name = models.CharField('Name', max_length=128, db_index=True,unique=True)

  def __unicode__(self):
    return "EPSG:" + str( self.epsg_code ) + " " + self.name

  class Meta:
    app_label= 'catalogue'
    verbose_name = 'Projection'
    verbose_name_plural = 'Projections'
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
  class Meta:
    app_label= 'catalogue'
  def __unicode__(self):
     return self.name


###############################################################################

class License( models.Model ):
  """
  Licenses for Products
  """
  LICENSE_TYPE_FREE       = 1
  LICENSE_TYPE_GOVERNMENT = 2
  LICENSE_TYPE_COMMERCIAL = 3
  LICENSE_TYPE_ANY        = 4

  LICENSE_TYPE_CHOICES = (
      (LICENSE_TYPE_FREE,       'Free'),
      (LICENSE_TYPE_GOVERNMENT, 'Government'),
      (LICENSE_TYPE_COMMERCIAL, 'Commercial'),
      (LICENSE_TYPE_ANY,        'Any'),
    )
  name = models.CharField( max_length="255" )
  details = models.TextField()
  type = models.IntegerField(choices=LICENSE_TYPE_CHOICES)

  class Meta:
    app_label= 'catalogue'
  def __unicode__(self):
     return self.name


###############################################################################

class Quality( models.Model ):
  name = models.CharField( max_length="255" )
  def __unicode__(self):
     return self.name
  class Meta:
    app_label= 'catalogue'
    verbose_name = 'Quality'
    verbose_name_plural = 'Qualities'

###############################################################################

class CreatingSoftware( models.Model ):
  name = models.CharField( max_length="255" )
  version = models.CharField( max_length="100" )
  class Meta:
    app_label= 'catalogue'
  def __unicode__(self):
     return self.name

###############################################################################

