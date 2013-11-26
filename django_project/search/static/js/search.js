var SearchPanelState = true;
var CartPanelState = false;
var ResultPanelState = false;
var ResultDownloadOptionsState = false;
var CartDownloadOptionsState = false;
var LayerSwitcherState = false;

function toggleSearchPanel() {
    if (SearchPanelState) {
        closeSearchPanel();
    } else {
        if (CartPanelState) {
            closeCartPanel();
        }
        $("#search-panel").animate({left: 10}, 300 );
        $('#search-panel-toggle').addClass('active');
        SearchPanelState = true;
    }
}

function closeSearchPanel() {
    $('#search-panel-toggle').removeClass('active');
    $("#search-panel").animate({left: -450}, 300 );
    SearchPanelState = false;
}

function toggleCartPanel() {
    if (CartPanelState) {
        closeCartPanel();
        CartPanelState = false;
    } else {
        if (SearchPanelState) {
            closeSearchPanel();
        }
        $("#cart-panel").animate({left: 10}, 300 );
        $('#cart-panel-toggle').addClass('active');
        CartPanelState = true;
    }
}

function closeCartPanel() {
    $("#cart-panel").animate({left: -490}, 300 );
    $('#cart-panel-toggle').removeClass('active');
    CartPanelState = false;
}

function toggleResultPanel() {
    if (ResultPanelState) {
        hideResultPanelButtons();
        $("#result-panel").animate({right: -491}, 300 );
        ResultPanelState = false;
    } else {
        $("#result-panel").animate({right: 10}, 300 );
        ResultPanelState = true;
        showResultPanelButtons();
    }
}

function openResultPanel() {
    if (!ResultPanelState) {
        $("#result-panel").animate({right: 10}, 300 );
        ResultPanelState = true;
        showResultPanelButtons();
    }
}

function defaultPanelState() {
    hideResultDownloadOptions();
    hideCartDownloadOptions();
    hideResultPanelButtons();
    if (SearchPanelState) {
        $("#search-panel").animate({left: 10}, 300 );
        SearchPanelState = true;
    } else if (CartPanelState) {
        $("#cart-panel").animate({left: 10}, 300 );
    }
    if (ResultPanelState) {
        $("#result-panel").animate({right: 10}, 300 );
        showResultPanelButtons();
    }
}

function hideResultPanelButtons() {
    if (ResultDownloadOptionsState) {
        toggleResultDownloadButton();
    }
    $("#result-panel-download-button").hide();
}

function hideResultDownloadOptions() {
    $(".downloadoptions").hide();
    ResultDownloadOptionsState = false;
}

function showResultDownloadOptions() {
    $(".downloadoptions").show();
    ResultDownloadOptionsState = true;
}

function hideCartDownloadOptions() {
    $('#cart-panel-btns').fadeOut('fast');
}

function showCartDownloadOptions() {
    $('#cart-panel-btns').fadeIn('fast');
}

function showResultPanelButtons() {
    $("#result-panel-download-button").show();
}

APP.blockResultPanel = function() {
    $.blockUI({
        message: '<div class="wrapperloading"><div class="loading up"></div><div class="loading down"></div></div>',
        css: {
            border: '1px solid #000',
            background: 'rgba(0, 0, 0, 0.3)',
            width: '450px',
            height:'450px'
        }
    });
};

APP.unblockResultPanel= function (){
    $.unblockUI();
};

APP.s = Snap('#svg');


function toggleResultDownloadButton() {
    if (ResultDownloadOptionsState) {
        hideResultDownloadOptions();
        $("#result-panel-download-button").animate({top: 500}, 200 );
    } else {
        $("#result-panel-download-button").animate({top: 300}, 200 );
        setTimeout(showResultDownloadOptions,210);
    }
}

