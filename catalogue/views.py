# Django helpers for forming html pages
from django.core.context_processors import csrf
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib.gis.shortcuts import render_to_kml, render_to_kmz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.db.models import Count, Min, Max #for aggregate queries
from django.forms.util import ErrorList

# for rendering template to email
from django.template.loader import render_to_string

# python logging support to django logging middleware
import logging

# Models and forms for our app
from catalogue.models import *
from catalogue.forms import *
from catalogue.shortcuts import render_to_geojson
from catalogue.renderDecorator import renderWithContext
from catalogue.profileRequiredDecorator import requireProfile
from catalogue.getFeaturesFromZipFile import *
from catalogue.getFeaturesFromKMLFile import *

# Helper classes
from catalogue.geoiputils import *
from catalogue.searcher import *
from catalogue.weblayers import *

#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

# PIL and os needed for making small thumbs
import os
from PIL import Image, ImageFilter, ImageOps

# For shopping cart
from django.utils import simplejson

# for sending email
from django.core.mail import send_mail,send_mass_mail

# for get feature info
import urllib2
import sys

# for error logging
import traceback


#### VIEW FUNCTIONS ####

#renderWithContext is explained in renderWith.py
@renderWithContext('index.html')
def index(theRequest):
  #render_to_response is done by the renderWithContext decorator
  myProfile = None
  return ( {
        'myPartnerFlag' : isStrategicPartner(theRequest)
      }
    )

