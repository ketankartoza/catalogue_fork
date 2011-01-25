from django.conf import settings

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
        '''
        }

mLayerJs = {'VirtualEarth' : '''<script src='http://dev.virtualearth.net/mapcontrol/mapcontrol.ashx?v=6.1'></script>
         ''',
         'Google' : '''
          <script src='http://maps.google.com/maps?file=api&amp;v=2&amp;key='{{GOOGLE_MAPS_API_KEY}}'></script>
          '''}


