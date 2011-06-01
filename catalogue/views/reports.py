# Django helpers for forming html pages
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.gis.shortcuts import render_to_kml, render_to_kmz
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.forms.util import ErrorList

# for aggregate queries
from django.db.models import Count, Min, Max #for aggregate queries
# python logging support to django logging middleware
import logging

# Models and forms for our app
from catalogue.models import *
from catalogue.renderDecorator import renderWithContext

# View Helper classes
from geoiputils import *
from helpers import *

# for error logging
import traceback

# for date handling
import datetime

@staff_member_required
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
    'myGraphLabel': ({'Country':'country'}),
    'myTopCountries': myTopCountries,
    'myScores': myScores,
    'myCurrentMonth': datetime.date.today()
    })

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('visitorMonthlyReport.html')
def visitorMonthlyReport( theRequest, theyear, themonth):
  #construct date object
  if not(theyear and themonth):
    myDate=datetime.date.today()
  else:
    try:
      myDate=datetime.date(int(theyear),int(themonth),1)
    except:
      logging.error("Date arguments cannot be parsed")
      logging.info(traceback.format_exc())

  myQuerySet = Visit()
  myCountryStats = myQuerySet.customSQL("""
  SELECT LOWER(country),count(*) as count, DATE_TRUNC('month',
  visit_date) as month
  FROM catalogue_visit
  WHERE visit_date BETWEEN to_date(%(date)s,'MM-YYYY') AND to_date(%(date)s,'MM-YYYY')+ interval '1 month'
  GROUP BY LOWER(country),DATE_TRUNC('month',visit_date)
  ORDER BY month DESC""",['country','count','month'],{'date':myDate.strftime('%m-%Y')})
  myMaximum = 1
  myScores = []
  for myRec in myCountryStats:
    myScores.append({'country' : myRec['country'],'count' : myRec['count']})
  myTopCountries = myScores[0:10]

  return ({
    'myGraphLabel': ({'Country':'country'}),
    'myTopCountries': myTopCountries,
    'myScores': myScores,
    'myCurrentDate': myDate,
    'myPrevDate':myDate - datetime.timedelta(days=1),
    'myNextDate':myDate + datetime.timedelta(days=31),
    })



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
  return ({'mySearches' : searchHistory,'myCurrentMonth':datetime.date.today()})

#monthly search report by user ip_position
@staff_member_required
@renderWithContext('searchMonthlyReport.html')
def searchMonthlyReport( theRequest, theyear, themonth):
  #construct date object
  if not(theyear and themonth):
    myDate=datetime.date.today()
  else:
    try:
      myDate=datetime.date(int(theyear),int(themonth),1)
    except:
      logging.error("Date arguments cannot be parsed")
      logging.info(traceback.format_exc())

  myQuerySet = Search()
  myCountryStats = myQuerySet.customSQL("""
  SELECT name,date_trunc('month',search_date) as date_of_search, count(*) as searches
  FROM (SELECT a.name, b.search_date FROM catalogue_worldborders a INNER JOIN catalogue_search b ON st_intersects(a.geometry,b.ip_position) OFFSET 0) ss
  WHERE search_date BETWEEN to_date(%(date)s,'MM-YYYY') AND to_date(%(date)s,'MM-YYYY') + interval '1 month'
  GROUP BY name,date_trunc('month',search_date)
  ORDER BY searches DESC""",['country','month','count'],{'date':myDate.strftime('%m-%Y')})

  myScores = []
  for myRec in myCountryStats:
    myScores.append({'country' : myRec['country'],'count' : myRec['count']})

  return ({
    'myGraphLabel': ({'Country':'country'}),
    'myScores': myScores,
    'myCurrentDate': myDate,
    'myPrevDate':myDate - datetime.timedelta(days=1),
    'myNextDate':myDate + datetime.timedelta(days=31),
    })