#renderWithContext is explained in renderWith.py
@renderWithContext('about.html')
def about(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('contact.html')
def contact(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('mapHelp.html')
def mapHelp(theRequest):
  #render_to_response is done by the renderWithContext decorator
  if theRequest.is_ajax():
    return ( {"myTemplate" : "emptytemplate.html"})
  else:
    return ( {"myTemplate" : "base.html"})

#renderWithContext is explained in renderWith.py
@renderWithContext('emptyCartHelp.html')
def emptyCartHelp(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#renderWithContext is explained in renderWith.py
@renderWithContext('positionNotFound.html')
def positionNotFound(theRequest):
  #render_to_response is done by the renderWithContext decorator
  return ()

#Note: Dont use the login required decorator here -
# it causes the page to continually try to reload and cpu
# for firefix goes ballistic
#renderWithContext is explained in renderWith.py
@renderWithContext('sceneIdHelp.html')
def sceneIdHelp(theRequest):
  return


def logVisit(theRequest):
  """Silently log a visit and return an empty string. The
  best way to use this method is by adding it as a fake css
  reference at the top of your template e.g.:
  <link rel="stylesheet" href="/visit" type="text/css">
  """
  if settings.USE_GEOIP:
    myGeoIpUtils = GeoIpUtils()
    myIp = myGeoIpUtils.getMyIp(theRequest)
    if myIp:
      myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
      myVisit = Visit()
      try:
        if myLatLong['city']:
          myVisit.city = myLatLong['city']
        else:
          myVisit.city = 'Unknown'
      except:
        myVisit.city = 'Unknown'
      try:
        myVisit.country = myLatLong['country_name']
        myVisit.ip_position = Point(myLatLong['longitude'], myLatLong['latitude'])
        myVisit.ip_address = myIp
        # User is optional - we can see anonymous visits as they will have a null user
        if theRequest.user:
          myVisit.user = theRequest.user
      except:
        return HttpResponse('/** Error in geoip */',mimetype='text/css')
      myVisit.save()
      # If user is logged in, store their IP lat lon to their profile
      try:
        if theRequest.user:
          myProfile = theRequest.user.get_profile()
          myProfile.latitude = str(myLatLong['latitude'])
          myProfile.longitude = str(myLatLong['longitude'])
          myProfile.save()
      except:
          #user has no profile ...
          return HttpResponse('/** No Profile */',mimetype='text/css')
    else:
      logging.info('GEOIP capture failed to retrieve valid position info')
      return HttpResponse('/** No valid position */',mimetype='text/css')
  else:
    logging.info('GEOIP capture disabled in settings')
    return HttpResponse('/** Geoip disabled in settings */',mimetype='text/css')
  return HttpResponse('',mimetype='text/css')

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def whereAmI(theRequest):
  logging.info('whereAmI called...')
  myExtent = '(16,-34, 33, -22)'
  myMessages = []
  myGeoIpUtils = GeoIpUtils()
  myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
  if myLatLong:
    # Above returns something like:
    # {'city': 'Johannesburg', 'region': '06', 'area_code': 0, 'longitude':
    # 28.08329963684082, 'country_code3': 'ZAF', 'latitude': -26.200000762939453,
    # 'postal_code': None, 'dma_code': 0, 'country_code': 'ZA', 'country_name':
    # 'South Africa'}
    myHeading = '<h3><a href="#"><img src="/media/images/wherami_16.png">&nbsp;Your Location</a></h3>'
    myMessages.append('Nearest City: ' + str(myLatLong['city']))
    myMessages.append('Country: ' + str(myLatLong['country_name']))
    myMessages.append('Longitude: ' + str(myLatLong['longitude']))
    myMessages.append('Latitude: ' + str(myLatLong['latitude']))
    myIp = myGeoIpUtils.getMyIp(theRequest)
    myMessages.append('IP Address: ' + myIp)
    # Record the visitor details to our db
    myVisit = Visit()
    if myLatLong['city']:
      myVisit.city = myLatLong['city']
    else:
      myVisit.city = 'Unknown'
    myVisit.country = myLatLong['country_name']
    myVisit.ip_position = Point(myLatLong['longitude'], myLatLong['latitude'])
    myVisit.ip_address = myIp
    myVisit.save()
    myLayerString = """
       /*
       * Layer style
       */
       // we want opaque external graphics and non-opaque internal graphics
       var myLayerStyle = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
       myLayerStyle.fillOpacity = 0.2;
       myLayerStyle.graphicOpacity = 1;
       /*
       * Blue style
       */
       var myBlueStyle = OpenLayers.Util.extend({}, myLayerStyle);
       myBlueStyle.strokeColor = "blue";
       myBlueStyle.fillColor = "blue";
       myBlueStyle.graphicName = "star";
       myBlueStyle.pointRadius = 10;
       myBlueStyle.strokeWidth = 3;
       myBlueStyle.rotation = 45;
       myBlueStyle.strokeLinecap = "butt";
       var myLayer = new OpenLayers.Layer.Vector("Simple Geometry", {style: myLayerStyle});
       // create a point feature
       var myPoint = new OpenLayers.Geometry.Point(""" + str(myLatLong['longitude']) + "," + str(myLatLong['latitude']) + """);
       myPoint = transformPoint( myPoint );
       var myPointFeature = new OpenLayers.Feature.Vector(myPoint,null,myBlueStyle);
       myLayer.addFeatures([myPointFeature]);
       //map.setCenter(new OpenLayers.LonLat(point.x, point.y), 5);
                    """
    myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2009'],WEB_LAYERS['ZaRoadsBoundaries'], myLayerString ]
    myLayersList = "[zaSpot10mMosaic2009,zaRoadsBoundaries,myLayer]"
    return ( {
      'myGoogleFlag' : 'true',
      'myExtent' : myExtent,
      'myMessagesHeading' : myHeading,
      'myMessages' : myMessages,
      'myLayerDefinitions' : myLayerDefinitions,
      'myLayersList' : myLayersList,
      'myMessagesFlag' : True,
      })

  else:
    myHeading = '<h3><img src="/media/images/wherami_16.png">&nbsp;Your Location</h3>'
    myMessages.append( 'Sorry, we could not resolve your position.' )
    return ( {
      'myGoogleFlag' : None,
      'myExtent' : None,
      'myMessagesHeading' : myHeading,
      'myMessages' : myMessages,
      'myLayerDefinitions' : None,
      'myLayersList' : None,
      'myMessagesFlag' : True,
      })

def worldMap(theRequest):
  """Show a world"""
  myExtent = '(-180,-90,180,90)'
  myMessages = []
  myMessages.append('<h3>Nasa Blue Marble</h3>')
  myMessages.append('This is a generic mosaic of the world.')
  myLayerDefinitions = [ WEB_LAYERS['BlueMarble'] ]
  myLayersList = "[BlueMarble];"

  return render_to_response('map.html', {
    'myMessages' : myMessages,
    'myExtent' : myExtent,
    'myLayerDefinitions' : myLayerDefinitions,
    'myLayersList' : myLayersList
    })

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('addPage.html')
def clip(theRequest):
  """Show a spot map of South Africa"""
  myTitle = 'Clip Request'
  myExtent = '(15.256693,-35.325000,33.743307,-21.675000)'
  myHeading = '<h3><a href="#"><img src="/media/images/globe_16.png">&nbsp;2008 SPOT5 Mosaic</a></h3>'
  myMessages = []
  myMessages.append('<h3>SPOT5 Mosaic, South Africa</h3>')
  myMessages.append('Initial view is NASA Blue Marble Data, zoom in and the SPOT Mosaic will appear... ')
  myLayerDefinitions = None
  myLayersList = None
  myActiveBaseMap = None
  myProfile = None
  myForm = None

  try:
    myProfile = theRequest.user.get_profile()
  except:
    logging.debug('Profile does not exist')
  if myProfile and myProfile.strategic_partner:
    myLayerDefinitions = [ WEB_LAYERS['ZaSpot2mMosaic2009TC'], WEB_LAYERS['ZaSpot2mMosaic2008TC'], WEB_LAYERS['ZaSpot2mMosaic2007TC'], WEB_LAYERS['ZaRoadsBoundaries'] ]
    myLayersList = "[ zaSpot2mMosaic2009TC,zaSpot2mMosaic2008TC,zaSpot2mMosaic2007TC,zaRoadsBoundaries ]"
  else:
    myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2009'],WEB_LAYERS['ZaSpot10mMosaic2008'],WEB_LAYERS['ZaSpot10mMosaic2007'],WEB_LAYERS['ZaRoadsBoundaries'] ]
    myLayersList = "[zaSpot10mMosaic2009,zaSpot10mMosaic2008,zaSpot10mMosaic2007,zaRoadsBoundaries]"

  if theRequest.method == 'POST':
    myForm = ClipForm(theRequest.POST, theRequest.FILES)
    if myForm.is_valid():
      myObject = myForm.save(commit=False)
      myObject.owner = theRequest.user
      myGeometry = None
      try:
        myGeometry = getGeometryFromShapefile( theRequest, myForm, 'geometry_file' )
        if myGeometry:
          myObject.geometry = myGeometry
        else:
          logging.info("Failed to set clip area from uploaded shapefile")
          logging.info("Or no shapefile uploaded")
      except:
        logging.info("An error occurred try to set clip area from uploaded shapefile")
        logging.info(traceback.format_exc() )
      if not myObject.geometry:
        myErrors = myForm._errors.setdefault("geometry", ErrorList())
        myErrors.append(u"No valid geometry provided")
        logging.info('Form is NOT valid - at least a file or digitised geom is needed')
        return render_to_response("addPage.html",
            myOptions,
            context_instance=RequestContext(theRequest))

        myObject.save()


      logging.debug("Clip: " + str( myClip ))
      logging.info('form is VALID after editing')
      #test of registered user messaging system
      theRequest.user.message_set.create(message="Your clip request has been submitted successfully. Please wait for email notification of result availability.")
      return HttpResponseRedirect(myRedirectPath + str(myObject.id))
    else:
      logging.info('form is INVALID after editing')

      #render_to_response is done by the renderWithContext decorator
      return ({
        'myTitle': myTitle,
        'mySubmitLabel' : "Submit Clip Request",
        'myTaskingRequestFlag' : True,
        'myForm': myForm,
        'myMessages' : myMessages,
        'myMessagesHeading' : myHeading,
        'myMessagesFlag' : True,
        'myLayerDefinitions' : myLayerDefinitions,
        'myLayersList' : myLayersList,
        'myLegendFlag' : True, #used to show the legend in the accordion
        'myActiveBaseMap' : myActiveBaseMap
        })
  else:
    myForm = ClipForm()
    #render_to_response is done by the renderWithContext decorator
    return  ( {
      'myTitle': myTitle,
      'mySubmitLabel' : "Submit Clip Request",
      'myTaskingRequestFlag' : True,
      'myForm': myForm,
      'myMessages' : myMessages,
      'myMessagesHeading' : myHeading,
      'myMessagesFlag' : True,
      'myExtent' : myExtent,
      'myLayerDefinitions' : myLayerDefinitions,
      'myLegendFlag' : True, #used to show the legend in the accordion
      'myLayersList' : myLayersList
      })

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def visitorMap(theRequest):
  """Show a map of all visitors"""
  myGeoIpUtils = GeoIpUtils()
  myCount = Visit.objects.count()
  myExtent = '(-180.0,-90.0, 180.0, 90.0)'
  myMessages = []
  myLayerDefinitions = None
  myExtent = None
  myLayersList = None
  myLatLong = myGeoIpUtils.getMyLatLong(theRequest)
  # Above returns something like:
  # {'city': 'Johannesburg', 'region': '06', 'area_code': 0, 'longitude':
  # 28.08329963684082, 'country_code3': 'ZAF', 'latitude': -26.200000762939453,
  # 'postal_code': None, 'dma_code': 0, 'country_code': 'ZA', 'country_name':
  # 'South Africa'}
  myMessages.append('<h3>Your details</h3>')
  if not myLatLong:
    myMessages.append("Could not calculate your location")
  else:
    if myLatLong['city']:
      myMessages.append('Nearest City: ' + myLatLong['city'])
    else:
      myMessages.append('Nearest City: Unknown')
    myMessages.append('Country: ' + myLatLong['country_name'])
    myMessages.append('Longitude: ' + str(myLatLong['longitude']))
    myMessages.append('Latitude: ' + str(myLatLong['latitude']))
    myIp = myGeoIpUtils.getMyIp(theRequest)
    myMessages.append('IP Address: ' + myIp)
    myMessages.append('<h3>All visitors</h3>')
    myMessages.append('Total Site Visits: ' + str(myCount))
  myLayerDefinitions = [ WEB_LAYERS['BlueMarble'],WEB_LAYERS['Visitors'] ]
  myLayersList = "[BlueMarble,visitors]"

  #render_to_response is done by the renderWithContext decorator
  return ( {
    'myMessages' : myMessages,
    'myExtent' : myExtent,
    'myLayerDefinitions' : myLayerDefinitions,
    'myLayersList' : myLayersList,
    'myPartnerFlag' : isStrategicPartner(theRequest)
    })


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitorReport.html')
def visitorReport( theRequest ):
  myQuerySet = Visit()
  myCountryStats = myQuerySet.customSQL("""
  SELECT LOWER(country), COUNT(*) AS count, (SELECT COUNT(*)
  FROM catalogue_visit) AS total
  FROM catalogue_visit
  GROUP BY LOWER(country)
  ORDER BY count DESC;""", [ 'country', 'count', 'total' ] )

  myMaximum = 1
  myScores = []
  for myRec in myCountryStats:
    myValue = myRec['count']
    myTotal = myRec['total']
    myPercent = (myValue / myTotal) * 100
    myScores.append({'country' : myRec['country'],'count' : myRec['count'], 'total' : myRec['total'], 'percent': myPercent})
  myTopCountries = myScores[0:10]
  #by_date = query_set.customSQL("""
  #SELECT EXTRACT( year FROM added_date ) AS year, MIN( to_char( added_date, 'Mon' ) ), COUNT( * ) FROM users_qgisuser
  #GROUP BY EXTRACT( year FROM added_date ), EXTRACT( month FROM added_date )
  #ORDER BY EXTRACT( year FROM added_date );""", [ 'year', 'month', 'count' ] )

  #render_to_response is done by the renderWithContext decorator
  return ( {
        'myTopCountries': myTopCountries,
        'myScores': myScores}
        )


def standardLayers(theRequest):
  """Helper methods used to return standard layer defs for the openlayers control
     Note intended to be published as a view in urls.py
    e.g. usage:
    myLayersList, myLayerDefinitions, myActiveLayer = standardLayers( theRequest )"""

  myProfile = None
  myLayersList = None
  myLayerDefinitions = None
  myActiveBaseMap = None
  try:
    myProfile = theRequest.user.get_profile()
  except:
    logging.debug('Profile does not exist')
  if myProfile and myProfile.strategic_partner:
    myLayerDefinitions = [ WEB_LAYERS['ZaSpot2mMosaic2009TC'], WEB_LAYERS['ZaSpot2mMosaic2008TC'], WEB_LAYERS['ZaSpot2mMosaic2007TC'], WEB_LAYERS['ZaRoadsBoundaries'] ]
    myLayersList = "[ zaSpot2mMosaic2009TC,zaSpot2mMosaic2008TC,zaSpot2mMosaic2007TC,zaRoadsBoundaries ]"
    myActiveBaseMap =  "zaSpot2mMosaic2009TC"
  else:
    myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2009'],WEB_LAYERS['ZaSpot10mMosaic2008'],WEB_LAYERS['ZaSpot10mMosaic2007'],WEB_LAYERS['ZaRoadsBoundaries'] ]
    myLayersList = "[zaSpot10mMosaic2009,zaSpot10mMosaic2008,zaSpot10mMosaic2007,zaRoadsBoundaries]"
    myActiveBaseMap =  "zaSpot10mMosaic2009"
  return myLayersList, myLayerDefinitions, myActiveBaseMap

@login_required
#theRequest context decorator not used here since we have different return paths
def search(theRequest):
  """Perform an attribute and spatial search for imagery"""
  myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
  # check if the post ended with /?advanced for advanced searches
  logging.debug(("Post vars:" + str(theRequest.POST)))
  # get request because initial form is requested via ajax with a /?advanced url
  # if the advanced form should be show. Post request because the for
  myAdvancedFlag = theRequest.GET.has_key('advanced') or theRequest.POST.has_key('advanced')
  mySearchTemplate = None
  if theRequest.is_ajax():
    mySearchTemplate = "searchPanel.html"
  else:
    mySearchTemplate = "search.html"
  myForm = None
  logging.info( 'search called')
  if theRequest.method == 'POST':
    if myAdvancedFlag:
      myForm = AdvancedSearchForm(theRequest.POST, theRequest.FILES)
    else:
      myForm = SearchForm(theRequest.POST)
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
        #myGeometry = getGeometryFromShapefile( theRequest, myForm, 'geometry_file' )
        myGeometry = getGeometryFromKML( theRequest, myForm, 'geometry_file' )
        if myGeometry:
          mySearch.geometry = myGeometry
        else:
          logging.info("Failed to set search area from uploaded shapefile")
      except:
        logging.info("An error occurred trying to set search area from uploaded shapefile")
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
      return render_to_response ( mySearchTemplate ,{
        'myAdvancedFlag' : myAdvancedFlag,
        'myForm': myForm,
        'myHost' : settings.HOST,
        'myLegendFlag' : True, #used to show the legend in the accordion
        'myLayerDefinitions' : myLayerDefinitions,
        'myLayersList' : myLayersList,
        'myActiveBaseMap' : myActiveBaseMap
        }, context_instance=RequestContext(theRequest))
  else:
    logging.info('initial search form being rendered')
    if myAdvancedFlag:
      myForm = AdvancedSearchForm()
    else:
      myForm = SearchForm()
    #render_to_response is done by the renderWithContext decorator
    return render_to_response ( mySearchTemplate ,{
      'myAdvancedFlag' : myAdvancedFlag,
      'myLegendFlag' : True, #used to show the legend in the accordion
      'myForm': myForm,
      'myHost' : settings.HOST,
      'myLayerDefinitions' : myLayerDefinitions,
      'myLayersList' : myLayersList,
      'myActiveBaseMap' : myActiveBaseMap
      }, context_instance=RequestContext(theRequest))


@login_required
def modifySearch(theRequest, theGuid):
  """Given a search guid, give the user a form prepopulated with
  that search's criteria so they can modify their search easily.
  A new search will be created from the modified one.
  """
  myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
  mySearchTemplate = None
  if theRequest.is_ajax():
    mySearchTemplate = "searchPanel.html"
  else:
    mySearchTemplate = "search.html"
  logging.info('initial search form being rendered')
  mySearch = get_object_or_404( Search, guid=theGuid )
  myForm = AdvancedSearchForm( instance = mySearch )
  #render_to_response is done by the renderWithContext decorator
  return render_to_response ( mySearchTemplate ,{
    'myAdvancedFlag' : True,
    'myForm': myForm,
    'myHost' : settings.HOST,
    'myLayerDefinitions' : myLayerDefinitions,
    'myLayersList' : myLayersList,
    'myActiveBaseMap' : myActiveBaseMap
    }, context_instance=RequestContext(theRequest))


@login_required
#theRequest context decorator not used here since we have different return paths
def productIdSearch(theRequest):
  """Perform an attribute and spatial search for imagery using the product id builder"""
  myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
  mySearchTemplate = "productIdSearch.html"
  if theRequest.method == 'POST':
    myForm = ProductIdSearchForm(theRequest.POST, theRequest.FILES)
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
      # else use the on-the-fly digitised geometry
      mySearch.save()
      logging.debug("Search: " + str( mySearch ))
      logging.info('form is VALID after editing')
      #test of registered user messaging system
      theRequest.user.message_set.create(message="Your search was carried out successfully.")
      return HttpResponseRedirect('/searchresult/' + mySearch.guid)
    else:
      logging.info('form is INVALID after editing')
      #render_to_response is done by the renderWithContext decorator
      return render_to_response ( mySearchTemplate ,{
        'myForm': myForm,
        }, context_instance=RequestContext(theRequest))
  else:
    logging.info('initial search form being rendered')
    myForm = ProductIdSearchForm()
    #render_to_response is done by the renderWithContext decorator
    return render_to_response ( mySearchTemplate ,{
      'myForm': myForm,
      }, context_instance=RequestContext(theRequest))


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

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def showProduct(theRequest, theProductId):
  """Renders a search results page including the map
  and all attendant html content - for a single product only
  identified by its sac product ID"""
  mySearchRecord = None
  myExtent = None
  myMessages = []
  myProducts = GenericProduct.objects.filter(product_id__icontains=theProductId)
  if len( myProducts ) > 0:
    myProduct = myProducts[0]
    mySearchRecord = SearchRecord()
    mySearchRecord.user = theRequest.user
    mySearchRecord.product = myProduct
    myExtent = myProduct.spatial_coverage.envelope
    myMessages.append("Product found")
  else:
    myMessages.append("No matching product found")
  myExtraLayers = [ WEB_LAYERS['ZaSpot10mMosaic2008'],WEB_LAYERS['ZaRoadsBoundaries'] ]
  myLayersList = "[zaSpot10mMosaic2008,zaRoadsBoundaries]"
  return ({
        'myMessages' : myMessages,
        'myLayerDefinitions' : myExtraLayers,
        'myLayersList' : myLayersList,
        'myRecords' : [mySearchRecord],
        'myExtent' : myExtent,
        'myShowDetailFlag' : True,
        'myShowSceneIdFlag' : True,
        'myShowDateFlag': False,
        'myShowRemoveIconFlag': False, #used in cart contents listing context only
        'myShowHighlightFlag': True,
        'myShowRowFlag' : False,
        'myShowPathFlag' : False,
        'myShowCloudCoverFlag' : True,
        'myShowMetadataFlag' : True,
        'myShowCartFlag' : True,
        'myShowPreviewFlag' : True,
        'myLegendFlag' : True, #used to show the legend in the accordion
        'mySearchFlag' : True,
        })


@login_required
def showPreview(theRequest, theId, theSize):
  """Show a segment or scene thumbnail details,
    returning the result as a scaled down image.

    This is basically just a wrapper for the showThumb
    method but it returns a html document instead of an image
    mime type. And adds a link to the larger image.
    """
  return HttpResponse("""
        <center><img src="/thumbnail/"""
        + str(theId)
        + "/"
        + str(theSize)
        + """/"><center>"""
        + """<img src="/media/images/info_32.png" onclick='showMetadata(""" +  str(theId) + """);'  alt="Click to view metadata for this image" title="Click to view metadata for this image" />&nbsp;"""
        + """<img src="/media/images/buy_32.png" onclick='addToCart(""" +  str(theId) + """);'  alt="Click to add to your cart" title="Click to add this image to your cart" />&nbsp;"""
        + """<a id="large_preview" href="/thumbnailpage/"""
        + str(theId)
        + """/"><img src="/media/images/search_32.png" alt="Click for larger view" title="Click for larger preview"/></a>"""
        +"""</center>"""
        , mimetype="text/html")

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('thumbnail.html')
def showThumbPage(theRequest, theId):
  """Show a segment or scene thumbnail details in a popup dialog"""
  logging.info("showThumbPage : id " + theId)
  myDetails=[]
  myProduct = get_object_or_404( GenericProduct, id=theId )
  myDetails.append("<tr><th>Sensor: " + myProduct.mission_sensor.name + "</th></tr>")
  myImageFile = os.path.join( myProduct.thumbnailPath(), myProduct.product_id + ".jpg" )
  myDetails.append("<tr><td><center><img src=\"/thumbnails/" + myImageFile + "\"></center></td></tr>")
  #render_to_response is done by the renderWithContext decorator
  logging.info('Thumbnail path:   ' + str(settings.THUMBS_ROOT))
  logging.info('Media path    :   ' + str(settings.MEDIA_ROOT))
  logging.info('Project root path:' + str(settings.ROOT_PROJECT_FOLDER))
  return ( { 'myDetails' : myDetails } )

@login_required
def showThumb(theRequest, theId, theSize):
  """Show a scene thumbnail details,
    returning the result as a scaled down image."""
  logging.info("showThumb : id " + theId)
  myProduct = get_object_or_404( GenericProduct, id=theId )
  myImage = myProduct.thumbnail( theSize )
  myResponse = HttpResponse(mimetype="image/png")
  myImage.save(myResponse, "PNG")
  return ( myResponse )


@login_required
def metadataText(theRequest, theId):
  myGenericProduct = get_object_or_404( GenericProduct, id=theId )
  myString = "<pre>%s</pre>" % myGenericProduct.metadata
  return HttpResponse( myString )

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('productInfo.html')
def metadata(theRequest, theId):
  """Get the metadata for a product. The technique used here is
  to iterate through the product class properties using class introspection
  and generate a simple html document containing key/value pairs"""
  myGenericProduct = get_object_or_404( GenericProduct, id=theId )
  myObject, myType = myGenericProduct.getConcreteProduct()
  myDetails=[]
  myDetails.append( "<tr><th>Key</th><th>Value</th></tr>")
  if myObject:
    myDict = myObject.__dict__
    myDict.keys().sort()
    for myKey, myValue in myDict.items():
      #a couple of exceptions:
      if myKey is "spatial_coverage": continue
      #later we will treat the metadata field differently and parse it rather
      #than just return it verbatim
      myDetails.append("<tr><th>" + str(myKey).replace("_"," ").capitalize() + "</th><td> : " + str(myValue) + "</td></th>" )
  else:
    logging.info("Getting concrete class failed")
  return ( { 'myDetails' : myDetails } )

def searchKml(theRequest, theGuid):
  """Show a kml of a single search"""
  mySearch = get_object_or_404(Search, guid=theGuid)
  return render_to_kml("kml/search.kml", {'search' : mySearch})

def cartKml(theRequest):
  """Show a kml of a single search"""
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
  return render_to_kmz("kml/cart.kml", {'myRecords' : myRecords})

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('map.html')
def searchesMap(theRequest):
  """Show a map of all searches"""
  myMessages = []
  myLayerDefinitions = None
  myLayersList = None
  myExtent = '(-180.0,-90.0, 180.0, 90.0)'
  myMessages.append('<h3>All searches</h3>')
  myCount = Search.objects.count()
  myMessages.append('Total Searches: ' + str(myCount))
  myLayerDefinitions = [ WEB_LAYERS['BlueMarble'],WEB_LAYERS['Searches'] ]
  myLayersList = "[BlueMarble,searches]"
  #myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2009'],WEB_LAYERS['ZaRoadsBoundaries'], WEB_LAYERS['Searches'] ]
  #myLayersList = "[zaSpot10mMosaic2009,zaRoadsBoundaries,searches]"

  #render_to_response is done by the renderWithContext decorator
  return ( {
    'myMessages' : myMessages,
    'myExtent' : myExtent,
    'myLayerDefinitions' : myLayerDefinitions,
    'myLayersList' : myLayersList,
    'myPartnerFlag' : isStrategicPartner(theRequest),
    'myShowSearchFeatureInfoFlag' : 'true'
    })

#
# Visitor related views. Visits are recordings of site hits by
# IP and LatLong
#
def visitorsKml(theRequest):
  myVisits = VisitorReport.objects.kml()
  return render_to_kml("kml/visitorreport.kml", {'Visits' : myVisits})

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitors.html')
def visitorList(theRequest):
  myRecords = Visit.objects.all().order_by('-visit_date')
  # Paginate the results
  myPaginator = Paginator(myRecords, 10) # Show 25 contacts per page
  # Make sure page request is an int. If not, deliver first page.
  try:
    myPage = int(theRequest.GET.get('page', '1'))
  except ValueError:
    myPage = 1
  # If page request (9999) is out of range, deliver last page of results.
  try:
    myRecords = myPaginator.page(myPage)
  except (EmptyPage, InvalidPage):
    myRecords = myPaginator.page(myPaginator.num_pages)

  #render_to_response is done by the renderWithContext decorator
  return ({'myRecords': myRecords})

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('segmentBrowser.html')
def segmentBrowser(theRequest):
  myRecords = SegmentCommon.objects.all().order_by('-insertionDate')
  # Paginate the results
  myPaginator = Paginator(myRecords, 10) # Show 10 items per page
  # Make sure page request is an int. If not, deliver first page.
  try:
    myPage = int(theRequest.GET.get('page', '1'))
  except ValueError:
    myPage = 1
  # If page request (9999) is out of range, deliver last page of results.
  try:
    myRecords = myPaginator.page(myPage)
  except (EmptyPage, InvalidPage):
    myRecords = myPaginator.page(myPaginator.num_pages)

  #render_to_response is done by the renderWithContext decorator
  return ({'myRecords': myRecords})


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('mySearches.html')
def searchHistory(theRequest):
  searchHistory = Search.objects.filter(user=theRequest.user.id).filter(deleted=False).order_by('-search_date')
  return ({'mySearches' : searchHistory})

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('recentSearches.html')
def recentSearches(theRequest):
  searchHistory = Search.objects.filter(deleted=False).order_by('-search_date')
  if len( searchHistory ) > 50:
    searchHistory = searchHistory[0:50]
  return ({'mySearches' : searchHistory})

@login_required
def deleteSearch(theRequest, theId):
  """We don't ever actually delete a search since we need to see them
  all for site statistics. Rather we mark them as deleted so the
  user only sees his valid ones"""
  mySearch = None
  try:
    mySearch = Search.objects.get(id=theId)
    if mySearch.user == theRequest.user:
      mySearch.deleted=True
      mySearch.save()
    else:
      rasise ("Search not owned by you!")
  except Exception, myError:
    return HttpResponse("{'success' : False,'reason' : '" + myError + "'}", mimetype="text/plain")

  #return a simple json object
  return HttpResponse("{'success' : True}", mimetype="text/plain")


@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('myClips.html')
def clipHistory(theRequest):
  clipHistory = Clip.objects.filter(owner=theRequest.user).order_by('-date')
  return ({'myClips' : clipHistory})

###########################################################
#
# Shopping cart stuff
#
###########################################################

@login_required
def cartAsShapefile(theRequest):
  """Return the search results as a shapefile"""
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
  myResponder = ShpResponder( SearchRecord )
  myResponder.file_name = theRequest.user.username + '-cart'
  return myResponder.write_search_records( myRecords )

@login_required
def addToCart(theRequest, theId):
  logging.info("addToCart : id " + theId)

  """Optionally we can return the response as json for ajax clients.
  We still keep normal html response to support clients with no ajax support.
  see http://www.b-list.org/weblog/2006/jul/31/django-tips-simple-ajax-example-part-1/
  """
  # we need to check for the xhr param because response redirect
  # does not pass along the ajax request header to the redirect url
  # The redirected url needs to check for is_ajax or xhr to
  # decide how to respond# check if the post ended with /?xhr
  myAjaxFlag = theRequest.GET.has_key('xhr')

  # construct a record by passing some params
  myGenericProduct = GenericProduct.objects.get(id=theId)
  myDuplicateRecords = SearchRecord.objects.filter(product=myGenericProduct).filter(user=theRequest.user).filter(order__isnull=True)
  myResponse = None
  if len( myDuplicateRecords ) ==0:
    myRecord = SearchRecord().create( theRequest.user, myGenericProduct )
    myRecord.save()
    logging.info( "Adding item %s Cart :" + myRecord.product.product_id )
    if not myAjaxFlag:
      myResponse = HttpResponse("Successfully added " + myRecord.product.product_id + " to your myCart", mimetype="text/html")
    else:
      myDict = {"Item" : theId,"Status" : "Added"}
      myResponse = HttpResponse(simplejson.dumps(myDict), mimetype='application/javascript')
  else:
    logging.info( "Adding item %s Cart failed (its a duplicate):" + myGenericProduct.product_id )
    myResponse = HttpResponse("alert('Item already exists in your cart!');", mimetype="application/javascript")
  return myResponse


@login_required
def removeFromCart(theRequest, theId):
  myRecord = SearchRecord.objects.get(id=theId)
  if myRecord.user == theRequest.user:
    myRecord.delete()
    response = HttpResponse("Successfully removed item from your basket", mimetype="text/plain")
  else:
    response = HttpResponse("You don't own this record so you can not delete it!", mimetype="text/plain")
  return response

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('cartContents.html')
def showCartContents(theRequest):
  """Just returns a table element - meant for use with ajax"""
  myBaseTemplate = 'cartContentsPage.html'
  myAjaxFlag = theRequest.GET.has_key('xhr')
  if theRequest.is_ajax() or myAjaxFlag:
    myBaseTemplate = 'emptytemplate.html' #so template can render full page if not an ajax load
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
  logging.info("Cart contains : " + str(myRecords.count()) + " items")
  return ({
         'myRecords' : myRecords,
         # Possible flags for the record template
         # myShowSensorFlag
         # myShowSceneIdFlag
         # myShowDateFlag
         # myShowCartFlag
         # myShowRemoveIconFlag
         # myShowPreviewFlag
         'myShowSensorFlag' : False,
         'myShowSceneIdFlag' : True,
         'myShowDateFlag': True,
         'myShowRemoveIconFlag': True,
         'myShowRowFlag' : False,
         'myShowPathFlag' : False,
         'myShowCloudCoverFlag' : True,
         'myShowMetdataFlag' : True,
         'myShowCartFlag' : False, #used when you need to add an item to the cart only
         'myShowPreviewFlag' : True,
         'myCartTitle' : 'Cart Contents',
         'myBaseTemplate' : myBaseTemplate
         })

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('cartContents.html')
def showMiniCartContents(theRequest):
  """Just returns a table element - meant for use with ajax"""
  myBaseTemplate = 'cartContentsPage.html'
  myAjaxFlag = theRequest.GET.has_key('xhr')
  if theRequest.is_ajax() or myAjaxFlag:
    myBaseTemplate = 'emptytemplate.html' #so template can render full page if not an ajax load
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
  logging.info("Cart contains : " + str(myRecords.count()) + " items")
  return ({
         'myRecords' : myRecords,
         # Possible flags for the record template
         # myShowSensorFlag
         # myShowSceneIdFlag
         # myShowDateFlag
         # myShowCartFlag
         # myShowRemoveFlag
         # myShowPreviewFlag
         'myShowSensorFlag' : False,
         'myShowIdFlag' : False,
         'myShowSceneIdFlag' : True,
         'myShowDateFlag': False,
         'myShowRemoveIconFlag': True,
         'myShowRowFlag' : False,
         'myShowPathFlag' : False,
         'myShowCloudCoverFlag' : False,
         'myShowMetdataFlag' : False,
         'myShowCartFlag' : False, #used when you need to add an item to the cart only
         'myShowMiniCartFlag' : True, # so the appropriate jscrip is called when entry is deleted
         'myShowPreviewFlag' : False,
         'myBaseTemplate' : myBaseTemplate
         })

###########################################################
#
# Map Query related views
#
###########################################################


@login_required
def getFeatureInfo(theRequest,
                   theLon,
                   theLat,
                   theBoundingBox,
                   thePixelX,
                   thePixelY,
                   theMapWidth,
                   theMapHeight):
  """This is a blind proxy that we use to get around browser
  restrictions that prevent the Javascript from loading pages not on the
  same server as the Javascript.  This has several problems: it's less
  efficient, it might break some sites, and it's a security risk because
  people can use this proxy to browse the web and possibly do bad stuff
  with it.  It only loads pages via http and https, but it can load any
  content type. It supports GET and POST requests."""

  logging.debug("getFeatureInfo called \n Lon: %s Lat: %s BBox: %s X: %s Y: %s Height: %s Width: %s" % (
                   theLon,
                   theLat,
                   theBoundingBox,
                   thePixelX,
                   thePixelY,
                   theMapWidth,
                   theMapHeight))

  myGeometryQuery = Q(frame_geometry__intersects=(self.mSearch.geometry))
  myUrl = "http://" + settings.WMS_SERVER

  myHeaders = {"Content-Type": "text/plain"}
  myBody = "foo body"
  try:
    myRequest = urllib2.Request( myUrl, myBody, myHeaders )
    myResponse = urllib2.urlopen( myRequest )

    # logging.debug(content type header)
    myInfo = myResponse.info()
    if myInfo.has_key( "Content-Type" ):
      logging.debug("Content-Type: %s" % ( myInfo["Content-Type"] ))
    else:
      logging.debug("Content-Type: text/plain")

    logging.debug(myResponse.read())

    myResponse.close()

  except Exception, E:
    logging.debug("Status: 500 Unexpected Error")
    logging.debug("Content-Type: text/plain")
    logging.debug( )
    logging.debug("Some unexpected error occurred. Error text was:", E)

  return HttpResponse("Hello world")

###########################################################
#
# Ordering related views
#
###########################################################

@login_required
def myOrders(theRequest):
  '''Non staff users can only see their own orders listed'''
  myPath = "orderListPage.html"
  if theRequest.is_ajax():
    # No page container needed, just a snippet
    myPath = "orderList.html"
    logging.info("Ajax request for order list page received")
  else:
    logging.info("Non ajax request for order list page received")
  myRecords = Order.base_objects.filter(user=theRequest.user).order_by('-order_date')
  # Paginate the results
  myPaginator = Paginator(myRecords, 10)
  # Make sure page request is an int. If not, deliver first page.
  try:
    myPage = int(theRequest.GET.get('page', '1'))
  except ValueError:
    myPage = 1
    logging.info("Order list page request defaulting to page 1 because on an error in pagination")
  # If page request (9999) is out of range, deliver last page of results.
  try:
    myRecords = myPaginator.page(myPage)
  except (EmptyPage, InvalidPage):
    myRecords = myPaginator.page(myPaginator.num_pages)
  myUrl = "myorders"
  #render_to_response is done by the renderWithContext decorator
  return render_to_response(myPath,
      {
        'myRecords': myRecords,
        'myUrl' : myUrl
      },
      context_instance=RequestContext(theRequest))


@login_required
def listOrders(theRequest):
  myPath = "orderListPage.html"
  if theRequest.is_ajax():
    # No page container needed, just a snippet
    myPath = "orderList.html"
  myRecords = None
  if not theRequest.user.is_staff:
    '''Non staff users can only see their own orders listed'''
    myRecords = Order.base_objects.filter(user=theRequest.user).order_by('-order_date')
  else:
    '''This view is strictly for staff only'''
    myRecords = Order.base_objects.all().order_by('-order_date')
  # Paginate the results
  myPaginator = Paginator(myRecords, 10)
  # Make sure page request is an int. If not, deliver first page.
  try:
    myPage = int(theRequest.GET.get('page', '1'))
  except ValueError:
    myPage = 1
  # If page request (9999) is out of range, deliver last page of results.
  try:
    myRecords = myPaginator.page(myPage)
  except (EmptyPage, InvalidPage):
    myRecords = myPaginator.page(myPaginator.num_pages)
  myUrl = "listorders"
  #render_to_response is done by the renderWithContext decorator
  return render_to_response(myPath,
      {
        'myRecords': myRecords,
        'myUrl' : myUrl
      },
      context_instance=RequestContext(theRequest))

@login_required
def viewOrder (theRequest, theId):
  '''This view is strictly for staff only or the order owner'''
  # check if the post ended with /?xhr
  # we do this as well as is_ajax call because we
  # may have arrived at this page via a response redirect
  # which will not then have the is_ajax flag set
  myAjaxFlag = theRequest.GET.has_key('xhr')
  myTemplatePath = "orderPage.html"
  if theRequest.is_ajax() or myAjaxFlag:
    # No page container needed, just a snippet
    myTemplatePath = "orderPageAjax.html"
    logging.debug("Request is ajax enabled")
  myOrder = get_object_or_404(Order,id=theId)
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order=myOrder)
  if not ((myOrder.user == theRequest.user) or (theRequest.user.is_staff)):
    raise Http404
  myHistory = OrderStatusHistory.objects.all().filter(order=theId)
  myForm = None
  if theRequest.user.is_staff:
    myForm = OrderStatusHistoryForm()
  #render_to_response is done by the renderWithContext decorator
  return render_to_response(myTemplatePath,
      {  'myOrder': myOrder,
         'myRecords' : myRecords,
         # Possible flags for the record template
         # myShowSensorFlag
         # myShowSceneIdFlag
         # myShowDateFlag
         # myCartFlag
         # myRemoveFlag
         # myThumbFlag
         'myShowSensorFlag' : False,
         'myShowSceneIdFlag' : True,
         'myShowDateFlag': False,
         'myRemoveFlag': False, # cant remove stuff after order was placed
         'myThumbFlag' : False,
         'myShowMetdataFlag' : False,
         'myCartFlag' : False, #used when you need to add an item to the cart only
         'myPreviewFlag' : False,
         'myForm' : myForm,
         'myHistory' : myHistory,
         'myCartTitle' : 'Product List',
      },
      context_instance=RequestContext(theRequest))

@login_required
def updateOrderHistory(theRequest):
  if not theRequest.user.is_staff:
    return HttpResponse('''Access denied''')
  if not theRequest.method == 'POST':
    return HttpResponse('''You can only access this view from a form POST''')
  myTemplatePath = "orderPage.html"
  if theRequest.is_ajax():
    # No page container needed, just a snippet
    myTemplatePath = "orderStatusHistory.html"
    logging.debug("Request is ajax enabled")
  myOrderId = theRequest.POST['order']
  myOrder = get_object_or_404(Order,id=myOrderId)
  myNewStatusId = theRequest.POST["new_order_status"]
  myNotes = theRequest.POST["notes"]
  myNewStatus = get_object_or_404(OrderStatus,id=myNewStatusId)

  myOrderStatusHistory = OrderStatusHistory()
  myOrderStatusHistory.order = myOrder
  myOrderStatusHistory.old_order_status=myOrder.order_status
  myOrderStatusHistory.new_order_status=myNewStatus
  myOrderStatusHistory.user=theRequest.user
  myOrderStatusHistory.notes=myNotes
  try:
    myOrderStatusHistory.save()
  except:
    return HttpResponse("<html><head></head><body>Query error - please report to SAC staff</body></html>")
  myOrder.order_status=myNewStatus
  myOrder.save()
  myHistory = OrderStatusHistory.objects.all().filter(order=myOrderId)
  # These next few lines and the long list of options below needed for no ajax fallback
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order=myOrder)
  myForm = None
  if theRequest.user.is_staff:
    myForm = OrderStatusHistoryForm()
  if TaskingRequest.objects.filter(id=myOrderId):
    notifySalesStaffOfTaskRequest(theRequest.user,myOrderId)
  else:
    notifySalesStaff(theRequest.user,myOrderId)
  return render_to_response(myTemplatePath,
      {  'myOrder': myOrder,
         'myRecords' : myRecords,
         'myShowSensorFlag' : True,
         'myShowSceneIdFlag' : True,
         'myShowDateFlag': True,
         'myRemoveFlag': False, # cant remove stuff after order was placed
         'myThumbFlag' : False,
         'myShowMetdataFlag' : False,
         'myCartFlag' : False, #used when you need to add an item to the cart only
         'myPreviewFlag' : False,
         'myForm' : myForm,
         'myHistory' : myHistory,
         'myCartTitle' : 'Product List',
      },
      context_instance=RequestContext(theRequest))



@requireProfile('addorder')
@login_required
def    addOrder( theRequest ):
  logging.debug("Order called")
  myTitle = 'Create a new order'
  myRedirectPath = '/vieworder/'
  logging.info("Preparing order for user " + str(theRequest.user))
  myRecords = None
  if str(theRequest.user) == "AnonymousUser":
    logging.debug("User is anonymous")
    logging.info("Anonymous users can't have items in their cart")
    myMessage = "If you want to order something, you need to create an account and log in first."
    return HttpResponse( myMessage )
  else:
    logging.debug("User NOT anonymous")
    myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
    if myRecords.count() < 1:
      logging.debug("Cart has no records")
      logging.info("User has no items in their cart")
      return HttpResponseRedirect( "/emptyCartHelp/" )
    else:
      logging.debug("Cart has records")
      logging.info("Cart contains : " + str(myRecords.count()) + " items")
  myExtraOptions = {
         # Possible flags for the record template
         # myShowSensorFlag
         # myShowIdFlag
         # myShowSceneIdFlag
         # myShowDateFlag
         # myShowCartFlag
         # myShowRemoveIconFlag
         # myShowPreviewFlag
         'myShowSensorFlag' : False,
         'myShowSceneIdFlag' : True,
         'myShowDateFlag': False,
         'myShowRemoveIconFlag': True,
         'myShowRowFlag' : False,
         'myShowPathFlag' : False,
         'myShowCloudCoverFlag' : True,
         'myShowMetdataFlag' : False,
         'myShowCartFlag' : False, #used when you need to add an item to the cart only
         'myShowCartContentsFlag' : True, #used when you need to add an item to the cart only
         'myShowPreviewFlag' : False,
         'myCartTitle' : 'Order Product List',
         'myRecords' : myRecords,
         'myBaseTemplate' : "emptytemplate.html", #propogated into the cart template
         'mySubmitLabel' : "Submit Order",
         'myMessage' : " <div>Please specify any details for your order requirements below. If you need specific processing steps taken on individual images, please use the notes area below to provide detailed instructions.</div>",
         }
  logging.info('Add Order called')
  if theRequest.method == 'POST':
    logging.debug("Order posted")
    myForm = OrderForm( theRequest.POST,theRequest.FILES )
    myOptions =  {
            'myForm': myForm,
            'myTitle': myTitle,
            'mySubmitLabel' : "Submit Order",
          }
    myOptions.update(myExtraOptions), #shortcut to join two dicts
    if myForm.is_valid():
      logging.debug("Order valid")
      myObject = myForm.save(commit=False)
      myObject.user = theRequest.user
      myObject.save()
      logging.debug("Order saved")
      logging.info('Add Order : data is valid')
      # Now add the cart contents to the order
      myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
      for myRecord in myRecords:
        myRecord.order=myObject
        myRecord.save()
      logging.debug("Search records added")
      #return HttpResponse("Done")
      notifySalesStaff(theRequest.user,myObject.id)
      return HttpResponseRedirect(myRedirectPath + str(myObject.id))
    else:
      logging.info('Add Order: form is NOT valid')
      return render_to_response("addPage.html",
          myOptions,
          context_instance=RequestContext(theRequest))
  else: # new order
    myForm = OrderForm( )
    myOptions =  {
          'myForm': myForm,
          'myTitle': myTitle,
          'mySubmitLabel' : "Submit Order",
        }
    myOptions.update(myExtraOptions), #shortcut to join two dicts
    logging.info( 'Add Order: new object requested' )
    return render_to_response("addPage.html",
        myOptions,
        context_instance=RequestContext(theRequest))

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('cartContents.html')
def viewOrderItems(theRequest,theOrderId):
  """Just returns a table element - meant for use with ajax"""
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order=theOrderId)
  return ({
         'myRecords' : myRecords,
         # Possible flags for the record template
         # myShowSensorFlag
         # myShowSceneIdFlag
         # myShowDateFlag
         # myShowCartFlag
         # myShowRemoveIconFlag
         # myShowPreviewFlag
         'myShowSensorFlag' : False,
         'myShowSceneIdFlag' : True,
         'myShowDateFlag': False,
         'myShowRemoveIconFlag': False,
         'myShowRowFlag' : False,
         'myShowPathFlag' : False,
         'myShowCloudCoverFlag' : False,
         'myShowMetdataFlag' : False,
         'myShowCartFlag' : False, #used when you need to add an item to the cart only
         'myShowPreviewFlag' : False,
         'myBaseTemplate' : 'emptytemplate.html',
         })

