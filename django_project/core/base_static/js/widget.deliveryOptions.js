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
		}
	},

	// creation code for mywidget
	// can use this.options
	_create: function() {
		var options = this.options;
		var elem = this.element;
		var suffix = this.default[options.type].suffix;
		elem.attr('id', options.id + suffix);
		elem.attr('name', options.id + suffix);
		_.each(options.data, function(opt) {
			var option = new Option(opt[1], opt[0]);
			elem.append(option);
		});
		if (options.type == 'projection') {
			var requiredOption = this.default[options.type].option;
			elem.append(requiredOption);
		}

		document.write(elem.prop('outerHTML'));
		if (options.type == 'processing') {
			$('#'+options.id + suffix).on('change', function() {
				$('#'+options.id+'_cost').html(options.data[this.selectedIndex][2])
			})
		}
		APP['widget_' + options.id + suffix ] = this;
	},

	getCost: function() {
		return this.options.data[$('#'+this.options.id + '_processing').prop('selectedIndex')][2]
	},

	//called everytime when accessing element without calling function
	//$('#').dialog({'something':'something else'})
	_init: function(){

	}

	//elem.append( new Option('Geographic WGS84', 4326));

    })//end widget
})(jQuery);