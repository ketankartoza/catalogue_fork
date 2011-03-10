# Django helpers for forming html pages
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
# python logging support to django logging middleware
import logging
from django.conf import settings

# Models and forms for our app
from catalogue.models import *
from catalogue.forms import *
from catalogue.renderDecorator import renderWithContext
from catalogue.profileRequiredDecorator import requireProfile
from django.db.models import Count, Min, Max #for aggregate queries

# For shopping cart and ajax product id search
from django.utils import simplejson

#shpresponder
from shapes.views import ShpResponder

# Helper classes
from helpers import *
from searcher import *

# for error logging
import traceback

# SHP and KML readers
from catalogue.featureReaders import *

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
@renderWithContext("orderListPage.html","orderList.html")
def listOrders(theRequest):
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
  return ({
        'myRecords': myRecords,
        'myUrl' : myUrl,
        'myCurrentMonth': datetime.date.today()
    })

@login_required
@renderWithContext('orderMonthlyReport.html')
def orderMonthlyReport( theRequest, theyear, themonth):
  #construct date object
  if not(theyear and themonth):
    myDate=datetime.date.today()
  else:
    try:
      myDate=datetime.date(int(theyear),int(themonth),1)
    except:
      logging.error("Date arguments cannot be parsed")
      logging.info(traceback.format_exc())

  if not theRequest.user.is_staff:
    '''Non staff users can only see their own orders listed'''
    myRecords = Order.base_objects.filter(user=theRequest.user).filter(order_date__month=myDate.month).filter(order_date__year=myDate.year).order_by('order_date')
  else:
    '''This view is strictly for staff only'''
    myRecords = Order.base_objects.filter(order_date__month=myDate.month).filter(order_date__year=myDate.year).order_by('order_date')

  return ({
    'myRecords': myRecords,
    'myCurrentDate': myDate,
    'myPrevDate':myDate - datetime.timedelta(days=1),
    'myNextDate':myDate + datetime.timedelta(days=31)
    })


@staff_member_required
def downloadClipGeometry(theRequest,theId):
  myOrder = get_object_or_404(Order,id=theId)

  if theRequest.GET.has_key('shp'):
    myResponder = ShpResponder( myOrder )
    myResponder.file_name = u'clip_geometry_order_%s' % myOrder.id
    return  myResponder.write_delivery_details( myOrder )
  elif theRequest.GET.has_key('kml'):
    return render_to_kml("kml/clipGeometry.kml", {'order' : myOrder,'external_site_url':settings.EXTERNAL_SITE_URL},u'clip_geometry_order_%s' % myOrder.id)
  elif theRequest.GET.has_key('kmz'):
    return render_to_kmz("kml/clipGeometry.kml", {'order' : myOrder,'external_site_url':settings.EXTERNAL_SITE_URL},u'clip_geometry_order_%s' % myOrder.id)
  else:
    logging.info('Request cannot be proccesed, unsupported download file type')
    raise Http404

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
         # myShowDeliveryDetailsFlag
         # myShowDeliveryDetailsFormFlag
         'myShowSensorFlag' : False,
         'myShowSceneIdFlag' : True,
         'myShowDateFlag': False,
         'myRemoveFlag': False, # cant remove stuff after order was placed
         'myThumbFlag' : False,
         'myShowMetdataFlag' : False,
         'myCartFlag' : False, #used when you need to add an item to the cart only
         'myPreviewFlag' : False,
         'myShowDeliveryDetailsFlag':True,
         'myShowDeliveryDetailsFormFlag':False,
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


@renderWithContext("deliveryDetailForm.html")
@login_required
def createDeilveryDetailForm( theRequest, theref_id):
  myDeliveryDetailForm = ProductDeliveryDetailForm(initial={'ref_id':theref_id},prefix='%i' % int(theref_id))
  return dict(myDeliveryDetailForm=myDeliveryDetailForm)

@renderWithContext("deliveryDetail.html")
@login_required
def showDeilveryDetail( theRequest, theref_id):
  myDeliveryDetail = DeliveryDetail.objects.filter(pk__exact=theref_id).get()
  return dict(myDeliveryDetail=myDeliveryDetail)

