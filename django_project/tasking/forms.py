"""
SANSA-EO Catalogue - Catalogue forms

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import logging
logger = logging.getLogger(__name__)

from django import forms


from catalogue.datetimewidget import DateTimeWidget

from orders.models import DeliveryDetail
from dictionaries.models import SatelliteInstrumentGroup
from .models import TaskingRequest

# Support dmy formats (see
#    http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
    '%d-%m-%Y',               # '25-10-2005'
    '%d/%m/%Y', '%d/%m/%y',   # '25/10/2006', '25/12/06'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
)


class TaskingRequestDeliveryDetailForm(forms.ModelForm):
    ref_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    geometry = forms.CharField(widget=forms.HiddenInput(), required=False)
    geometry_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'file'}),
        required=False,
        help_text=(
            'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If '
            'the shapefile contains more than one polygon, only the first will'
            ' be used.'))

    def __init__(self, *args, **kwargs):
        super(TaskingRequestDeliveryDetailForm, self).__init__(*args, **kwargs)

    class Meta:
        model = DeliveryDetail
        exclude = ('user', 'processing_level', 'datum', 'file_format')


class TaskingRequestForm(forms.ModelForm):
    target_date = forms.DateField(
        widget=DateTimeWidget, required=True, input_formats=DATE_FORMATS,
        error_messages={
            'required': (
                'Entering a target date for your tasking request is '
                'required.')},
        help_text='Tasking target date is required. DD-MM-YYYY.')

    class Meta:
        model = TaskingRequest
        exclude = ('user', 'delivery_detail', 'order_status')

    class Media:
        js = ("/media/js/widget.sansa-datepicker.js",)

    def __init__(self, *args, **kwargs):
        super(TaskingRequestForm, self).__init__(*args, **kwargs)
        self.fields['satellite_instrument_group'].queryset = (
            SatelliteInstrumentGroup.objects.filter(
                instrument_type__is_taskable=True)
        )