#monthly search report by user ip_position
@staff_member_required
@renderWithContext('searchMonthlyReportAOI.html')
def searchMonthlyReportAOI( theRequest, theyear, themonth):
  #construct date object
  if not(theyear and themonth):
    myDate=datetime.date.today()
  else:
    try:
      myDate=datetime.date(int(theyear),int(themonth),1)
    except:
      logging.error("Date arguments cannot be parsed")
      logging.info(traceback.format_exc())

  myQuerySet = Search()
  myCountryStats = myQuerySet.customSQL("""
  SELECT a.name, date_trunc('month',b.search_date) as date_of_search, count(*) as searches
  FROM catalogue_worldborders a INNER JOIN catalogue_search b ON st_intersects(a.geometry,b.geometry)
  WHERE search_date between to_date(%(date)s,'MM-YYYY') AND to_date(%(date)s,'MM-YYYY') + interval '1 month'
  GROUP BY  a.name,date_trunc('month',b.search_date)
  ORDER BY searches desc;""",['country','month','count'],{'date':myDate.strftime('%m-%Y')})

  myScores = []
  for myRec in myCountryStats:
    myScores.append({'country' : myRec['country'],'count' : myRec['count']})

  return ({
    'myGraphLabel': ({'Country':'country'}),
    'myScores': myScores,
    'myCurrentDate': myDate,
    'myPrevDate':myDate - datetime.timedelta(days=1),
    'myNextDate':myDate + datetime.timedelta(days=31),
    })

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('dataSummaryTable.html')
def dataSummaryTable(theRequest):
  """
  Summary of available records
  """
  #myResultSet = GenericProduct.objects.values("mission_sensor").annotate(Count("id")).order_by().aggregate(Min('product_acquisition_start'),Max('product_acquisition_end'))
  #ABP: changed to GenericSensorProduct
  #ABP: changed to MissionSensor
  myResultSet = MissionSensor.objects.annotate(id__count=Count('sensortype__acquisitionmode__genericsensorproduct')).order_by('name')
    #[{'mission_sensor': 6, 'id__count': 288307}, {'mission_sensor': 9, 'id__count': 289028}, {'mission_sensor': 3, 'id__count': 120943}, {'mission_sensor': 7, 'id__count': 222429}, {'mission_sensor': 5, 'id__count': 16624}, {'mission_sensor': 1, 'id__count': 3162}, {'mission_sensor': 2, 'id__count': 20896}, {'mission_sensor': 4, 'id__count': 17143}, {'mission_sensor': 8, 'id__count': 186269}]
  myTotal = 0
  for myResult in myResultSet:
    myTotal += myResult.id__count
  return ({"myResultSet": myResultSet, "myTotal" : myTotal})

@staff_member_required
#renderWithContext is explained in renderWith.py
@renderWithContext('sensorSummaryTable.html')
def sensorSummaryTable(theRequest, theSensorId):
  """
  Summary of tasking requests,orders etc for a given sensor
  """
  #
  # Note: don't use len() to count recs - its very inefficient
  #       use count() rather
  #
  mySensor = get_object_or_404(MissionSensor,id=theSensorId)
  myTaskingSensorCount = TaskingRequest.objects.filter(mission_sensor=mySensor).count()
  myTaskingTotalCount = TaskingRequest.objects.count()
  mySearchCount = Search.objects.all().count()
  mySearchForSensorCount = Search.objects.filter(sensors=mySensor).count()
  myProductForSensorCount = None
  if ( mySensor.is_radar ):
    myProductForSensorCount = RadarProduct.objects.filter(acquisition_mode__sensor_type__mission_sensor=mySensor).count()
  else:
    myProductForSensorCount = OpticalProduct.objects.filter(acquisition_mode__sensor_type__mission_sensor=mySensor).count()
  myProductTotalCount = GenericSensorProduct.objects.count()

  myRecords = SearchRecord.objects.filter(user__isnull=False).filter(order__isnull=False)
  myProductOrdersTotalCount = myRecords.count()
  myProductOrdersForSensorCount = 0
  for myRecord in myRecords:
    try:
      myProduct = myRecord.product
      if (myProduct.genericimageryproduct.genericsensorproduct.acquisition_mode.sensor_type.mission_sensor == mySensor):
        myProductOrdersForSensorCount += 1
    except:
      pass

  myResults = {}
  myResults["Tasking requests for this sensor"] = myTaskingSensorCount 
  myResults["Tasking requests all sensors"] = myTaskingTotalCount 
  myResults["Searches for this sensor"] = mySearchForSensorCount 
  myResults["Searches for all sensors"] = mySearchCount 
  myResults["Total ordered products for this sensor"] = myProductOrdersForSensorCount 
  myResults["Total ordered products for all sensors"] = myProductOrdersTotalCount 
  myResults["Total products for this sensor"] = myProductForSensorCount 
  myResults["Total products for all sensors"] = myProductTotalCount 
  return ({ "myResults": myResults, "mySensor" : mySensor})