function toggleCartDownloadButton() {
    if (CartDownloadOptionsState) {
        hideCartDownloadOptions();
        $('#cart-panel-download-button').html('<i class="icon-download"></i> Download Order');
        CartDownloadOptionsState = false;
    } else {
        showCartDownloadOptions();
        $('#cart-panel-download-button').html('<i class="icon-remove"></i> Hide Options');
        CartDownloadOptionsState = true;
    }
}

function toggleLayerSwitcher() {
    if (LayerSwitcherState) {
        $('#map-layerswitcher').hide();
        $('#map-layerswitcher-control').css('color','#FFFFFF');
        LayerSwitcherState = false;
    } else {
        $('#map-layerswitcher').show();
        $('#map-layerswitcher-control').css('color','green');
        LayerSwitcherState = true;
    }
}

function validate_form(){
  var form_ok = false;
  var myDateRange = $('#date_range .date_range_row');
  if (myDateRange.length === 0) {
      $('#daterange_inline').html('You have to select at least 1 date range!').addClass('form-error');
      $('#tab-2').prop('checked',true);
  } else {
    form_ok = true;
    // clear missing daterange error
    $('#daterange_inline').html('');
  }
  return form_ok;
}

function submitSearchForm() {
    $('#catalogueSearch').ajaxForm({
        type: 'POST',
        dataType: 'json',
        beforeSubmit: function(formData, jqForm, options) {
          if (validate_form()) {
            // process data if needed... before submit
            var selected_sensors = [];
            _.each($('.listTree').data('listTree').selected, function(parent) {
              _.each(parent.values, function(sensor) {
                selected_sensors.push(sensor.val);
              });
            });
            _.each(formData, function (element, index) {
              if (element.name === 'selected_sensors') {
                // update selected sensors value
                formData[index].value = selected_sensors;
              }
            });
          } else {
            // don't submit the form, there is an error in JS form validation
            return false;
          }
        },
        success: function(data){
            resetSearchFromErrors();
            APP.guid = data.guid;
            $APP.trigger('collectionSearch', {
              offset: 0
            });
            openResultPanel();
            toggleSearchPanel();
        },
        error: function(data) {
            if (data.status == '404') {
                processSearchFormErrors(data.responseText);
            } else {
                alert('Sorry! There has been an error. Please try again');
                console.log(data);
            }
        }

    });
    // submit the form
    $('#catalogueSearch').submit();

}

function processSearchFormErrors(data) {
    /* process json with errors when search submit fails
    set class error to control-group div
    add span element that holds error message afer input */
    resetSearchFromErrors();
    var errors = $.parseJSON(data);
    for (field in errors) {
        var inputDOM = $('#id_'+field);
        inputDOM.parent().parent().addClass('error');
        var helpElem = '<span class="error-block">'+ errors[field] +'</span>'
        inputDOM.parent().append(helpElem);
    }
    $('#tab-3').prop('checked',true);
}

function resetSearchFromErrors() {
    /* remove all error notifciatons on search form */
    $('.error-block').each( function() { this.remove(); })
    $('.error').each( function() { $(this).removeClass('error'); })
}

// backbone models/collections/views

APP.$modal = $('#ajax-modal');
APP.$imagemodal = null;
APP.guid = '';

APP.ResultItem = Backbone.Model.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/'
});
APP.ResultItemCollection = PaginatedCollection.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/',
    urlRoot: function() {
        return '/api/v1/searchresults/'+ APP.guid + '/';
    },
    model: APP.ResultItem,
    limit: APP.searchresults
});

APP.Results = new APP.ResultItemCollection();

