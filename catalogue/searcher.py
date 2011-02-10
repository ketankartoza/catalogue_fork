from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.contrib.gis import gdal
from django.contrib.gis.geos import *
# Models and forms for our app
from catalogue.models import *
# to be deprecated...
from acscatalogue.models import *
from catalogue.weblayers import *
# for using django Q() query defs
from django.db.models import Q
from django.conf import settings
import logging


class Searcher:
  """
  This is a class that manages searches in the catalogue.
  Class members - variables declared here act like static class members in C++
  i.e. if you change them from an object, all objects will receive that change.
  """

  def clearTemplateData(self):
    """Clear the searcher data"""
    self.mMessages = []
    self.mThumbnails = []
    self.mRequest = None
    self.mSearch = None
    self.mSearchRecords = []
    self.mQuerySet = None
    self.mSearchPage = None
    self.mExtent = '(-180.0,-90.0, 180.0, 90.0)'
    self.mPageNo = 1
    self.mSqlString = ""
    self.mExtraLayers = ""
    self.mLayersList = ""
    self.mRecordCount = 0

  def templateData(self):
    """Return data from the searcher suitable for passing along
    to the map.html template"""
    return ({
        'mySearchGuid' : self.mSearch.guid,
        'myMessages' : self.mMessages,
        'myLayerDefinitions' : self.mExtraLayers,
        'myThumbnails' : self.mThumbnails,
        'myLayersList' : self.mLayersList,
        'mySensor' : self.mSearch.sensorsAsString(),
        'myRecords' : self.mSearchRecords,
        'myQuerySet' : self.mQuerySet,
        'myPage' : self.mSearchPage,
        'myExtent' : self.mExtent,
        'myPageNo' : self.mPageNo,
        'mySqlString' : self.mSqlString,
         # Possible flags for the record template
         # myShowSensorFlag
         # myShowSceneIdFlag
         # myShowDateFlag
         # myShowCartFlag
         # myRemoveFlag
         # myShowHighlightFlag
         # myThumbFlag
         # myLegendFlag
         'myDetailFlag' : True,
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
         'myPaginator' : self.mPaginator,
         'myProductIdSearch' :  self.mSearch.search_type == Search.PRODUCT_SEARCH_OPTICAL,
        })

  def __del__(self):
    logging.info('Searcher destroyed')
    return

  def initQuery(self):
    """
    Setup the querySet configuring the filters
    """
    # -----------------------------------------------------
    # First fallback extent, will be overwritten by search geom extents if
    # there is a search geom
    self.mExtent = '(-180.0,-90.0, 180.0, 90.0)'
    if self.mSearch.geometry:
      # Add the geometry of the search to the layers list for openlayers to render
      self.mExtraLayers.append('''
        var mySearchAreaLayer = new OpenLayers.Layer.Vector("Search Area");
        var myGeojsonFormat = new OpenLayers.Format.GeoJSON();
        var mySearchFeature = myGeojsonFormat.read(''' + self.mSearch.geometry.geojson + ''')[0];
        mySearchFeature.geometry = transformGeometry( mySearchFeature.geometry );
        mySearchAreaLayer.addFeatures(mySearchFeature);
        mMap.addLayer(mySearchAreaLayer);
        ''')
      # This will get overwritten by the extents of the page further down here
      # but its a good fallback in case there were no records
      self.mExtent =  str( self.mSearch.geometry.envelope.extent )
    self.mLayersList = "[zaSpot10mMosaic2008,zaRoadsBoundaries,myCartLayer]"

    # ABP: Create the query set based on the type of class we're going to search in
    assert self.mSearch.search_type in dict(Search.PRODUCT_SEARCH_TYPES).keys()

    if self.mSearch.search_type == Search.PRODUCT_SEARCH_GENERIC:
        logging.info('Search type is PRODUCT_SEARCH_GENERIC')
        self.mQuerySet = GenericProduct.objects.all()
    elif self.mSearch.search_type == Search.PRODUCT_SEARCH_OPTICAL:
        logging.info('Search type is PRODUCT_SEARCH_OPTICAL')
        self.mQuerySet = OpticalProduct.objects.all()
    elif self.mSearch.search_type == Search.PRODUCT_SEARCH_RADAR:
        logging.info('Search type is PRODUCT_SEARCH_RADAR')
        self.mQuerySet = RadarProduct.objects.all()
    elif self.mSearch.search_type == Search.PRODUCT_SEARCH_GEOSPATIAL:
        logging.info('Search type is PRODUCT_SEARCH_GEOSPATIAL')
        self.mQuerySet = GeospatialProduct.objects.all()

    # -----------------------------------------------------
    logging.info('filtering by search criteria ...')
    #
    # ABP: new logic is to get directly from the request which kind of product to search on

    # ABP: common "simple search" parameters
    if self.mSearch.start_date and self.mSearch.end_date:
      self.mDateQuery = Q(product_date__range=(self.mSearch.start_date,self.mSearch.end_date))
      self.mMessages.append('dates between <b>%s and %s</b>' % (self.mSearch.start_date, self.mSearch.end_date))
      self.mQuerySet = self.mQuerySet.filter( self.mDateQuery )

    if self.mSearch.geometry:
      self.mGeometryQuery = Q(spatial_coverage__intersects=self.mSearch.geometry)
      self.mQuerySet = self.mQuerySet.filter( self.mGeometryQuery )

    # ABP: paramters for "advanced search" only
    if self.mAdvancedFlag:
      logging.info('Search is advanced')
      # ABP: adds informations about search_type
      self.mMessages.append('search type <b>%s</b>' % dict(self.mSearch.PRODUCT_SEARCH_TYPES)[self.mSearch.search_type])
      # ABP: advanced search parameters, not sensor-specific
      if self.mSearch.license.count():
        self.mMessages.append('licenses %s' % ' ,'.join(["<b>%s</b>" % l for l in self.mSearch.license.all()]))
        # ABP: m2m
        self.mLicenseQuery = Q(license__in = self.mSearch.license.all())
        self.mQuerySet = self.mQuerySet.filter( self.mLicenseQuery )


      # ABP: sensor only (advanced  query for Radar and Optical)
      # I don't really like this kind of checks... bad OOP ...
      # this should be sooner or later heavily refactored
      if self.mSearch.search_type in (Search.PRODUCT_SEARCH_OPTICAL, Search.PRODUCT_SEARCH_RADAR):
        logging.info('GenericSensorProduct advanced search activated')
        # ABP: sensors is mandatory ? Better if not: too bad in product_id search!
        #assert self.mSearch.sensors.count() > 0, "Search contains no sensors informations"
        if self.mSearch.sensors.count() > 0:
          self.mSensorQuery = Q( mission_sensor__in=self.mSearch.sensors.all()) #__in = match to one or more sensors
          self.mQuerySet = self.mQuerySet.filter( self.mSensorQuery )
          self.mMessages.append("sensors <b>%s</b>" % self.mSearch.sensorsAsString())
          logging.info('Sensor in use is:' + str( self.mSearch.sensors.values_list( 'name',flat=True ) ) )
        if self.mSearch.acquisition_mode:
          self.mMessages.append('acquisition mode <b>%s</b>' % self.mSearch.acquisition_mode)
          self.mAcquisitionModeQuery = Q(acquisition_mode = self.mSearch.acquisition_mode)
          self.mQuerySet = self.mQuerySet.filter( self.mAcquisitionModeQuery )
        if self.mSearch.mission:
          self.mMessages.append('mission <b>%s</b>' % self.mSearch.mission)
          self.mMissionQuery = Q(mission = self.mSearch.mission)
          self.mQuerySet = self.mQuerySet.filter( self.mMissionQuery )
        if self.mSearch.sensor_type:
          self.mMessages.append('sensor type <b>%s</b>' % self.mSearch.sensor_type)
          self.mSensorTypeQuery = Q(sensor_type = self.mSearch.sensor_type)
          self.mQuerySet = self.mQuerySet.filter( self.mSensorTypeQuery )
        if self.mSearch.geometric_accuracy_mean:
          # ABP: this needs special handling to map from classes to floats
          self.mMessages.append('geometric accuracy mean between <b>%sm and %sm</b>' % Search.ACCURACY_MEAN_RANGE.get(self.mSearch.geometric_accuracy_mean))
          self.mGeometryAccuracyMeanQuery = Q(geometric_accuracy_mean__range = Search.ACCURACY_MEAN_RANGE.get(self.mSearch.geometric_accuracy_mean))
          self.mQuerySet = self.mQuerySet.filter( self.mGeometryAccuracyMeanQuery )
        if self.mSearch.spectral_resolution:
          self.mMessages.append('spectral resolution <b>%s</b>' % self.mSearch.spectral_resolution)
          self.mSpectralResolutionQuery = Q(spectral_resolution = self.mSearch.spectral_resolution)
          self.mQuerySet = self.mQuerySet.filter( self.mSpectralResolutionQuery)

        logging.info('checking if we should use landsat path / row filtering...')
        if self.mSearch.k_orbit_path_min > 0 \
            and self.mSearch.k_orbit_path_max > 0 \
            and self.mSearch.j_frame_row_min > 0 \
            and self.mSearch.j_frame_row_max > 0:
          logging.info('path row filtering is enabled')
          # used for scene searches only (landsat only)
          self.mKOrbitPathQuery = Q(path__range=[self.mSearch.k_orbit_path_min, self.mSearch.k_orbit_path_max])
          # used for scene searches only (landsat only)
          self.mJFrameRowQuery = Q(row__range=[self.mSearch.j_frame_row_min,self.mSearch.j_frame_row_max])
          self.mQuerySet = self.mQuerySet.filter( self.mKOrbitPathQuery )
          self.mQuerySet = self.mQuerySet.filter( self.mJFrameRowQuery )
          self.mMessages.append(self.rowPathAsString())
        else:
          logging.info( 'path row filtering is DISABLED' )

      # ABP: optical only
      if self.mSearch.search_type == Search.PRODUCT_SEARCH_OPTICAL:
        logging.info('OpticalProduct advanced search activated')
        if self.mSearch.use_cloud_cover:
          self.mCloudQuery = Q( cloud_cover__lte=self.mSearch.cloud_mean ) | Q( cloud_cover__isnull=True )
          self.mQuerySet = self.mQuerySet.filter( self.mCloudQuery )
          self.mMessages.append(self.meanCloudString())
        if self.mSearch.sensor_inclination_angle_start and self.mSearch.sensor_inclination_angle_end:
          assert (self.mSearch.sensor_inclination_angle_start < self.mSearch.sensor_inclination_angle_end) or not (self.mSearch.sensor_inclination_angle_start or self.mSearch.sensor_inclination_angle_end), "Search sensor_inclination_angle_start is not < sensor_inclination_angle_end"
          self.mSensorInclinationAngleQuery = Q(sensor_inclination_angle__range = (self.mSearch.sensor_inclination_angle_start, self.mSearch.sensor_inclination_angle_end))
          self.mQuerySet = self.mQuerySet.filter( self.mSensorInclinationAngleQuery )
          self.mMessages.append('sensor inclination angle between <b>%s and %s</b>' % (self.mSearch.sensor_inclination_angle_start, self.mSearch.sensor_inclination_angle_end))

      # ABP: radar only
      if self.mSearch.search_type == Search.PRODUCT_SEARCH_RADAR:
        logging.info('RadarProduct advanced search activated')

      # ABP: geospatial only
      if self.mSearch.search_type == Search.PRODUCT_SEARCH_GEOSPATIAL:
        logging.info('GeospatialProduct advanced search activated')
    else:
      logging.info('Search is simple (advanced flag is not set)')

    self.mSqlString = self.mQuerySet.query
    self.mRecordCount =  self.mQuerySet.count()


  def __init__(self, theRequest, theGuid):
    # Queries
    self.mPageNo = 1

    # items that are passed back with templateData
    self.mMessages = []
    self.mThumbnails = []
    self.mSearchRecords = []
    self.mExtent = '(-180.0,-90.0, 180.0, 90.0)'
    self.mRequest = theRequest
    self.mRecordCount = 0

    logging.info('Searcher initialised')

    # ABP: is advanced ?
    self.mSearch = get_object_or_404(Search, guid=theGuid)
    self.mAdvancedFlag = self.mSearch.isAdvanced

    # Map of all search footprints that have been added to the users cart
    # Transparent: true will make a wms layer into an overlay
    self.mCartLayer = '''myCartLayer = new OpenLayers.Layer.WMS("Cart", "http://''' + settings.WMS_SERVER + '''/cgi-bin/mapserv?map=CART&user=''' + str(theRequest.user.username) + '''",
          {
             version: '1.1.1',
             width: '800',
             layers: 'Cart',
             srs: 'EPSG:4326',
             height: '525',
             format: 'image/png',
             transparent: 'true'
           },
           {isBaseLayer: false});
           '''
    self.mSqlString = ""
    self.mExtraLayers = ""
    self.mLayersList = ""
    self.initQuery()


  def logResults (self):
    logging.info('New results: ')
    for myResult in self.mSearchRecords:
      logging.info('Result product: ' + str(myResult.product.product_id) )
    return

  def search(self, thePaginateFlag=True):
    """Performs a search and shows a map of a single search for scenes"""
    logging.info('search called...')
    logging.info('Searching by scene')
    self.mExtraLayers = [ WEB_LAYERS['ZaSpot10mMosaic2008'],WEB_LAYERS['ZaRoadsBoundaries'],self.mCartLayer ]
    self.mLayersList = "[zaSpot10mMosaic2008,zaRoadsBoundaries,myCartLayer]"
    self.mSearchRecords = []
    self.mSearchPage = None
    self.mThumbnails = []
    self.mPaginator = None



    logging.info('search by Scene paginating...')
    # Can also write the query like this:
    # mQuerySet = Localization.objects.filter(sensor=mSearch.sensor).filter(timeStamp__range=(mSearch.start_date,mSearch.end_date)).filter(geometry__intersects=mSearch.geometry)
    #

    if thePaginateFlag:
      # only use this next line for serious debugging - its a performance killer
      #logging.info('search by scene pre-paginator count...' + str(self.mQuerySet.count()))
      # Paginate the results
      self.mPaginator = Paginator(self.mQuerySet, settings.PAGE_SIZE)
      # Make sure page request is an int. If not, deliver first page.
    else:
      self.mPaginator = Paginator(self.mQuerySet,self.mQuerySet.count())
    try:
      self.mPageNo = int(self.mRequest.GET.get('page', '1'))
    except ValueError:
      self.mPageNo = 1
    logging.info('search by scene using paginator page...' + str(self.mPageNo))
    # If page request (9999) is out of range, deliver last page of results.
    try:
      logging.info('search by scene - getting page')
      self.mSearchPage = self.mPaginator.page(self.mPageNo)
      logging.info('search by scene - search results paginated')
    except (EmptyPage, InvalidPage):
      logging.info('search by scene - paginator page requested is out of range')
      self.mSearchPage = self.mPaginator.page(self.mPaginator.num_pages)

    myUnion = None
    for myObject in self.mSearchPage.object_list:
      myRecord = SearchRecord()
      myRecord.product = myObject
      self.mSearchRecords.append( myRecord )
      if not myUnion:
        # We only union the envelopes as we are only interested in
        # the rectangular extents of all features, not their geometric union
        myUnion = myObject.spatial_coverage.envelope
      else:
        # This can be done faster using cascaded union but needs geos 3.1
        myUnion = myUnion.union( myObject.spatial_coverage.envelope )
      logging.info( "%s added to myRecords" % myObject.product_id )
    if myUnion:
      self.mExtent = str( myUnion.extent )


    # -----------------------------------------------------
    # Wrap up now ...
    # -----------------------------------------------------
    logging.info( "search : wrapping up search result presentation " )
    logging.info('extent of search results page...' + str(self.mExtent))
    self.logResults()
    return ()

  def rowPathAsString(self):
    if self.mSearch.k_orbit_path_min > 0 \
      and self.mSearch.k_orbit_path_max > 0 \
      and self.mSearch.j_frame_row_min > 0 \
      and self.mSearch.j_frame_row_max > 0:
      myString =  "Row [%s,%s], Path [%s,%s]." % ( self.mSearch.j_frame_row_min , self.mSearch.j_frame_row_max , self.mSearch.k_orbit_path_min, self.mSearch.k_orbit_path_max )
      return myString
    else:
      return ""

  def meanCloudString(self):
    myCloudAsPercent = None
    if self.mSearch.cloud_mean:
      myCloudAsPercent = int( self.mSearch.cloud_mean )  * 10
    else:
      myCloudAsPercent = 0
    # %% is to escape the percent symbol so we get a % literal
    myString =  "with a maximum cloud cover of %s%%" % myCloudAsPercent
    return myString

  def describeQuery(self):
    """
    Returns a struct with messages and SQL of mSearch query
    """
    # Get option for all related fields, exclude users
    values = {}
    for field_name in [f.name for f in self.mSearch._meta.fields if f.rel]:
      if field_name != 'user' and not getattr(self.mSearch, field_name , None):
        values[field_name] = self.getOption(field_name)
    # m2m
    if not getattr(self.mSearch, 'sensors').count():
        values['sensors'] = self.getOption('mission_sensor')
    if not getattr(self.mSearch, 'license').count():
        values['license'] = self.getOption('license')

    return { 'messages' : self.mMessages, 'query' : "%s" % self.mSqlString, 'count' : self.mRecordCount, 'values' : values }

  def getOption(self, field_name):
    """
    Returns a list of possible values that selected search parameters can assume for a given field
    """
    return list(self.mQuerySet.distinct().values_list(field_name, flat = True).order_by())


