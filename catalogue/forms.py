from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
import logging

from catalogue.models import *
from catalogue.datetimewidget import *
from catalogue.geometrywidget import *
from catalogue.sliderwidget import *
# Used for reading shapefiles etc
#from django.contrib.gis.gdal import DataSource

import datetime

# Support dmy formats (see http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
        '%d-%m-%Y',                         # '25-10-2005'
        '%d/%m/%Y', '%d/%m/%y',             # '25/10/2006', '25/12/06'
        '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
        '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
        )

class AdvancedSearchForm(forms.ModelForm):
  """ Let the user perform searches on sensors, by date and/or geometry digitised on map. """
  #keywords = forms.CharField(widget=forms.TextInput(attrs={'cols':'32'}),required=False)
  # Note1: the help_text strings are duplicated from the model help text
  #        since I didnt find a simple way to reuse it if adding custom fields
  # Note2: Only custom fields are added here. Fields that need no tweaking are
  #        pulled by the form generator directly from the model


  # ABP: the common part: will be searched on GenericProducts class only
  start_date = forms.DateField(widget=DateTimeWidget,required=True,input_formats=DATE_FORMATS,
      error_messages={'required': '''Entering a start date for your search is required.'''},
      help_text='Start date is required. DD-MM-YYYY.')
  end_date = forms.DateField(widget=DateTimeWidget,required=True,input_formats=DATE_FORMATS,
      error_messages={'required': '''Entering an end date for your search is required.'''},
      help_text='End date is required. DD-MM-YYYY.'
      )
  geometry = forms.CharField(widget=forms.HiddenInput(), required=False,
      help_text='Digitising an area of interest is not required but is recommended. You can use the help tab in the map area for more information on how to use the map. Draw an area of interest on the map to refine the set of search results to a specific area.')

  geometry_file = forms.FileField(widget = forms.FileInput(attrs={'class' : 'file'}),
                                  required = False,
                                  help_text = 'Upload a zipped shapefile of less than 1MB. If the shapefile contains\
                                              more than one polygon, only the first will be used. \
                                              Complex polygons will increase search time.')

  cloud_mean = forms.CharField(widget=SliderWidget(),
                                  required = False,
                                  label="Maximum cloud cover",
                                  help_text = 'Select the maximum cloud cover when searching for images. \
                                               Note that not all sensors support cloud cover filtering.\
                                              ')
  isAdvanced = forms.CharField(widget=forms.HiddenInput(), required = False)


  class Meta:
    model = Search
    exclude = ('ip_position' ,'guid' ,'keywords' ,'geometry_file' ,'user' ,'deleted' )

  # Simple way to assign css class to every field
  def __init__(self, *args, **kwargs):

    super(AdvancedSearchForm, self).__init__(*args, **kwargs)
    for myField in self.fields:
      self.fields[myField].widget.attrs['class'] = 'ui-corner-all'

  def clean_guid(self):
    """Custom validator for guid"""
    myCleanedData = self.cleaned_data
    myGuid = myCleanedData.get('guid')
    if not myGuid:
      myGuid='null'
      # we dont raise an error as we will just generate the guid in the model's save method
    return myGuid

  def clean_ip_position(self):
    myCleanedData = self.cleaned_data
    myPoint = myCleanedData.get('ip_position')
    if not myPoint:
      myPoint="SRID=4326;POINT(0 0)"
    return myPoint

  def clean_end_date(self):
    """End date validator"""
    #Note that required=False fields are not passed to cleaned_data but
    #rather just to self.data
    myData = self.data
    myEndDate = myData.get("end_date")
    if not myEndDate:
      # date is empty which is ok so do nothing
      pass
    else:
      try:
        myEndDate = datetime.datetime(*time.strptime(myEndDate, "%d-%m-%Y")[:6]).date()
      except:
        raise forms.ValidationError( "End date was not valid." )
      #pass
    return myEndDate

  def clean(self):
    myCleanedData = self.cleaned_data
    logging.info('cleaned data: ' + str(myCleanedData))
    try:
      myStartDate = myCleanedData.get("start_date")
      myEndDate = myCleanedData.get("end_date")
      if myEndDate and (myEndDate < myStartDate):
        raise forms.ValidationError("Error: Start date can not be after the end date!")
    except:
      raise forms.ValidationError("Error: Start date can not be after the end date! Both dates must be entered.")

    # ABP: checks for advanced search only (not in cleaned_data because it does not belong to Search model)
    if self.data.get('isAdvanced') == 'true':
      myStartSensorAngle = myCleanedData.get('sensor_inclination_angle_start')
      myEndSensorAngle = myCleanedData.get('sensor_inclination_angle_end')
      if (myStartSensorAngle and myEndSensorAngle) and (myEndSensorAngle < myStartSensorAngle):
        raise forms.ValidationError("Error: Start sensor angle can not be greater than the end sensor angle!")

      if int(myCleanedData.get('search_type')) in (Search.PRODUCT_SEARCH_OPTICAL, Search.PRODUCT_SEARCH_RADAR) and not myCleanedData.get('sensors'):
        raise forms.ValidationError("Error: Sensors are mandatory for sensors-based products search!")

    return self.cleaned_data



class AbbreviationModelChoiceField( forms.ModelChoiceField ):
  """Custom model choice field that shows abbreviated name rather than the default unicode representation
  so that we can show compact combo boxes. The associated model must have a field called abbreviation."""
  def label_from_instance(self, obj):
    return obj.abbreviation


class AbbreviationModelMultipleChoiceField( forms.ModelMultipleChoiceField ):
  """Custom model choice field that shows abbreviated name rather than the default unicode representation
  so that we can show compact combo boxes. The associated model must have a field called abbreviation."""
  def label_from_instance(self, obj):
    return obj.abbreviation



