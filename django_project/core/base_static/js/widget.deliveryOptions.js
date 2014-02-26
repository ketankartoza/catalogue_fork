/*
 * deliveryOptions widget - enables users dynamically set product
 * options
 * @author: Igor Crnković <icrni@candela-it.com>
 *
 */

(function($) {
    $.widget("sansa.deliveryOptions",{
	// default options
	options: {
		id: 0,
		data: {},
		type: ''
	},

	default: {
		'projection': {
			'suffix': '_projection',
			'option': new Option('Geographic WGS84', 4326)
		},
		'processing': {
			'suffix': '_processing',
			'option': new Option('Level 0 Raw instrument data', 14)
		}
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
		var elem = this.element;
		var suffix = this.default[this.options.type].suffix;
		var requiredOption = this.default[this.options.type].option;
		elem.attr('id',this.options.id + suffix);
		elem.attr('name',this.options.id + suffix);
		_.each(this.options.data, function(opt) {
			var option = new Option(opt[1], opt[0]);
			elem.append(option);
		});
		elem.append(requiredOption);
		document.write(elem.prop('outerHTML'));
	},

	//called everytime when accessing element without calling function
	//$('#').dialog({'something':'something else'})
	_init: function(){

	}

	//elem.append( new Option('Geographic WGS84', 4326));

    })//end widget
})(jQuery);