APP.ResultGridView = Backbone.View.extend({
    el: $("#result-panel"),

    events: {
        'click div.searchPrev': 'previous',
        'click div.searchNext': 'next',
        'click div.resetZoom': 'resetZoom'
    },

    resetZoom: function() {
        $APP.trigger('resetZoom');
    },

    jumpToPage: function(page) {
        APP.blockResultPanel();
        this.collection.jumpToPage(page);
        return false;
    },

    previous: function() {
        APP.blockResultPanel();
        this.collection.previousPage();
        return false;
    },

    next: function() {
        APP.blockResultPanel();
        this.collection.nextPage();
        return false;
    },

    first: function() {
        this.collection.firstPage();
        return false;
    },

    last: function() {
        this.collection.lastPage();
        return false;
    },

    initialize: function() {
        this.collection.bind('reset', this.render, this);
        //this.collection.fetch({reset: true});
        this.cont = $("#results-container");
        $APP.on('collectionSearch', $.proxy(this.collectionSearch, this));
    },

    collectionSearch: function (evt, options) {
        $APP.trigger('ResultGridView_fetchresults');
        APP.blockResultPanel();
        _.extend(this.collection, options);
        this.collection.fetch({
            reset: true,
            error: function() { APP.unblockResultPanel(); }
        });
    },
    render: function() {
        if (_.size(this.collection.models) != 0) {
            $APP.trigger('SearchLayer_addFeatures', {
                'data': this.collection.models
            });

            this.cont.empty();
            var self=this;
            _(this.collection.models).each(function(item){
                self.renderItem(item);
            },this);
            this._update_pagination_info();
        }

        APP.unblockResultPanel();

        return this;
    },
    renderItem: function(item) {
        var myItem = new APP.ResultGridViewItem({
            model:item,
            collection:this.collection
        });
        var el = myItem.render().el;
        this.cont.append(el);
        // check if result item if is in cart
        var id = myItem.model.get('id');
        var exist = APP.Cart.filter(function(item) {
            return item.get("product").id == id;
        });
        // if it is, color it differently
        if (exist.length > 0) {
            $("#result_item_"+ myItem.model.get('unique_product_id')).addClass('cartResultRow');
        }
    },

    _createSelectPaginator: function(current, end) {
        var select = document.createElement("select");
        select.style.width = "50px";
        var self = this;
        select.onchange = function(event) {
            self.jumpToPage(event.explicitOriginalTarget.value);
        };
        var option;
        for (var i = 1; i < end+1; i++) {
            option = document.createElement("option");
            option.setAttribute("value", i);
            option.innerHTML = i;
            select.appendChild(option);
        }
        select.options.selectedIndex = current-1;
        return select;
    },

    _update_pagination_info:function() {
        var cur_pag_el = this.$el.find('#resultsPosition');
        var page_info = this.collection.pageInfo();
        var paginator = this._createSelectPaginator(page_info.current_page, page_info.pages);
        var text = 'Page <span id="paginator"></span> of ' + page_info.pages + ' ('+page_info.total+' records)';
        if (page_info.current_page > 1) {
            $('#searchPrev').show();
        } else {
            $('#searchPrev').hide();
        }
        if (page_info.current_page != page_info.pages) {
            $('#searchNext').show();
        } else {
            $('#searchNext').hide();
        }
        $('#SearchShare').show();
        cur_pag_el.html(text);
        $('#paginator').html(paginator);
    }
});

