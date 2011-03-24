###########################################################
#
# Initialization, generic and helper methods
#
###########################################################
import logging

from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect,HttpResponse

from catalogue.models import *
from django.template import RequestContext
# for rendering template to email
from django.template.loader import render_to_string

# for sending email
from django.core.mail import send_mail,send_mass_mail

# for kmz
import zipfile
from cStringIO import StringIO

# Read from settings
CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS = getattr(settings, 'CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS', False )

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
     >>> notifySalesStaff( myUser, 16 )

  """

  if not settings.EMAIL_NOTIFICATIONS_ENABLED:
    logging.info("Email sending disabled, set EMAIL_NOTIFICATIONS_ENABLED in settings")
    return
  myOrder = get_object_or_404(Order,id=theOrderId)
  myRecords = SearchRecord.objects.filter(user=theUser, order=myOrder).select_related()
  myHistory = OrderStatusHistory.objects.filter(order=myOrder)
  myEmailSubject = 'SAC Order ' + str(myOrder.id) + ' status update (' + myOrder.order_status.name + ')'
  myEmailMessage = 'The status for order #' +  str(myOrder.id) + ' has changed. Please visit the order page:\n'
  myEmailMessage = myEmailMessage + 'http://' + settings.DOMAIN + '/vieworder/' + str(myOrder.id) + '/\n\n\n'
  myTemplate = "orderEmail.txt"
  myEmailMessage += render_to_string( myTemplate, { 'myOrder': myOrder,
                                                    'myRecords' : myRecords,
                                                    'myHistory' : myHistory
                                                  })

  # Get a list of staff user's email addresses
  myMessagesList = [] # we will use mass_mail to prevent users seeing who other recipients are

  myRecipients = set()
  # get the list of recipients
  for myProduct in [s.product for s in myRecords]:
    myRecipients.update(OrderNotificationRecipients.getUsersForProduct(myProduct))

  for myRecipient in myRecipients:
    myAddress = myRecipient.email
    myMessagesList.append((myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN, [myAddress]))
    logging.info("Sending notice to : %s" % myAddress)

  # Add default
  if not myRecipients and CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS:
    logging.info("Sending notice to default recipients : %s" % CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)
    myMessagesList.append((myEmailSubject, myEmailMessage, settings.DEFAULT_FROM_EMAIL, list(CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)))

  #also send an email to the originator of the order
  #We do this separately to avoid them seeing the staff cc list
  myClientAddress = theUser.email
  myMessagesList.append((myEmailSubject, myEmailMessage, settings.DEFAULT_FROM_EMAIL, [myClientAddress]))
  # mass mail expects a tuple (read-only list) so convert the list to tuple on send
  logging.info("Sending messages: \n%s" % myMessagesList)
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
    logging.info("Email sending disabled, set EMAIL_NOTIFICATIONS_ENABLED in settings")
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
  myMessagesList = [] # we will use mass_mail to prevent users seeing who other recipients are
  myRecipients = OrderNotificationRecipients.objects.filter(sensors=t.mission_sensor)
  for myRecipient in myRecipients:
    myMessagesList.append((myEmailSubject, myEmailMessage, 'dontreply@' + settings.DOMAIN,
          [myRecipient.user.email]))
    logging.info("Sending notices to : %s" % myRecipient.user.email)

  # Add default
  if not myRecipients and CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS:
    logging.info("Sending notice to default recipients : %s" % CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)
    myMessagesList.append((myEmailSubject, myEmailMessage, settings.DEFAULT_FROM_EMAIL, list(CATALOGUE_DEFAULT_NOTIFICATION_RECIPIENTS)))

  #also send an email to the originator of the order
  #We do this separately to avoid them seeing the staff cc list
  myMessagesList.append((myEmailSubject, myEmailMessage, settings.DEFAULT_FROM_EMAIL,
          [ theUser.email ]))
  send_mass_mail(tuple(myMessagesList), fail_silently=False)
  return


"""Layer definitions for use in conjunction with open layers"""
WEB_LAYERS = {
            # Streets and boundaries for SA base map with an underlay of spot 2009 2m mosaic
            #
            # Uses the degraded 2.5m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
          'ZaSpot2mMosaic2009TC' : '''var zaSpot2mMosaic2009TC = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2009TC", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic2m2009',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2008 mosaic
            #
            # Uses the degraded 2m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
          'ZaSpot2mMosaic2008TC' : '''var zaSpot2mMosaic2008TC = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2008TC", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic2m2008',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2007 mosaic
            #
            # Uses the degraded 2m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
          'ZaSpot2mMosaic2007TC' : '''var zaSpot2mMosaic2007TC = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2007TC", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic2m2007',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2009 mosaic
            # and under that blue marble. Its rendered as a single layer for best quality.
            'ZaSpot2mMosaic2009' : '''var zaSpot2mMosaic2009 = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2009", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT2009",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             layers: 'Roads',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
           # Streets and boundaries for SA base map with an underlay of spot 2008 mosaic
           # and under that blue marble. Its rendered as a single layer for best quality.
           'ZaSpot2mMosaic2008' : '''var zaSpot2mMosaic2008 = new OpenLayers.Layer.WMS(
           "ZaSpot2mMosaic2008", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT2008",
           {
              width: '800',
              layers: 'Roads',
              srs: 'EPSG:900913',
              maxResolution: '156543.0339',
              VERSION: '1.1.1',
              EXCEPTIONS: "application/vnd.ogc.se_inimage",
              height: '525',
              format: 'image/jpeg',
              transparent: 'false',
              antialiasing: 'true'
            },
            {isBaseLayer: true});
           ''',
           # Streets and boundaries for SA base map with an underlay of spot 2007 mosaic
           # and under that blue marble. Its rendered as a single layer for best quality.
           'ZaSpot2mMosaic2007' : '''var zaSpot2mMosaic2007 = new OpenLayers.Layer.WMS(
          "ZaSpot2mMosaic2007", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT2007",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             layers: 'Roads',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2009 mosaic
            #
            # Uses the degraded 10m product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
            # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaSpot10mMosaic2009' : '''var zaSpot10mMosaic2009 = new OpenLayers.Layer.WMS(
          "ZaSpot10mMosaic2009", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic10m2009',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2008 mosaic
            #
            # Uses the degraded 10 product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
            # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaSpot10mMosaic2008' : '''var zaSpot10mMosaic2008 = new OpenLayers.Layer.WMS(
          "ZaSpot10mMosaic2008", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic10m2008',
             maxResolution: '156543.0339',
             srs: 'EPSG:900913',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
            # Streets and boundaries for SA base map with an underlay of spot 2007 mosaic
            #
            # Uses the degraded 10 product in a tile cache
            #
            # and under that blue marble. Its rendered as a single layer for best quality.
            # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaSpot10mMosaic2007' : '''var zaSpot10mMosaic2007 = new OpenLayers.Layer.WMS(
          "ZaSpot10mMosaic2007", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             //layers: 'Roads',
             layers: 'spot5mosaic10m2007',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
           #a Vector only version of the above
           # "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_VECTOR",
          'ZaRoadsBoundaries' : '''var zaRoadsBoundaries = new OpenLayers.Layer.WMS(
          "ZaRoadsBoundaries", "http://''' + settings.WMS_SERVER + '''/cgi-bin/tilecache.cgi?",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             //layers: 'Roads',
             layers: 'za_vector',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/jpeg',
             transparent: 'false',
             antialiasing: 'true'
           },
           {isBaseLayer: true});
           ''',
            # Map of all search footprints that have been made.
            # Transparent: true will make a wms layer into an overlay
            'Searches' : '''var searches = new OpenLayers.Layer.WMS(
          "Searches", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=SEARCHES",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             layers: 'searches',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false});
           ''',
        # Map of site visitors
        # Transparent: true will make a wms layer into an overlay
        'Visitors' : '''var visitors = new OpenLayers.Layer.WMS(
          "Visitors", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=VISITORS",
          {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             width: '800',
             layers: 'visitors',
             styles: '',
             srs: 'EPSG:900913',
             maxResolution: '156543.0339',
             height: '525',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false}
        );
        ''',
        # Spot5 ZA 2008 10m Mosaic directly from mapserver
            'ZaSpot5Mosaic2008' : '''var zaSpot5Mosaic2008 = new OpenLayers.Layer.WMS( "SPOT5 10m Mosaic 2008, ZA",
            "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=ZA_SPOT",
            {
              VERSION: '1.1.1',
              EXCEPTIONS: "application/vnd.ogc.se_inimage",
              layers: "Spot5_RSA_2008_10m",
              maxResolution: '156543.0339',
            });
            zaSpot5Mosaic2008.setVisibility(false);
            ''',
        # Nasa Blue marble directly from mapserver
            'BlueMarble' : '''var BlueMarble = new OpenLayers.Layer.WMS( "BlueMarble",
            "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=WORLD",
            {
             VERSION: '1.1.1',
             EXCEPTIONS: "application/vnd.ogc.se_inimage",
             layers: "BlueMarble",
             maxResolution: '156543.0339'
            });
            BlueMarble.setVisibility(false);
            ''',
        #
        # Google
        #
       'GooglePhysical' : '''var gphy = new OpenLayers.Layer.Google(
           "Google Physical",
           {type: G_PHYSICAL_MAP}
           );
       ''',
        #
        # Google streets
        #
        'GoogleStreets' : '''var gmap = new OpenLayers.Layer.Google(
           "Google Streets" // the default
           );
        ''',
        #
        # Google hybrid
        #
        'GoogleHybrid' : ''' var ghyb = new OpenLayers.Layer.Google(
           "Google Hybrid",
           {type: G_HYBRID_MAP}
           );
        ''',
        #
        # Google Satellite
        #
        'GoogleSatellite' : '''var gsat = new OpenLayers.Layer.Google(
           "Google Satellite",
           {type: G_SATELLITE_MAP}
           );
        ''',
        #
        # Heatmap - all
        #
        'Heatmap' : '''var heatmap_all = new OpenLayers.Layer.Image(
                'Heatmap All',
                '/media/heatmaps/heatmap-total.png',
                new OpenLayers.Bounds(-20037508.343,-16222639.241,20019734.329,16213801.068),
                new OpenLayers.Size(1252,1013),
                {isBaseLayer: false,
                maxResolution: 156543.0339,
                opacity:0.8
                }
            );
        ''',
        }

mLayerJs = {'VirtualEarth' : '''<script src='http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6.1'></script>
         ''',
         'Google' : '''
          <script src='http://maps.google.com/maps?file=api&amp;v=2&amp;key='{{GOOGLE_MAPS_API_KEY}}'></script>
          '''}



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


#render_to_kml helpers
def render_to_kml(theTemplate,theContext,filename):
  response = HttpResponse(render_to_string(theTemplate,theContext))
  response['Content-Type'] = 'application/vnd.google-earth.kml+xml'
  response['Content-Disposition'] = 'attachment; filename=%s.kml' % filename
  return response

def render_to_kmz(theTemplate,theContext,filename):
  response = HttpResponse(render_to_string(theTemplate,theContext))
  kmz = StringIO()
  f = zipfile.ZipFile(kmz, 'w', zipfile.ZIP_DEFLATED)
  f.writestr('%s.kml' % filename, response.content)
  f.close()
  response.content = kmz.getvalue()
  kmz.close()
  response['Content-Type']        = 'application/vnd.google-earth.kmz'
  response['Content-Disposition'] = 'attachment; filename=%s.kmz' % filename
  response['Content-Length']      = str(len(response.content))
  return response
