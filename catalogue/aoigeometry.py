from django import forms
import logging

from django.contrib.gis.geos import Point,Polygon

class AOIGeometryField(forms.CharField):
  widget = forms.TextInput
  
  def __init__(self, *args,**kwargs):
    super(AOIGeometryField,self).__init__(*args, **kwargs)
    self.label = "Area of interest"
    self.help_text ="Enter bounding box coordinates separated by comma for West, South, East and North edges i.e. (20,-34,22,-32), or enter single coordinate which defines circle center and radius in kilometers (20,-32,100)"

  def clean(self,value):
    """ AOI geometry validator """
    if not value:
      #do nothing, return empty string ''
      return ''
    else:
      try:
        myFields = value.split(',')

        #test if fields can be converted to nunbers
        try:
          myFields=[float(field) for field in myFields]
        except:
          logging.info("AOI geometry: invalid input values, can't be converted tu numbers: %s" % (value))
          raise
            
        #point and radius validation
        if len(myFields)==3:
          logging.info("AOI geometry: point and radius validation")
          if myFields[0] <= -180 or myFields[0] >= 180:
            logging.info("AOI geometry: point longitude not in -180..180 range: %f" % (myFields[0]))
            raise
          if myFields[1] <= -90 or myFields[1] >= 90:
            logging.info("AOI geometry: point latitude not in -90..90 range: %f" % (myFields[1]))
            raise
          if myFields[2] <= 0:
            logging.info("AOI geometry: radius equal or less then Zero: %f" % (myFields[2]))
            raise
        #bbox validation
        elif len(myFields)==4:
          logging.info("AOI geometry: bbox validation")
          if myFields[0] <= -180 or myFields[0] >= 180:
            logging.info("AOI geometry: west longitude not in -180..180 range: %f" % (myFields[0]))
            raise
          if myFields[2] <= -180 or myFields[2] >= 180:
            logging.info("AOI geometry: east longitude not in -180..180 range: %f" % (myFields[2]))
            raise
          if myFields[1] <= -90 or myFields[1] >= 90:
            logging.info("AOI geometry: south latitude not in -90..90 range: %f" % (myFields[1]))
            raise
          if myFields[3] <= -90 or myFields[3] >= 90:
            logging.info("AOI geometry: north latitude not in -90..90 range: %f" % (myFields[3]))
            raise
          #check bbox
          if myFields[0]>myFields[2]:
            logging.info("AOI geometry: west edge can't be after east edge: %f<%f" % (myFields[0],myFields[2]))
            raise

          if myFields[1]>myFields[3]:
            logging.info("AOI geometry: south edge can't be after north edge: %f<%f" % (myFields[1],myFields[3]))
            raise

          if myFields[0]==myFields[2]:
            logging.info("AOI geometry: west edge and east edge are identical: %f=%f" % (myFields[0],myFields[2]))
            raise
          if myFields[1]==myFields[3]:
            logging.info("AOI geometry: south edge and north edge are identical: %f=%f" % (myFields[1],myFields[3]))
            raise
        #unexpected number of arguments
        else:
          logging.info("AOI geometry: unexpected number of arguments: (%i),%s" % (len(myFields),value))
          raise
      except Exception,e:
        logging.info(str(e))
        raise forms.ValidationError( "Area of interest geometry is not valid." )
    
    return self.to_python(myFields)

  def to_python(self,value):
    if len(value)==3:
      #calculate radius in degrees 1 deg ~= 111 km
      myradius=value[2]/111.
      mygeometry=Point(value[0],value[1]).buffer(myradius)
    else:
      mygeometry=Polygon.from_bbox((value[0],value[3],value[2],value[1]))
    #set srid
    mygeometry.set_srid(4326)
    #geos must output geom as ewkt, because wkt doesm't contain SRID info
    return mygeometry.ewkt
