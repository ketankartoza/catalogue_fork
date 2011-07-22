# -*- coding: utf-8 -*-
# widgets.py
#
# To use you have to put calendar/ (from http://www.dynarch.com/projects/calendar/)
# to your MEDIA folder and then include such links on your page:
# <!-- calendar -->
# <link rel="stylesheet" type="text/css" href="{{ MEDIA_URL }}calendar/calendar-win2k-cold-2.css" />
#<script type="text/javascript" src="{{ MEDIA_URL }}calendar/calendar.js"></script>
# <!-- this is translation file - choose your language here -->
#<script type="text/javascript" src="{{ MEDIA_URL }}calendar/lang/calendar-pl.js"></script>
#<script type="text/javascript" src="{{ MEDIA_URL }}calendar/calendar-setup.js"></script>
#<!-- /calendar -->

from django.utils.encoding import force_unicode
from django.conf import settings
from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
import datetime, time
import logging
from dateutil.relativedelta import relativedelta

# Support dmy formats (see http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
        '%d-%m-%Y',                         # '2006-10-25'
        '%d/%m/%Y', '%d/%m/%y',             # '25/10/2006', '25/12/06'
        '%d %b %Y', '%d %b, %Y',            # '25 Oct 2006', '25 Oct, 2006'
        '%d %B %Y', '%d %B, %Y',            # '25 October 2006', '25 October, 2006'
        )
# DATETIMEWIDGET

class DateTimeWidget(forms.DateInput):
    dformat = '%d-%m-%Y'
    def render(self, name, value, attrs=None):
        myDefaultDateProperty = ""
        myDefaultDate = ""
        if value is None: value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            try:
                final_attrs['value'] = \
                                   force_unicode(value.strftime(self.dformat))
            except:
                final_attrs['value'] = \
                                   force_unicode(value)
            myDefaultDate = "%s" % value.strftime(self.dformat)
            myDefaultDateProperty = ", defaultDate: '%s'" % value.strftime(self.dformat)
        if not final_attrs.has_key('id'):
            final_attrs['id'] = u'%s_id' % (name)
        id = final_attrs['id']

        #set defaults to start and end days of month if not set explicitly
        myDate = datetime.date.today()
        if "start" in name and not myDefaultDate:
          myDefaultDate = "01-%s-%s" % ( str(myDate.month), str(myDate.year))
        if "end" in name and not myDefaultDate:
          # work out the last day of the current month
          #myEndDate = datetime.date.today() + relativedelta(months=+1)
          #myEndDate = datetime.date( myFutureDate.year(), myFutureDate.month(), 1) - relativedelta(days=-1)

          # work out yesterdays date
          myEndDate = datetime.date.today() + relativedelta(days=-1)
          myDefaultDate = "%s-%s-%s" % ( myEndDate.day, myEndDate.month, myEndDate.year )


        a = u'''
        <script type="text/javascript">
          $(function() {
              $("#%s-widget").datepicker({
                minDate: new Date(1970, 1, 1),
                yearRange: "1972:+1",
                dateFormat: 'dd-m-yy',
                maxDate: '+1Y',
                changeMonth: true,
                changeYear: true,
                onSelect: function( theDate, inst)
                  {
                    check_search_dates();
                    $('#%s').val( theDate );
                  }
                %s
                });
            $("#%s-widget").datepicker("setDate", "%s");
          });
        </script>
        <div id="%s-widget"></div>
        <input type="hidden" name="%s" id="%s" value="%s" />''' % (id, id, myDefaultDateProperty, id, myDefaultDate, id, name, id, myDefaultDate)
        return mark_safe(a)


    def value_from_datadict(self, data, files, name):
        logging.info("Getting date value from data dict")
        #dtf = forms.fields.DEFAULT_DATETIME_INPUT_FORMATS
        empty_values = forms.fields.EMPTY_VALUES
        value = data.get(name, None)
        if value in empty_values:
          return None
        if isinstance(value, datetime.datetime):
          return value
        if isinstance(value, datetime.date):
          return datetime.datetime(value.year, value.month, value.day)
        #for format in dtf:
        for format in DATE_FORMATS:
          try:
            myDate = datetime.datetime(*time.strptime(value, format)[:6])
            logging.info("Parsed date is: " + str(myDate))
            return myDate
          except ValueError:
            continue
        return None


