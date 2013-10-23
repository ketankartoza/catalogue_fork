+function () {

  "use strict"; // jshint ;_;

  APP.CartLayer = function (map_object, options) {
      this.options = options || {};
      this.map_object = map_object;
      this._initialize();
  };


  APP.CartLayer.prototype = {

    _initialize: function() {
      console.log(this.options);
      this.layerCart = new OpenLayers.Layer.WMS('Cart',
        'http://' + WMS_SERVER + '/cgi-bin/mapserv?map=CART_TEST&user='+this.options.username,
        {
           version: '1.1.1',
           layers: 'Cart',
           srs: 'EPSG:4326',
           format: 'image/png',
           transparent: 'true'
         },
         {isBaseLayer: false, singleTile:true}
        );

      this.map_object.add_layer(this.layerCart);

  }

}; // prototype

}(); // anonfunc