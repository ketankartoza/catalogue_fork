from django.contrib.gis.db import models

###############################################################################
# Product related model ancilliary tables
###############################################################################

class Mission( models.Model ):
  """Satellite or Mission"""
  abbreviation = models.CharField( max_length="3", unique=True )
  name = models.CharField( max_length="255" )
  class Meta:
    app_label= 'catalogue'
  def __unicode__(self):
     return self.name


###############################################################################

class MissionSensor( models.Model ):
  """MissionSensor on the mission or satellite - e.g. HRV"""
  abbreviation = models.CharField( max_length="3", unique=True )
  name = models.CharField( max_length="255" )
  description = models.TextField()
  has_data = models.BooleanField(help_text='Mark false if there is no data for this sensor')
  class Meta:
    app_label= 'catalogue'
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
  class Meta:
    app_label= 'catalogue'
  def __unicode__(self):
     return self.name

###############################################################################

class SensorType( models.Model ):
  """Sensor type / camera number e.g. CAM1"""
  abbreviation = models.CharField( max_length="4", unique=True )
  name = models.CharField( max_length="255" )
  class Meta:
    app_label= 'catalogue'
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
  name = models.CharField( max_length="255" )
  details = models.TextField()
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

