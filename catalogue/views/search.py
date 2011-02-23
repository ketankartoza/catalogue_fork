# Django helpers for forming html pages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.db.models import Count, Min, Max #for aggregate queries

# python logging support to django logging middleware
import logging

# Models and forms for our app
from catalogue.models import *
from catalogue.forms import *
from catalogue.renderDecorator import renderWithContext

# Helper classes
# For shopping cart and ajax product id search
from django.utils import simplejson
#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

from catalogue.views.helpers import *
from catalogue.views.searcher import *


@staff_member_required
def dataSummaryTable(theRequest):
  """
  Summary of available records
  """
  if not theRequest.user.is_staff:
    '''Non staff users cannot see this'''
    return

  #myResultSet = GenericProduct.objects.values("mission_sensor").annotate(Count("id")).order_by().aggregate(Min('product_acquisition_start'),Max('product_acquisition_end'))
  #ABP: changed to GenericSensorProduct
  myResultSet = GenericSensorProduct.objects.values("mission_sensor").annotate(Count("id")).order_by()
    #[{'mission_sensor': 6, 'id__count': 288307}, {'mission_sensor': 9, 'id__count': 289028}, {'mission_sensor': 3, 'id__count': 120943}, {'mission_sensor': 7, 'id__count': 222429}, {'mission_sensor': 5, 'id__count': 16624}, {'mission_sensor': 1, 'id__count': 3162}, {'mission_sensor': 2, 'id__count': 20896}, {'mission_sensor': 4, 'id__count': 17143}, {'mission_sensor': 8, 'id__count': 186269}]
  myResults = "<table><thead>"
  myResults += "</thead>"
  myResults += "<tbody>"
  myResults += "<tr><th>Sensor</th><th>Count</th></tr>"
  myCount = 0
  for myRecord in myResultSet:
    myResults += "<tr><td>%s</td><td>%s</td></tr>" % ( MissionSensor.objects.get(id=myRecord['mission_sensor']), myRecord['id__count'] )
    myCount += myRecord['id__count']
  myResults += "</tbody>"
  myResults += "<tr><th>All</th><th>%s</th></tr>" % ( myCount )
  myResults += "</table>"
  return HttpResponse(myResults)



@login_required
#theRequest context decorator not used here since we have different return paths
def search(theRequest):
  """
  Perform an attribute and spatial search for imagery
  """
  myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
  logging.debug(("Post vars:" + str(theRequest.POST)))
  logging.info( 'search called')
  if theRequest.method == 'POST':
    myForm = AdvancedSearchForm(theRequest.POST, theRequest.FILES)
    if myForm.is_valid():
      mySearch = myForm.save(commit=False)
      myLatLong = {'longitude':0,'latitude':0}
      if settings.USE_GEOIP:
        try:
          myGeoIpUtils = GeoIpUtils()
          myIp = myGeoIpUtils.getMyIp(theRequest)
          myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
        except:
          #raise forms.ValidationError( "Could not get geoip for this request" + traceback.format_exc() )
          # do nothing - better in a production environment
          pass
      if myLatLong:
        mySearch.ip_position = "SRID=4326;POINT(" + str(myLatLong['longitude']) + " " + str(myLatLong['latitude']) + ")"
      mySearch.user = theRequest.user
      mySearch.deleted = False
      try:
        myGeometry = getGeometryFromShapefile( theRequest, myForm, 'geometry_file' )
        if myGeometry:
          mySearch.geometry = myGeometry
        else:
          logging.info("Failed to set search area from uploaded shapefile")
      except:
        logging.info("An error occurred trying to set search area from uploaded shapefile")
      #check if aoi_geometry exists
      myAOIGeometry = myForm.cleaned_data.get('aoi_geometry')
      if myAOIGeometry:
        logging.info("Using AOI geometry, specified by user")
        mySearch.geometry = myAOIGeometry
      # else use the on-the-fly digitised geometry
      mySearch.save()
      """Another side effect of using commit=False is seen when your model has
      a many-to-many relation with another model. If your model has a
      many-to-many relation and you specify commit=False  when you save a form,
      Django cannot immediately save the form data for the many-to-many
      relation. This is because it isn't possible to save many-to-many data for
      an instance until the instance exists in the database.

      To work around this problem, every time you save a form using
      commit=False, Django adds a save_m2m() method to your ModelForm subclass.
      After you've manually saved the instance produced by the form, you can
      invoke save_m2m() to save the many-to-many form data.

      ref: http://docs.djangoproject.com/en/dev/topics/forms/modelforms/#the-save-method
      """
      myForm.save_m2m()
      logging.debug("Search: " + str( mySearch ))
      logging.info('form is VALID after editing')
      #test of registered user messaging system
      theRequest.user.message_set.create(message="Your search was carried out successfully.")
      return HttpResponseRedirect('/searchresult/' + mySearch.guid)
    else:

      logging.info('form is INVALID after editing')
      #render_to_response is done by the renderWithContext decorator
      return render_to_response ( 'search.html' ,{
        'myAdvancedFlag' : theRequest.POST['isAdvanced'] == 'true',
        'mySearchType' :  theRequest.POST['search_type'],
        'myForm': myForm,
        'myHost' : settings.HOST,
        'myLegendFlag' : True, #used to show the legend in the accordion
        'myLayerDefinitions' : myLayerDefinitions,
        'myLayersList' : myLayersList,
        'myActiveBaseMap' : myActiveBaseMap
        }, context_instance=RequestContext(theRequest))
  else:
    logging.info('initial search form being rendered')
    myForm = AdvancedSearchForm()
    #render_to_response is done by the renderWithContext decorator
    return render_to_response ( 'search.html' ,{
      'myAdvancedFlag' : False,
      'mySearchType' :  None,
      'myLegendFlag' : True, #used to show the legend in the accordion
      'myForm': myForm,
      'myHost' : settings.HOST,
      'myLayerDefinitions' : myLayerDefinitions,
      'myLayersList' : myLayersList,
      'myActiveBaseMap' : myActiveBaseMap
      }, context_instance=RequestContext(theRequest))


