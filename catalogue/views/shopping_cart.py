from django.contrib.auth.decorators import login_required
from catalogue.renderDecorator import renderWithContext
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

# Models and forms for our app
from catalogue.models import *

# For shopping cart and ajax product id search
from django.utils import simplejson

# Helper classes (render_as_kml, ...)
from helpers import *

###########################################################
#
# Shopping cart stuff
#
###########################################################

@login_required
def downloadCart(theRequest):
  """Dispaches request and returns products in cart in desired file format"""
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)

  myFilename = u'%s-cart' % theRequest.user.username
  if theRequest.GET.has_key('shp'):
    myResponder = ShpResponder( myRecords )
    myResponder.file_name = myFilename
    return  myResponder.write_order_products( myRecords )
  elif theRequest.GET.has_key('kml'):
    return render_to_kml("kml/searchRecords.kml", {
        'mySearchRecords' : myRecords, 
        'external_site_url':settings.DOMAIN, 
        'transparentStyle':True
      }, 
      myFilename)
  elif theRequest.GET.has_key('kmz'):
    return render_to_kmz("kml/searchRecords.kml", {
        'mySearchRecords' : myRecords, 
        'external_site_url':settings.DOMAIN, 
        'transparentStyle':True,
        'myThumbsFlag': True
      }, myFilename)
  else:
    logging.info('Request cannot be proccesed, unsupported download file type')
    raise Http404

@login_required
def downloadCartMetadata(theRequest):
  """Returns ISO 19115 metadata for products in cart, unless request is suffixed with ?html"""
  myRecords = SearchRecord.objects.all().filter(user=theRequest.user).filter(order__isnull=True)
  if theRequest.GET.has_key('html'):
    return downloadHtmlMetadata(myRecords,'Cart-%s' % theRequest.user.username)
  else:
    return downloadISOMetadata(myRecords,'Cart-%s' % theRequest.user.username)

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