APP.ResultGridViewItem = Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata',
        'click span.cart-button': 'addToCart',
        'click': 'highlightResultItem',
        'click img': 'imagePopover',
        'mouseenter': 'focusItem',
        'mouseleave': 'blurItem'
    },
    initialize: function() {
        $APP.on('highlightResultItem', $.proxy(this.highlightResultItem, this));
        this.expanded = false;
    },

    imagePopover: function(event) {
        if (typeof varPopover == 'undefined') varPopover = [{'id': 0}];
        if (varPopover[0].id == $(event.currentTarget).parent()[0].id) {
            $(event.currentTarget).parent().popover('hide');
            varPopover = [{'id': 0}];
        } else {
            if (varPopover[0].id != 0) varPopover.popover('destroy');
            var src = event.currentTarget.src.replace('mini','large');
            varPopover = $(event.currentTarget).parent();
            $.loadImage(src).done(function(image) {
                var src = image.src.replace('large','raw');
                varPopover.popover({
                    content: '<img src="'+image.src+'" /><br /><a data-lightbox="'+src+'" href="' + src + '">Open large preview</a>',
                    placement: 'left',
                    container: 'body',
                    html: true
                }).popover('show');
            });
        }
        event.stopPropagation();
    },

    focusItem: function() {
        var selectedID = this.model.get('unique_product_id');
        var pos2 = $("#result_item_"+ selectedID).offset();
        var targetFeature = searchLayer.getFeatureElementRecordId(selectedID);
        var point = targetFeature.geometry.getCentroid();
        var pos = myMap.map.getPixelFromLonLat(new OpenLayers.LonLat(point.x, point.y));
        this.line = APP.s.line(pos.x, pos.y + 35, pos2.left+2, pos2.top+9);
        this.line.animate({stroke: "#228441", strokeWidth: "2"}, 500);
    },

    blurItem: function() {
        this.line.remove();
    },

    highlightResultItem: function(event, data) {
        // if id is not set presume user has clicked in result panel on item
        // if id is set presuem user has clicked record on the map
        if (typeof data == 'undefined') {
            $APP.trigger('highlightSearchRecord', {'unique_product_id': this.model.get('unique_product_id')});
            var selectedID = this.model.get('unique_product_id');
            $('#resetZoom').show();
        } else {
            var selectedID = data.id;
        }
        $("#results-container div:first-child").each(function (id, data) {
            // reset selected rows
            $(data).removeClass('focusedResultRow');
        });
        $("#result_item_"+ selectedID).addClass('focusedResultRow');
    },

    showMetadata: function(event) {
        var id = this.model.get('id');
        APP.$modal.load('/metadata/'+id, '', function(){
            APP.$modal.modal();
        });
        event.stopPropagation();
    },
    addToCart: function(event) {
        if (UserLoged) {
            var id = this.model.get('id');
            var exist = APP.Cart.filter(function(item) {
                return item.get("product").id == id;
            });
            if (exist.length > 0) {
                alert('Product already in cart!');
            } else {
                APP.Cart.create({'product': {'id':id}},{wait: true});
                $APP.trigger('colorCartFeature', {'unique_product_id': this.model.get('unique_product_id')});
                $("#result_item_"+ this.model.get('unique_product_id')).addClass('cartResultRow');
                alert('Product added to cart');
            }
        } else {
            alert('You need to log in first!');
        }
        event.stopPropagation();
    },
    render: function() {
       $(this.el).html(_.template(template, {model:this.model}));
        return this;
    },
});

var template = [
            '<div class="result-item" id="result_item_<%= model.get("unique_product_id") %>">',
            '<img class="result-img" src="/thumbnail/<%= model.get("id") %>/mini/" />',
            '<div class="result-item-info">',
              '<p><%= model.get("unique_product_id") %></p>',
            '</div>',
            '<div class="result-item-info-date">',
              '<p><%= model.get("product_date") %></p>',
            '</div>',
            '<div class="cloud-cover"><p>',
              '<% if(model.get("cloud_cover") != -1) { %><%= model.get("cloud_cover") %>%',
              '<% } else { %>UNK',
              '<% } %>',
            '</p></div>',
            '<span class="button metadata-button"><i class="icon-list-alt"></i></span>',
            '<span class="button cart-button"><i class="icon-shopping-cart"></i></span>',
          '</div>'
          ].join('');

var ResultgridViewHtml = new APP.ResultGridView({
        'collection': APP.Results});


APP.CartItem = Backbone.Model.extend({
    urlRoot: '/api/v1/searchrecords/',
    idAttribute: 'id',
    url: function () {
        var urlRoot;
        if (_.isFunction(this.urlRoot)) { urlRoot = this.urlRoot(); } else { urlRoot = this.urlRoot; }
        var id;
        if (typeof this.id === 'undefined') {
            id = '';
        } else {
            id = this.id + '/';
        }
        return urlRoot+id;
    }
});