###########################################################
#
# Tasking related views
#
###########################################################

@login_required
def viewTaskingRequest (theRequest, theId):
  '''
  Used to get a detailed view of a single tasking request.
  This view is strictly for staff only or the tasking request owner'''
  # check if the post ended with /?xhr
  # we do this as well as is_ajax call because we
  # may have arrived at this page via a response redirect
  # which will not then have the is_ajax flag set
  myAjaxFlag = theRequest.GET.has_key('xhr')
  myTemplatePath = "taskingRequestPage.html"
  if theRequest.is_ajax() or myAjaxFlag:
    # No page container needed, just a snippet
    myTemplatePath = "taskingRequestPageAjax.html"
    logging.debug("Request is ajax enabled")
  myTaskingRequest = get_object_or_404(TaskingRequest, id=theId)
  if not ((myTaskingRequest.user == theRequest.user) or (theRequest.user.is_staff)):
    raise Http404
  myHistory = OrderStatusHistory.objects.all().filter(order=theId)
  myForm = None
  if theRequest.user.is_staff:
    myForm = OrderStatusHistoryForm()
  #render_to_response is done by the renderWithContext decorator
  return render_to_response(myTemplatePath,
      {  'myTaskingRequest': myTaskingRequest,
         'myHistory' : myHistory,
         'myForm' : myForm,
      },
      context_instance=RequestContext(theRequest))