@requireProfile('addorder')
@login_required
def addOrder( theRequest ):
  logging.debug("Order called")
  myTitle = 'Create a new order'
  myRedirectPath = '/vieworder/'
  logging.info("Preparing order for user " + str(theRequest.user))
  myRecords = None
  myLayersList, myLayerDefinitions, myActiveBaseMap = standardLayers( theRequest )
  myCartLayer = '''var myCartLayer = new OpenLayers.Layer.WMS("Cart", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=CART&user=''' + str(theRequest.user.username) + '''",
          {
             version: '1.1.1',
             layers: 'Cart',
             srs: 'EPSG:4326',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false, singleTile:true});
           '''

  myLayersList=myLayersList[:-1]+', myCartLayer ]' #UGLY hack for adding Cart layer
  myLayerDefinitions.append(myCartLayer)

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
    # myShowDeliveryDetailsFlag
    # myShowDeliveryDetailsFormFlag
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
    'myShowDeliveryDetailsFlag': False,
    'myShowDeliveryDetailsFormFlag': True,
    'myCartTitle' : 'Order Product List',
    'myRecords' : myRecords,
    'myBaseTemplate' : "emptytemplate.html", #propogated into the cart template
    'mySubmitLabel' : "Submit Order",
    'myMessage' : " <div>Please specify any details for your order requirements below. If you need specific processing steps taken on individual images, please use the notes area below to provide detailed instructions.</div>",
    'myLayerDefinitions' : myLayerDefinitions,
    'myLayersList' : myLayersList,
    'myActiveBaseMap' : myActiveBaseMap

    }
  logging.info('Add Order called')
  if theRequest.method == 'POST':
    logging.debug("Order posted")

    myOrderForm = OrderForm( theRequest.POST,theRequest.FILES )
    myDeliveryDetailForm = DeliveryDetailForm( theRequest.POST,theRequest.FILES )

    #get ref_ids of product details forms, if any, and generate forms for validation
    myProductForms = [ProductDeliveryDetailForm(theRequest.POST,prefix='%i' % int(myref)) for myref in myDeliveryDetailForm.data.get('ref_id').split(',') if len(myref)>0]

    myOptions =  {
            'myOrderForm': myOrderForm,
            'myDeliveryDetailForm': myDeliveryDetailForm,
            'myTitle': myTitle,
            'mySubmitLabel' : "Submit Order",
          }
    myOptions.update(myExtraOptions) #shortcut to join two dicts
    if myOrderForm.is_valid() and myDeliveryDetailForm.is_valid() and all([form.is_valid() for form in myProductForms]):
      logging.debug("Order valid")

      myDeliveryDetailObject = myDeliveryDetailForm.save(commit=False)
      myDeliveryDetailObject.user = theRequest.user
      #check if user uploaded file and try to extract geometry
      try:
        myGeometry = getGeometryFromUploadedFile( theRequest, myDeliveryDetailForm, 'geometry_file' )
        if myGeometry:
          myDeliveryDetailObject.geometry = myGeometry
        else:
          logging.info("Failed to set search area from uploaded geometry file")
      except:
        logging.info("An error occurred trying to set search area from uploaded geometry file")
      myDeliveryDetailObject.user = theRequest.user
      myDeliveryDetailObject.save()
      #save order
      myObject = myOrderForm.save(commit=False)
      myObject.user = theRequest.user
      myObject.delivery_detail = myDeliveryDetailObject
      myObject.save()
      logging.debug("Order saved")

      #save all of the subforms
      myDeliveryDetailsProducts={}
      for mySubDeliveryForm in myProductForms:
        mySubData=mySubDeliveryForm.save(commit=False)
        mySubData.user=theRequest.user
        mySubData.save()
        #temporary store reference to deliverydetails with search record ID as a key
        myDeliveryDetailsProducts[int(mySubDeliveryForm.cleaned_data.get('ref_id'))]=mySubData
      #update serachrecords
      for myRecord in myRecords:
        #check if this record has sepcific DeliveryDetails
        if myDeliveryDetailsProducts.has_key(myRecord.id):
          myRecord.delivery_detail=myDeliveryDetailsProducts[myRecord.id]
        myRecord.order=myObject
        myRecord.save()

      logging.info('Add Order : data is valid')

      logging.debug("Search records added")
      #return HttpResponse("Done")
      #notifySalesStaff(theRequest.user,myObject.id)
      return HttpResponseRedirect(myRedirectPath + str(myObject.id))
    else:
      logging.info('Add Order: form is NOT valid')
      return render_to_response("addPage.html",
          myOptions,
          context_instance=RequestContext(theRequest))
  else: # new order
    myOrderForm = OrderForm( )
    myDeliveryDetailForm = DeliveryDetailForm()
    for myRec in myRecords:
      myRec.form = DeliveryDetailForm(initial={'ref_id':myRec.id},prefix='%i' % myRec.id)
    myOptions =  {
      'myOrderForm': myOrderForm,
      'myDeliveryDetailForm': myDeliveryDetailForm,
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
         # myShowDeliveryDetailsFlag
         # myShowDeliveryDetailsFormFlag
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
         'myShowDeliveryDetailsFlag':True,
         'myShowDeliveryDetailsFormFlag':False,
         'myBaseTemplate' : 'emptytemplate.html',
         })

@login_required
#renderWithContext is explained in renderWith.py
@renderWithContext('ordersSummary.html')
def ordersSummary(theRequest):
  #count orders by status
  myOrderStatus = OrderStatus.objects.annotate(num_orders=Count('order__id'))
  #count orders by product type (misson sensor)
  myOrderProductType = MissionSensor.objects.annotate(num_orders=Count('taskingrequest__order_ptr__id'))

  return dict(myOrderStatus=myOrderStatus, myOrderProductType=myOrderProductType)
