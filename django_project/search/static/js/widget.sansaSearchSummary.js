+function () {

    "use strict"; // jshint ;_;

    APP.SearchSummary = function (div, options) {
        this.options = options || {};
        this.div = $(div);
        this.data = [
            { 'id': 'ssd1', 'label': 'Satellites', 'data': {}},
            { 'id': 'ssd2', 'label': 'Date Ranges', 'data': {}},
            { 'id': 'ssd3', 'label': 'Search Area', 'data': {}},
            { 'id': 'ssd4', 'label': 'Cloud Cover', 'data': {}},
            { 'id': 'ssd5', 'label': 'Other options', 'data': {}}
        ];
        this.template = [
            '<table>',
            // iterate each  row
            '<% _.each(context, function(row) { %>',
                // if there is any data it means there is something to show
                '<% if (_.keys(row.data).length > 0) { %>',
                    // display row name
                    '<tr><td><%= row.label %></td><td>',
                    // display each option in new row
                    '<% _.each(row.data, function(text) { %>',
                        '<%= text %><br />',
                    '<% }); %>',
                    '</td></tr>',
                '<% } %>',
            '<% }); %>',
            '</table>'
        ].join('');
        this._initialize();
    };

    APP.SearchSummary.prototype = {

        _initialize: function() {
            // listening on listTree plugin to fire change event
            $(document).on("listTreeChange", $.proxy(this._handleListTree, this));
            // listening on sansaDateRange plugin to fire change event
            $(document).on("sansaDateRangeChanged", $.proxy(this._handleDateRange, this));
        },

        _handleListTree: function() {

            var text = '';
            // iterate through each sattelite group
            _.each($('.listTree').data('listTree').selected, function(data) {
                // add bolded satellite groupe name for output
                text = text + '<b>' + data.key + ': </b>';
                _.each(data.values, function(item) {
                    // add each satellite name
                    text = text + ' ' + item.key + ',';
                });
                // remove last comma
                text = text.slice(0, - 1);
                text = text + '<br />';
            });
            //remove last br
            text = text.slice(0, - 7);

            // remove existing
            if (typeof this.data[0].data.listTree != undefined) delete this.data[0].data.listTree;

            // save data
            if (text != '') this.data[0].data.listTree = text;

            // request render of specific element
            this._render();
        },

        _handleDateRange: function(e) {
            var text = '';
            // parse payload from event as json and iterate
            _.each(JSON.parse(e.dates), function(daterange) {
                text = text + daterange.from + ' - ' + daterange.to + ', ';
            });
            // remove last comma
            text = text.slice(0, - 2);

            // remove existing
            if (typeof this.data[1].data.dateRange != undefined) delete this.data[1].data.dateRange;

            // save data
            if (text != '') this.data[1].data.dateRange = text;

            // request render of specific element
            this._render();
        },

        _render: function() {
            this.div.html( _.template( this.template, { "context": this.data } ) );
        }
    };

}(); // anonfunc

