+function () {

  "use strict"; // jshint ;_;

  APP.SearchLayer = function (map_object, options) {
      this.options = options || {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.SearchLayer.prototype = {

    _initialize: function() {
      var defaultStyle = new OpenLayers.Style(
        {'fillOpacity': 0, 'strokeColor' : '${getColor}'},
        {
          context :
            {
              getColor : function (f)
                {
                    return f.attributes.strokeColor;
                }
            }
        }
      );

      var selectStyle = new OpenLayers.Style({'strokeColor': '#0000FF', 'fillOpacity': 0});1

      var style = new OpenLayers.StyleMap({'default': defaultStyle, 'select': selectStyle});

      this.layerSearch = new OpenLayers.Layer.Vector("Search geometry", { styleMap: style } );
      this.map_object.add_layer(this.layerSearch);

      var myHighlightControl = new OpenLayers.Control.SelectFeature(
      this.layerSearch , {
        hover: false,
        highlightOnly: true,
        renderIntent: "temporary",
        eventListeners: {
            beforefeaturehighlighted: null,
            featurehighlighted: $.proxy(this.featureSelected,this),
            featureunhighlighted: null
        }
      }
    );
    this.map_object.map.addControl(myHighlightControl);
    myHighlightControl.activate();
    this.layerSearch.selectFeatureControl = myHighlightControl;

    var self=this;
    $APP.on('ResultGridView_fetchresults', function (evt) {
      self.layerSearch.removeFeatures(self.layerSearch.features);
    });

    $APP.on('resetZoom', function (evt) {
      self.map_object.map.zoomToExtent(self.layerSearch.getDataExtent());
      $('#resetZoom').hide();
    });

    $APP.on('SearchLayer_addFeatures', function(evt, payload){
      self.layerSearch.removeAllFeatures();
      _.each(payload.data, function (feature) {
        var feat = new OpenLayers.Feature.Vector(
          self.map_object.transformGeometry(OpenLayers.Geometry.fromWKT(feature.attributes.spatial_coverage)),
          feature.attributes
        );
        // check if item is in cart
        var exist = APP.Cart.filter(function(item) {
          return item.get("product").id == feature.attributes.id;
        });

        //if item is in cart, color green else orange
        if (exist.length > 0) {
          feat.attributes.strokeColor = '#00FF00';
        } else {
          feat.attributes.strokeColor = '#FFA500';
        }
        self.layerSearch.addFeatures([feat]);
      });
      // zoom to features extent
      self.map_object.map.zoomToExtent(self.layerSearch.getDataExtent());
    });

    $APP.on('highlightSearchRecord', function (evt, data) {
      self.highlightRecord(data.unique_product_id, true);
    });

    $APP.on('colorCartFeature', function (evt, data) {
      self.colorCartFeature(data.unique_product_id);
    });
  },

  featureSelected: function(theEvent) {
    APP.blockResultPanel();
    var id = theEvent.feature.attributes.unique_product_id;
    $APP.trigger('highlightResultItem', {'id': id});
    this.highlightRecord(id, false);
    APP.unblockResultPanel();
  },

  highlightRecord: function( theRecordId, theZoomFlag ) {
    var myIndex = this.getFeatureIndexByRecordId( theRecordId );
    this.layerSearch.features[myIndex].attributes.zIndex=1;
    this.layerSearch.features[myIndex].selected = "yes";
    if (theZoomFlag)
    {
      this.map_object.map.zoomToExtent(this.layerSearch.features[myIndex].geometry.bounds);
    }
    this.layerSearch.redraw();
    this.resetSceneZIndices();
  },

  colorCartFeature: function( theRecordId ) {
    var myIndex = this.getFeatureIndexByRecordId( theRecordId );
    this.layerSearch.features[myIndex].attributes.strokeColor = '#00FF00';
    this.layerSearch.redraw();
  },

  getFeatureIndexByRecordId: function( theRecordId ) {
    var myFeatures = this.layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      if(myFeatures[i].attributes.unique_product_id == theRecordId)
      {
        return i;
      }
    }
  },

  getFeatureElementRecordId: function( theRecordId ) {
    var myFeatures = this.layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i)
    {
      if(myFeatures[i].attributes.unique_product_id == theRecordId)
      {
        return myFeatures[i];
      }
    }
  },

  resetSceneZIndices: function() {
    var myFeatures = this.layerSearch.features;
    for(var i=0; i < myFeatures.length; ++i) {
        myFeatures[i].attributes.zIndex=0;
        myFeatures[i].selected = "no";
    }
}

}; // prototype

}(); // anonfunc