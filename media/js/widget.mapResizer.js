(function($) {
    $.widget("sansa.mapResizer",{
	
	// default options
	options: {
	    'map': null
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
	    var self=this;
	    
	    //calculate minimal right edge for the map
	    var elem_parent= this.element.parent();
	    this.right_edge_limit = elem_parent.offset().left + elem_parent.width();

	    //set min_width to parent width
	    this.min_width=elem_parent.width();

	    this.map=this.element.find("#map");
	    
	    //this.element.css({'position':'relative'});
	    this.element.resizable({
		minHeight: 300,
		minWidth: self.min_width,
		
		start: function (evt){
		    self.old_width=self.element.width();//store old width
		},
		resize: function (evt){
		    //called during resize
		    self.map.height(self.element.height()-38);
		    self.map.width(self.element.width());
		},
		stop: function (evt){
		    var new_width=self.element.width();
		    var offset = self.element.offset();
		    
		    var right_edge=offset.left+new_width;
		    if (right_edge < self.right_edge_limit) {
			self.element.offset({top:offset.top,left:self.right_edge_limit-self.min_width});
			self.element.width(self.min_width);
		    }
		    else {
			var left_offset = new_width-self.old_width;//mirror left side as much as right side == mirror
			var final_width=new_width+left_offset;
			
			self.element.offset({top:offset.top,left:offset.left-left_offset});
			self.element.width(new_width+left_offset);
			self.map.width(new_width+left_offset);
		    }		    
		    self._set_dim(); // resize map and recenter (mandatory for draw feature controls)			
		}
	    });
	},
	
	//called everytime when accessing element without calling function 
	//$('#').dialog({'something':'something else'})
	_init: function(){

	},

	_set_dim: function (offset){
	    var center = self.options.map.getCenter();
	    var zoom = self.options.map.getZoom();
	    this.options.map.setCenter(center,zoom);
	},

	_fullscreen_image:function(arg){
	    var self=this;
	    var img_handle = $('<div>').attr({
		'id':'map_resize'
	    });
	    img_handle.css({
		'z-index':99999,
		'width':'32px',
		'height':'32px',
		'display':'none',
		'position':'absolute',
		'bottom':'0px',
		'right':'0px',
		'background-image':'url("/media/images/sun.png")'
	    });
	    return img_handle
	}

    })//end widget
})(jQuery);