@login_required
def myTaskingRequests(theRequest):
  '''Used to get an overview listing of tasking requests.
  Non staff users can only see their own orders listed'''
  myPath = "taskingRequestPage.html"
  if theRequest.is_ajax():
    # No page container needed, just a snippet
    myPath = "taskingRequestList.html"
  myRecords = TaskingRequest.objects.filter(user=theRequest.user).order_by('-order_date')
  # Paginate the results
  myPaginator = Paginator(myRecords, 10)
  # Make sure page request is an int. If not, deliver first page.
  try:
    myPage = int(theRequest.GET.get('page', '1'))
  except ValueError:
    myPage = 1
  # If page request (9999) is out of range, deliver last page of results.
  try:
    myRecords = myPaginator.page(myPage)
  except (EmptyPage, InvalidPage):
    myRecords = myPaginator.page(myPaginator.num_pages)
  myUrl = "mytaskingrequests"
  #render_to_response is done by the renderWithContext decorator
  return render_to_response(myPath,
      {
        'myRecords': myRecords,
        'myUrl' : myUrl
      },
      context_instance=RequestContext(theRequest))

@requireProfile('addtaskingrequest')
@login_required
def    addTaskingRequest( theRequest ):
  """Used to create a new tasking request"""
  logging.debug(("Post vars:" + str(theRequest.POST)))
  logging.debug(("Post files:" + str(theRequest.FILES)))
  myLayerDefinitions = [ WEB_LAYERS['ZaSpot10mMosaic2009'],WEB_LAYERS['ZaRoadsBoundaries'] ]
  myLayersList = "[zaSpot10mMosaic2009,zaRoadsBoundaries]"
  logging.debug("Add tasking request called")
  myTitle = 'Create a new tasking request'
  myRedirectPath = '/viewtaskingrequest/'
  logging.info("Preparing tasking request for user " + str(theRequest.user))
  myRecords = None
  if str(theRequest.user) == "AnonymousUser":
    logging.debug("User is anonymous")
    logging.info("Anonymous users can't have items in their cart")
    myMessage = "If you want to make a tasking request, you need to create an account and log in first."
    return HttpResponse( myMessage )

  if theRequest.method == 'POST':
    logging.debug("Tasking request posted")
    myForm = TaskingRequestForm( theRequest.POST,theRequest.FILES )
    myOptions =  {
            'myForm': myForm,
            'myTitle': myTitle,
            'mySubmitLabel' : "Submit Tasking Request",
            'myTaskingRequestFlag' : True,
            'myLayerDefinitions' : myLayerDefinitions,
            'myLayersList' : myLayersList,
          }
    if myForm.is_valid():
      logging.debug("Tasking Request valid")
      myObject = myForm.save(commit=False)
      myObject.user = theRequest.user
      myGeometry = None
      try:
        myGeometry = getGeometryFromShapefile( theRequest, myForm, 'geometry_file' )
        if myGeometry:
          myObject.geometry = myGeometry
        else:
          logging.info("Failed to set tasking request from uploaded shapefile")
          logging.info("Or no shapefile uploaded")
      except:
        logging.info("An error occurred try to set tasking area from uploaded shapefile")
        logging.info(traceback.format_exc() )
      if not myObject.geometry:
        myErrors = myForm._errors.setdefault("geometry", ErrorList())
        myErrors.append(u"No valid geometry provided")
        logging.info('Form is NOT valid - at least a file or digitised geom is needed')
        return render_to_response("addPage.html",
            myOptions,
            context_instance=RequestContext(theRequest))

      myObject.save()
      logging.debug("Tasking Request saved")
      logging.info('Tasking request : data is valid')
      # Now add the cart contents to the order
      notifySalesStaffOfTaskRequest(theRequest.user,myObject.id)
      return HttpResponseRedirect(myRedirectPath + str(myObject.id))
    else:
      logging.info('Add Tasking Request : form is NOT valid')
      return render_to_response("addPage.html",
          myOptions,
          context_instance=RequestContext(theRequest))
  else: # new order
    myForm = TaskingRequestForm( )
    myOptions =  {
          'myForm': myForm,
          'myTitle': myTitle,
          'mySubmitLabel' : "Submit Tasking Request",
          'myTaskingRequestFlag' : True,
          'myLayerDefinitions' : myLayerDefinitions,
          'myLayersList' : myLayersList,
        }
    logging.info( 'Add Tasking Request: new object requested' )
    return render_to_response("addPage.html",
        myOptions,
        context_instance=RequestContext(theRequest))