APP.CartItemCollection = Backbone.Collection.extend({
    //urlRoot: '/api/v1/searchresults/6cfa079f-8be1-4029-a1eb-f80875a4e27c/',
    urlRoot: '/api/v1/searchrecords/',
    model: APP.CartItem,
    limit: 100
});

APP.Cart = new APP.CartItemCollection();

APP.CartGridView = Backbone.View.extend({
    el: $("#cart-container"),

    initialize: function() {
        this.collection.bind('reset', this.render, this);
        this.collection.bind('add', this.render, this);
        this.collection.bind('destroy', this.render, this);
        if (UserLoged) {
            this.collection.fetch({reset: true});
        }
    },
    render: function() {
        // house keeping
        this.$el.empty();
        var self=this;
        _(this.collection.models).each(function(item){
            self.renderItem(item);
        },this);
        $('#cart-container').perfectScrollbar('update');
        return this;
    },
    renderItem: function(item) {
        var myItem = new APP.CartGridViewItem({
            model:item,
            collection:this.collection
        });
        this.$el.append(myItem.render().el);
    }
});

APP.CartGridViewItem = Backbone.View.extend({
    tagName: 'div',
    events: {
        'click span.metadata-button': 'showMetadata',
        'click span.delete-button': 'delete'
    },

    showMetadata: function() {
        var id = this.model.get('product').id;
        APP.$modal.load('/metadata/'+id, '', function(){
            APP.$modal.modal();
        });
    },
    delete: function() {
        var del = confirm('Are you sure?');
        if (del) {
            this.model.destroy({wait: true});
        }
    },
    render: function() {
       $(this.el).html(_.template(templateCart, {model:this.model}));
        return this;
    },
});


var templateCart = [
        '<div class="cart-item">',
          '<img src="/thumbnail/<%= model.get("product").id %>/mini/" />',
          '<div class="cart-item-info">',
            '<p><%= model.get("product").unique_product_id %></p>',
          '</div>',
          //'<div class="cart-item-info-date">',
          //  '<p><%= model.get("product").product_date %></p>',
          //'</div>',
          '<div class="cart-item-buttons">',
              '<span class="btn btn-small metadata-button"><i class="icon-list-alt"></i></span>',
              '<span class="btn btn-small btn-danger delete-button"><i class="icon-trash"></i></span>',
          '</div>',
          '<div class="cart-item-cloud-cover"><p>',
            '<% if(model.get("product").cloud_cover != -1) { %><%= model.get("product").cloud_cover %>%',
              '<% } else { %>UNK',
              '<% } %>',
          '</p></div>',
        '</div>'
        ].join('');

var CartgridViewHtml = new APP.CartGridView({
        'collection': APP.Cart});

$.loadImage = function(url) {
  // Define a "worker" function that should eventually resolve or reject the deferred object.
  var loadImage = function(deferred) {
    var image = new Image();
    // Set up event handlers to know when the image has loaded
    // or fails to load due to an error or abort.
    image.onload = loaded;
    image.onerror = errored; // URL returns 404, etc
    image.onabort = errored; // IE may call this if user clicks "Stop"

    // Setting the src property begins loading the image.
    image.src = url;

    function loaded() {
      unbindEvents();
      // Calling resolve means the image loaded sucessfully and is ready to use.
      deferred.resolve(image);
    }
    function errored() {
      unbindEvents();
      // Calling reject means we failed to load the image (e.g. 404, server offline, etc).
      deferred.reject(image);
    }
    function unbindEvents() {
      // Ensures the event callbacks only get called once.
      image.onload = null;
      image.onerror = null;
      image.onabort = null;
    }
  };

  // Create the deferred object that will contain the loaded image.
  // We don't want callers to have access to the resolve() and reject() methods,
  // so convert to "read-only" by calling `promise()`.
  return $.Deferred(loadImage).promise();
};