class ProductIdSearchForm( forms.Form ):
  """
  A special class of search form that allows to construct the search by
  building up a Product ID. This is intended to be used as an unbound form
  so the init function initialises the choices lists and so on.
  """
  mission = AbbreviationModelChoiceField( None, empty_label="*" , required = False)
  sensors = AbbreviationModelMultipleChoiceField(None, required = False)
  acquisition_mode = AbbreviationModelChoiceField(None, empty_label="*", required = False)
  sensor_type = AbbreviationModelChoiceField(None, empty_label="*", required = False)
  myRange = range(1970, datetime.date.today().year + 1)
  #zip creates a 2-tuple out of an array e.g. ((1970,1970),(1971,1971),etc....)
  start_year = forms.ChoiceField([(None, '*')] + zip(myRange,myRange))
  start_month = forms.ChoiceField( zip( range(1,13), range(1,13) ) )
  start_day = forms.ChoiceField( zip( range(1,32), range(1,32) ) )
  start_hour = forms.ChoiceField( zip( range(0,24), range(0,24) ), required = False)
  start_minute = forms.ChoiceField( zip( range(0,60),range(0,60) ), required = False)
  start_second = forms.ChoiceField( zip( range(0,60), range(0,60) ), required = False)
  end_year = forms.ChoiceField( zip(myRange,myRange) )
  end_month = forms.ChoiceField( zip( range(1,13), range(1,13) ) )
  end_day = forms.ChoiceField( zip( range(1,32), range(1,32) ) )
  end_hour = forms.ChoiceField( zip( range(0,24), range(0,24) ), required = False)
  end_minute = forms.ChoiceField( zip( range(0,60),range(0,60) ), required = False)
  end_second = forms.ChoiceField( zip( range(0,60), range(0,60) ), required = False)

  def __init__(self,*args,**kwargs):
    """
    Querysets will be filtered by existing search instance if passed in init
    """
    super ( ProductIdSearchForm, self ).__init__(*args,**kwargs)
    self.fields['mission'].queryset = Mission.objects.all()
    self.fields['sensors'].queryset = MissionSensor.objects.all()
    self.fields['acquisition_mode'].queryset = AcquisitionMode.objects.all()
    self.fields['sensor_type'].queryset = SensorType.objects.all()

  def clean(self):
    cleaned_data = self.cleaned_data
    try:
      self.cleaned_data['start_date'] = datetime.datetime(int(cleaned_data.get('start_year')), int(cleaned_data.get('start_month')), int(cleaned_data.get('start_day')), int(cleaned_data.get('start_hour')), int(cleaned_data.get('start_minute')), int(cleaned_data.get('start_second')))
    except ValueError, e:
      raise forms.ValidationError ('Error: start date is not valid. %s' % e)
    try:
      self.cleaned_data['end_date'] = datetime.datetime(int(cleaned_data.get('end_year')), int(cleaned_data.get('end_month')), int(cleaned_data.get('end_day')), int(cleaned_data.get('end_hour')), int(cleaned_data.get('end_minute')), int(cleaned_data.get('end_second')))
    except ValueError, e:
      raise forms.ValidationError ('Error: end date is not valid. %s' % e)

    if not self.cleaned_data['start_date'] <=  self.cleaned_data['end_date']:
      raise forms.ValidationError ('Error: date range is not valid.')

    return self.cleaned_data


class OrderStatusForm(forms.ModelForm):
  class Meta:
    model = OrderStatus

class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    #exclude = ('user','order_status')
    exclude = ('user','order_status',"processing_level","projection","datum","resampling_method","file_format","delivery_method")

class TaskingRequestForm(forms.ModelForm):
  geometry = forms.CharField(widget=GeometryWidget,required=False)
  geometry_file = forms.FileField(widget = forms.FileInput(attrs={'class' : 'file'}),
                                  required = False,
                                  help_text = 'Upload a zipped shapefile of less than 1MB. If the shapefile contains\
                                              more than one polygon, only the first will be used. \
                                              The computation time is related to polygon complexity.')
  target_date = forms.DateField(widget=DateTimeWidget,required=True,input_formats=DATE_FORMATS,
      error_messages={'required': '''Entering a target date for your tasking request is required.'''},
      help_text='Tasking target date is required. DD-MM-YYYY.'
      )
  class Meta:
    model = TaskingRequest
    #exclude = ('user','order_status')
    exclude = ('user','order_status',"processing_level","datum","file_format","delivery_method")


class OrderStatusHistoryForm(forms.ModelForm):
  class Meta:
    model = OrderStatusHistory
    exclude = ('order','user','order_change_date', 'old_order_status' )


class ClipForm(forms.ModelForm):
  """ Allows the CSIR Partner user to clip one of the Extra Layers by a given geometry. """

  image = forms.ChoiceField(choices = [(0,"zaSpot2mMosaic2009"),
                                       (1,"zaSpot2mMosaic2008"),
                                       (2,"zaSpot2mMosaic2007")] )
  geometry = forms.CharField(widget=GeometryWidget,required=False,
      help_text='You can digitise your clip area directly, or alternatively use the file upload option below to upload the clip shapefile. You can use the help tab in the map area for more information on how to use the map. Draw an area of interest on the map to refine the set of search results to a specific area.')
  geometry_file = forms.FileField(widget = forms.FileInput(attrs={'class' : 'file'}),
                                  required = False,
                                  help_text = 'Upload a zipped shapefile of less than 1MB. If the shapefile contains\
                                              more than one polygon, only the first will be used. \
                                              The computation time is related to polygon complexity.')

  class Meta:
    model = Clip
    exclude = ('result_url','owner','guid', 'status' )