@login_required
def taskingRequestAsShapefile(theRequest, theTaskingRequestId):
  """Return the a tasking request results as a shapefile"""
  myRecords = TaskingRequest.objects.filter(id=theTaskingRequestId)
  if myRecords[0].user != theRequest.user and not theRequest.user.is_staff:
    myJscript= """<script>alert('Error: You do not own this request, so you cannot download its geometry.</script>"""
    return HttpResponse( myJscript, mimetype='application/javascript' )
  myResponder = ShpResponder( SearchRecord )
  myResponder.file_name = 'taskingarea%s' % theTaskingRequestId
  return myResponder.write_request_records( myRecords )

###########################################################
#
# Generic and helper methods
#
###########################################################


# Note this code is from Tims personal codebase and copyright is retained
@login_required
def genericAdd(theRequest,
    theFormClass,
    theTitle,
    theRedirectPath,
    theOptions
    ):
  myObject = getObject(theFormClass)
  logging.info('Generic add called')
  if theRequest.method == 'POST':
    # create a form instance using reflection
    # see http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname/452981
    myForm = myObject(theRequest.POST,theRequest.FILES)
    myOptions =  {
            'myForm': myForm,
            'myTitle': theTitle
          }
    myOptions.update(theOptions), #shortcut to join two dicts
    if myForm.is_valid():
      myObject = myForm.save(commit=False)
      myObject.user = theRequest.user
      myObject.save()
      logging.info('Add : data is valid')
      return HttpResponseRedirect(theRedirectPath + str(myObject.id))
    else:
      logging.info('Add : form is NOT valid')
      return render_to_response('add.html',
          myOptions,
          context_instance=RequestContext(theRequest))
  else:
    myForm = myObject()
    myOptions =  {
          'myForm': myForm,
          'myTitle': theTitle
        }
    myOptions.update(theOptions), #shortcut to join two dicts
    logging.info('Add : new object requested')
    return render_to_response('add.html',
        myOptions,
        context_instance=RequestContext(theRequest))

