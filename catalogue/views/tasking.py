from catalogue.renderDecorator import renderWithContext
from catalogue.profileRequiredDecorator import requireProfile
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

#Dane Springmeyer's django-shapes app for exporting results as a shpfile
from shapes.views import ShpResponder

# Models and forms for our app
from catalogue.models import *

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

