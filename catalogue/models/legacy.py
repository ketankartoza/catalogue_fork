from django.contrib.gis.db import models

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
    app_label= 'catalogue'
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
    app_label= 'catalogue'
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
    app_label= 'catalogue'
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
    app_label= 'catalogue'
    db_table = '"import"."cbers"'
    #requires django 1.1
    managed = False