def genericDelete(theRequest,theObject):
  if theObject.user != theRequest.user:
    return ({"myMessage" : "You can only delete an entry that you own!"})
  else:
    theObject.delete()
    return ({'myMessage' : "Entry was deleted successfully"})

def getObject( theClass ):
  #Create an object instance using reflection
  #from http://stackoverflow.com/questions/452969/does-python-have-an-equivalent-to-java-class-forname/452981
  myParts = theClass.split('.')
  myModule = ".".join(myParts[:-1])
  myObject = __import__( myModule )
  for myPath in myParts[1:]:
    myObject = getattr(myObject, myPath)
  return myObject


@login_required
def isStrategicPartner(theRequest):
  """Returns true if the current user is a CSIR strategic partner
  otherwise false"""
  myProfile = None
  try:
    myProfile = theRequest.user.get_profile()
  except:
    logging.debug('Profile does not exist')
  myPartnerFlag = False
  if myProfile and myProfile.strategic_partner:
    myPartnerFlag = True
  return myPartnerFlag


###########################################################
#
# Email notification of orders to sac sales staff
#
###########################################################
def notifySalesStaff(theUser, theOrderId):
  """ A helper method to notify sales staff who are subscribed to a sensor
     Example usage from the console / doctest:
     >>> from catalogue.models import *
     >>> from catalogue.views import *
     >>> myUser = User.objects.get(id=1)
     >>> myUser
     >>> notifySalesStaff( myUser, 16 )"""

  if not settings.EMAIL_NOTIFICATIONS_ENABLED:
    return
  myOrder = get_object_or_404(Order,id=theOrderId)
  myRecords = SearchRecord.objects.all().filter(user=theUser).filter(order=myOrder)
  myHistory = OrderStatusHistory.objects.all().filter(order=myOrder)
  myEmailSubject = 'SAC Order ' + str(myOrder.id) + ' status update (' + myOrder.order_status.name + ')'
  myEmailMessage = 'The status for order #' +  str(myOrder.id) + ' has changed. Please visit the order page:\n'
  myEmailMessage = myEmailMessage + 'http://' + settings.DOMAIN + '/vieworder/' + str(myOrder.id) + '/\n\n\n'
  myTemplate = "orderEmail.txt"
  myEmailMessage += render_to_string( myTemplate, { 'myOrder': myOrder,
                                                    'myRecords' : myRecords,
                                                    'myHistory' : myHistory
                                                  })
  # Get a list of all the mission sensors involved in this order:
  myMissionSensors = []
  for myRecord in myRecords:
    mySensor = myRecord.product.mission_sensor
    if not mySensor in myMissionSensors:
      myMissionSensors.append(mySensor)
  # Get a list of staff user's email addresses
  myMessagesList = [] # we will use mass_mail to prevent users seeing who other recipients are
  for myMissionSensor in myMissionSensors:
    myRecipients = OrderNotificationRecipients.objects.filter(sensors__id__exact=myMissionSensor.id)
    for myRecipient in myRecipients:
      myAddress = myRecipient.user.email
      myMessagesList.append((myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN, [myAddress]))
      logging.info("Sending notice to : %s" % myAddress)
  #also send an email to the originator of the order
  #We do this separately to avoid them seeing the staff cc list
  myClientAddress = theUser.email 
  myMessagesList.append((myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN, [myClientAddress]))
  # mass mail expects a tuple (read-only list) so convert the list to tuple on send
  logging.info("Sending messages: \n%s" % tuple(myMessagesList) )
  send_mass_mail( tuple(myMessagesList),fail_silently=False )
  return