@login_required
def modifySearch(theRequest, theGuid):
  """
  Given a search guid, give the user a form prepopulated with
  that search's criteria so they can modify their search easily.
  A new search will be created from the modified one.
  """
  myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
  logging.info('initial search form being rendered')
  mySearch = get_object_or_404( Search, guid=theGuid )
  myForm = AdvancedSearchForm( instance = mySearch )
  #render_to_response is done by the renderWithContext decorator
  return render_to_response ( 'search.html' ,{
    'myAdvancedFlag' :  mySearch.isAdvanced,
    'mySearchType' :  mySearch.search_type,
    'myForm': myForm,
    'myGuid' : theGuid,
    'myHost' : settings.HOST,
    'myLayerDefinitions' : myLayerDefinitions,
    'myLayersList' : myLayersList,
    'myActiveBaseMap' : myActiveBaseMap
    }, context_instance=RequestContext(theRequest))



@login_required
#theRequest context decorator not used here since we have different return paths
def productIdSearch(theRequest, theGuid):
  """
  Display the product id builder, based on initial existing Search values,
  the following interaction is ajax based.
  This kind of search is only available when search_type is PRODUCT_SEARCH_OPTICAL
  """
  myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
  mySearch = get_object_or_404( Search, guid=theGuid)

  if mySearch.search_type != Search.PRODUCT_SEARCH_OPTICAL:
    raise Http500('productIdSearch is only available for products of type PRODUCT_SEARCH_OPTICAL')

  myInitialValues = mySearch.productIdAsHash()
  logging.info('productIdSearch initializing values from existing search %s' % theGuid)
  logging.info('productIdSearch initial values: %s' % myInitialValues)
  mySearcher = Searcher(theRequest, theGuid)
  mySearcher.search()
  myTemplateData = mySearcher.templateData()

  if theRequest.method == 'POST':
    myForm = ProductIdSearchForm(theRequest.POST, theRequest.FILES)
    if myForm.is_valid():
      logging.info('productIdSearch form is VALID after editing')
      logging.info('productIdSearch cleaned_data: %s' % myForm.cleaned_data)
      # Bind data
      for f in [f.name for f in mySearch._meta.fields]:
        if myForm.cleaned_data.has_key(f):
          setattr(mySearch, f, myForm.cleaned_data.get(f))
        mySearch.save()
      # Save m2m,
      # ABP: sensors is not required anymore for pivot oo work
      # ... should be required, but check anyway
      mySearch.sensors.clear()
      if myForm.cleaned_data.get('sensors'):
        for s in myForm.cleaned_data.get('sensors'):
          mySearch.sensors.add(s)
      if theRequest.is_ajax():
        # ABP: Returns a json object with query description.
        # We need to instanciate the Searcher since search logic
        # is not in the Search class :(
        mySearcher = Searcher(theRequest,theGuid)
        return HttpResponse(simplejson.dumps(mySearcher.describeQuery()), mimetype='application/json')
    else:
      logging.info('form is INVALID after editing')
      if theRequest.is_ajax():
        # Sends a 500
        return HttpResponseServerError(simplejson.dumps(myForm.errors), mimetype='application/json')
      return render_to_response ( 'productIdSearch.html' ,{
        'myForm': myForm,
        'theGuid' : theGuid,
      }, context_instance=RequestContext(theRequest))

  myForm = ProductIdSearchForm(initial = myInitialValues)
  logging.info('initial search form being rendered')
  myTemplateData['myForm'] = myForm
  myTemplateData['theGuid'] = theGuid
  myTemplateData['filterValues'] = simplejson.dumps(mySearcher.describeQuery()['values'])
  return render_to_response ( 'productIdSearch.html' , myTemplateData, context_instance=RequestContext(theRequest))


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def searchResultMap(theRequest, theGuid):
  """Renders a search results page including the map
  and all attendant html content"""
  mySearcher = Searcher(theRequest,theGuid)
  mySearcher.search()
  return(mySearcher.templateData())

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('page.html')
def searchResultPage(theRequest, theGuid):
  """Does the same as searchResultMap but renders only
  enough html to be inserted into a div"""
  mySearcher = Searcher(theRequest,theGuid)
  mySearcher.search()
  return(mySearcher.templateData())

@login_required
def searchResultShapeFile(theRequest, theGuid):
  """Return the search results as a shapefile"""
  mySearcher = Searcher(theRequest,theGuid)
  mySearcher.search( False ) # dont paginate
  myResponder = ShpResponder( SearchRecord )
  myResponder.file_name = theGuid + "-imagebounds"
  return myResponder.write_search_records( mySearcher.mSearchRecords )
