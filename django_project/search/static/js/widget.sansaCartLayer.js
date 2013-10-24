+function () {

  "use strict"; // jshint ;_;

  APP.CartLayer = function (map_object, options) {
      this.options = options || {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.CartLayer.prototype = {

    _initialize: function() {

      this.layerCart = new OpenLayers.Layer.Vector("Cart", {'displayInLayerSwitcher': false});
      this.map_object.add_layer(this.layerCart);
      var feat = [];
      for(var index in this.options.wkt) {
        var featData = this.options.wkt[index];
        feat.push(new OpenLayers.Feature.Vector(this.map_object.transformGeometry(OpenLayers.Geometry.fromWKT(featData))));
      }
      this.layerCart.addFeatures(feat);
      this.map_object.map.zoomToExtent(this.layerCart.getDataExtent());
  }

}; // prototype

}(); // anonfunc