###########################################################
#
# Email notification of tasking requests to sac sales staff
#
###########################################################
def notifySalesStaffOfTaskRequest(theUser, theId):
  """ A helper method to notify tasking staff who are subscribed to a sensor
     Example usage from the console / doctest:
     >>> from catalogue.models import *
     >>> from catalogue.views import *
     >>> myUser = User.objects.get(id=1)
     >>> myUser
     >>> notifySalesStaffOfTaskRequest( myUser, 11 )"""
  if not settings.EMAIL_NOTIFICATIONS_ENABLED:
    return
  myTaskingRequest = get_object_or_404(TaskingRequest,id=theId)
  myHistory = OrderStatusHistory.objects.all().filter(order=myTaskingRequest)
  myEmailSubject = 'SAC Tasking Request ' + str(myTaskingRequest.id) + ' status update (' + myTaskingRequest.order_status.name + ')'
  myEmailMessage = 'The status for tasking order #' +  str(myTaskingRequest.id) + ' has changed. Please visit the tasking request page:\n'
  myEmailMessage = myEmailMessage + 'http://' + settings.DOMAIN + '/viewtaskingrequest/' + str(myTaskingRequest.id) + '/\n\n\n'
  myTemplate = "taskingEmail.txt"
  myEmailMessage += render_to_string( myTemplate, { 'myOrder': myTaskingRequest,
                                                    'myHistory' : myHistory
                                                  })
  myRecipients = OrderNotificationRecipients.objects.filter(sensors__id__exact = myTaskingRequest.mission_sensor.id)
  myAddresses = []
  for myRecipient in myRecipients:
    myAddresses.append(myRecipient.user.email)
  logging.info("Sending notices to : %s" % myAddresses)
  send_mail(myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN,
          myAddresses, fail_silently=False)
  #also send an email to the originator of the order
  #We do this separately to avoid them seeing the staff cc list
  myAddresses = [ theUser.email ]
  send_mail(myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN,
          myAddresses, fail_silently=False)
  return

