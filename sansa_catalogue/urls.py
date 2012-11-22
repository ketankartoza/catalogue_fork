#from django.conf.urls.defaults import *
from django.conf.urls import patterns, include, url
#from django.views.generic import list_detail
from catalogue.views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


# These dictionaries are used for our generic views
# see http://docs.djangoproject.com/en/dev/intro/tutorial04/
#myOrdersDict = { 'queryset': Order.objects.all(),
   #  "template_object_name" : "myOrders",
#    }


# Here are our patterns
urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Usually you would do this using apache but since
    # I have deployed the app to the root of the server
    # we need to do it here
    url(r'^admin_media/(.*)$','django.views.static.serve',
      {'document_root': "/usr/share/python-support/python-django/django/contrib/admin/media/"
        , 'show_indexes': True}),
    #(r'^sentry/', include('sentry.web.urls')),
    url(r'^media/(.*)$','django.views.static.serve',
      {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'^thumbnails/(.*)$','django.views.static.serve',
      {'document_root': settings.THUMBS_ROOT, 'show_indexes': False}),
    url(r'^$', index),
    url(r'^video/$', video, name='video'),
    url(r'^about/$', about, name='about'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^deletesearch/(?P<theId>[0-9]+)/$', deleteSearch, name='deleteSearch'),
    url(r'^kml/$', visitorsKml, name='visitorsKml'),
    url(r'^mapHelp/$', mapHelp, name='mapHelp'),
    url(r'^emptyCartHelp/$', emptyCartHelp, name='emptyCartHelp'),
    url(r'^sceneidhelp/$', sceneIdHelp),
    url(r'^modifysearch/(?P<theGuid>[a-h0-9\-]{36})/$', modifySearch, name='modifySearch'),
    # match a product id - its not needed to give teh full id, just enough to be semi unique
    url(r'^showProduct/(?P<theProductId>[A-Za-z0-9\_\-]{38,58})/$', showProduct, name='showProduct'),
    url(r'^clip/$', clip),
    # is this used?
    url(r'^myclips/$', clipHistory),
    url(r'^mysearches/$', searchHistory, name='searchHistory'),
    url(r'^recentsearches/$', recentSearches, name='recentSearches'),
    url(r'^searchmonthlyreport/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$', searchMonthlyReport, name='searchMonthlyReport'),
    url(r'^searchmonthlyreportaoi/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$', searchMonthlyReportAOI, name='searchMonthlyReportAOI'),
    url(r'^search/$', 'catalogue.views.search.search', name='search'), # clashes with module name catalogue.views.search
    url(r'^productIdSearch/(?P<theGuid>[a-h0-9\-]{36})/$', productIdSearch, name='productIdSearch'),
    url(r'^visit/$', logVisit, name='logVisit'),
    url(r'^visitormap/$', visitorMap, name='visitorMap'),
    url(r'^whereami/$', whereAmI, name='whereAmI'),

    #show all searches that were made
    url(r'^searchesmap/$', searchesMap, name='searchesMap'),
    url(r'^visitorlist/$', visitorList, name='visitorList'),
    url(r'^visitorreport/$', visitorReport, name='visitorReport'),
    url(r'^visitormonthlyreport/(?P<theYear>\d{4})/(?P<theMonth>\d{1,2})/$', visitorMonthlyReport, name='visitorMonthlyReport'),
    # Profile application
    url(r'^accounts/', include('userprofile.urls')),
    #show a single search map
    url(r'^searchresult/(?P<theGuid>[a-h0-9\-]{36})/$', searchResultMap, name='searchResultMap'),
    #show a single search page to insert into search result map
    url(r'^searchpage/(?P<theGuid>[a-h0-9\-]{36})/$', searchResultPage, name='searchResultPage'),
    # return the results of a search as a shapefile
    url(r'^downloadsearchresults/(?P<theGuid>[a-h0-9\-]{36})/$', downloadSearchResult, name='downloadSearchResult'),
    url(r'^downloadsearchmetadata/(?P<theGuid>[a-h0-9\-]{36})/$', downloadSearchResultMetadata, name='downloadSearchResultMetadata'),
    # show segment thumb for a segment by #
    # thumbnailpage is called only by itself?
    url(r'^thumbnailpage/(?P<theId>[0-9]+)/$', showThumbPage, name='showThumbPage'),
    url(r'^sensordictionaries/$', getSensorDictionaries, name='getSensorDictionaries'),
    # returns image mime type - show segment thumb info for a segment
    url(r'^thumbnail/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', showThumb, name='showThumb'),
    # returns html mime type
    url(r'^showpreview/(?P<theId>[0-9]+)/(?P<theSize>[a-z]+)/$', showPreview, name='showPreview'),
    #show info for a scene or segment by #
    url(r'^metadata/(?P<theId>[0-9]+)/$', metadata, name="metadata"),
    url(r'^addtocart/(?P<theId>[0-9]+)/$', addToCart, name='addToCart'),
    url(r'^removefromcart/(?P<theId>[0-9]+)/$', removeFromCart, name='removeFromCart'),
    # cart contents for embedding into other pages
    url(r'^downloadcart/$', downloadCart, name='downloadCart'),
    url(r'^downloadcartmetadata/$', downloadCartMetadata, name='downloadCartMetadata'),
    url(r'^showcartcontents/$', showCartContents, name='showCartContents'), #used by xhr requests
    url(r'^showminicartcontents/$', showMiniCartContents, name='showMiniCartContents'),
    #
    # Order management and related lookup tables
    #
    url(r'^addorder/', addOrder, name='addOrder'),
    url(r'^deliverydetailform/(?P<theReferenceId>\d*)/$', createDeliveryDetailForm, name='createDeliveryDetailForm'),
    url(r'^showdeliverydetail/(?P<theReferenceId>\d*)/$', showDeliveryDetail, name='showDeliveryDetail'),
    url(r'^downloadclipgeometry/(?P<theId>\d*)/$', downloadClipGeometry, name='downloadClipGeometry'),
    url(r'^downloadordermetadata/(?P<theId>\d*)/$', downloadOrderMetadata, name='downloadOrderMetadata'),
    url(r'^downloadorder/(?P<theId>\d*)/$', downloadOrder, name='downloadOrder'),
    url(r'^myorders/$', myOrders, name='myOrders'),
    url(r'^listorders/$', listOrders, name='listOrders'),
    url(r'^ordermonthlyreport/(?P<theyear>\d{4})/(?P<themonth>\d{1,2})/$', orderMonthlyReport, name='orderMonthlyReport'),
    url(r'^vieworder/(?P<theId>[0-9]+)/$', viewOrder, name='viewOrder'),
    url(r'^updateorderhistory/$', updateOrderHistory, name='updateOrderHistory'),
    url(r'^orderssummary/$', ordersSummary, name='ordersSummary'),
    # Tasking request managmenet
    url(r'^listtaskingrequests/$', listTaskingRequests, name='listTaskingRequests'),
    url(r'^addtaskingrequest/', addTaskingRequest, name='addTaskingRequest'),
    url(r'^mytaskingrequests/$', myTaskingRequests, name='myTaskingRequests'),
    url(r'^viewtaskingrequest/(?P<theId>[0-9]+)/$', viewTaskingRequest, name='viewTaskingRequest'),
    url(r'^taskingrequest/(?P<theId>\d*)/$', downloadTaskingRequest, name='downloadTaskingRequest'),

    # upload polygon from zipped shapefile for search/clip
    #( r'^uploadFeature/$', uploadFeature),

    url(r'^getFeatureInfo/(?P<theLon>[-]*\d+.\d+)/(?P<theLat>[-]*\d+.\d+)/(?P<theBoundingBox>[0-9\-,.]*)/(?P<thePixelX>\d+)/(?P<thePixelY>\d+)/(?P<theMapWidth>\d+)/(?P<theMapHeight>\d+)/$', getFeatureInfo),

    url( r'^dataSummaryTable/$', dataSummaryTable, name='dataSummaryTable'),
    url( r'^sensorSummaryTable/(?P<theSensorId>[0-9]+)/$', sensorSummaryTable),
    url(r'^getUserMessages/$', messaging.userMessages),
    #need to be staff to use this
    url(r'^sendMessageToUser/$', messaging.sendMessageToUser),
    #need to be staff to use this
    url(r'^sendMessageToAllUsers/$', messaging.sendMessageToAllUsers),

    # New dictionaries
    url(r'^collectionList/$', collectionList),
    url(r'^satelliteDetails/(?P<theSatelliteId>\d*)/$', satelliteDetails),


)