###########################################################
#
# Summary of available records
#
###########################################################

@staff_member_required
def dataSummaryTable(theRequest):
  if not theRequest.user.is_staff:
    '''Non staff users cannot see this'''
    return

  #myResultSet = GenericProduct.objects.values("mission_sensor").annotate(Count("id")).order_by().aggregate(Min('product_acquisition_start'),Max('product_acquisition_end'))
  myResultSet = GenericProduct.objects.values("mission_sensor").annotate(Count("id")).order_by()
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




###########################################################
#
# Try to extract a geometry if a shp was uploaded
#
###########################################################
def getGeometryFromShapefile( theRequest, theForm, theFileField ):
  """Retrieve an uploaded geometry from a shp file. Note in order for this to
     work, you must have set your form to use multipart encoding type e.g.
     <form enctype="multipart/form-data" action="/search/" method="post" id="search_form">"""
  logging.info('Form cleaned data: ' + str(theForm.cleaned_data))
  if theRequest.FILES[theFileField]:
    logging.debug("Using geometry from shapefile.")
    #if not theForm.cleaned_data.contains( "theFileField" ):
    #  logging.error("Error: %s field not submitted with form" % theFileField)
    #  return False
    myExtension = theForm.cleaned_data[theFileField].name.split(".")[1]
    if myExtension != "zip":
      logging.info('Wrong format for uploaded geometry. Please select a ZIP archive.')
      #render_to_response is done by the renderWithContext decorator
      #@TODO return a clearer error spotmap just like Alert for the missing dates
      return False
    myFile = theForm.cleaned_data[theFileField]
    myOutFile = '/tmp/%s' % myFile.name
    destination = open(myOutFile, 'wb+')
    for chunk in myFile.chunks():
      destination.write(chunk)
    destination.close()
    extractedGeometries = getFeaturesFromZipFile(myOutFile, "Polygon", 1)
    myGeometry = extractedGeometries[0]
    return myGeometry


def getGeometryFromKML( theRequest, theForm, theFileField ):
  """Retrieve an uploaded geometry from a shp file. Note in order for this to
     work, you must have set your form to use multipart encoding type e.g.
     <form enctype="multipart/form-data" action="/search/" method="post" id="search_form">"""
  logging.info('Form cleaned data: ' + str(theForm.cleaned_data))
  if theRequest.FILES[theFileField]:
    logging.debug("Using geometry from KML.")
    #if not theForm.cleaned_data.contains( "theFileField" ):
    #  logging.error("Error: %s field not submitted with form" % theFileField)
    #  return False
    myExtension = theForm.cleaned_data[theFileField].name.split(".")[1]
    if not(myExtension.lower() == "kml" or myExtension.lower() == "kmz"):
      logging.info('Wrong format for uploaded geometry. Please select a KML/KMZ file.')
      #render_to_response is done by the renderWithContext decorator
      #@TODO return a clearer error spotmap just like Alert for the missing dates
      return False
    myFile = theForm.cleaned_data[theFileField]
    myOutFile = '/tmp/%s' % myFile.name
    destination = open(myOutFile, 'wb+')
    for chunk in myFile.chunks():
      destination.write(chunk)
    destination.close()
    extractedGeometries = getFeaturesFromKML(myOutFile, "Polygon", 1)
    myGeometry = extractedGeometries[0]
    return myGeometry

