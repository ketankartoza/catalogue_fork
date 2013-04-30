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
from django.contrib.auth.models import User


from catalogue.models import (
    OrderStatus,
    Order,
    Projection,
    DeliveryDetail,
    TaskingRequest,
    OrderStatusHistory,
)
from catalogue.datetimewidget import DateTimeWidget
from catalogue.geometrywidget import GeometryWidget
from catalogue.aoigeometry import AOIGeometryField

from search.models import (
    SearchRecord,
    Clip,
)

from dictionaries.models import SatelliteInstrumentGroup

# Support dmy formats (see
#    http://dantallis.blogspot.com/2008/11/date-validation-in-django.html )
DATE_FORMATS = (
    '%d-%m-%Y',               # '25-10-2005'
    '%d/%m/%Y', '%d/%m/%y',   # '25/10/2006', '25/12/06'
    '%d %b %Y', '%d %b, %Y',  # '25 Oct 2006', '25 Oct, 2006'
    '%d %B %Y', '%d %B, %Y',  # '25 October 2006', '25 October, 2006'
)


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = OrderStatus


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        #exclude = ('user','order_status')
        exclude = ('user', 'order_status', 'delivery_detail')


class DeliveryDetailForm(forms.ModelForm):
    ref_id = forms.CharField(widget=forms.HiddenInput(), required=False)
    aoi_geometry = AOIGeometryField(
        required=False,
        help_text=(
            'Enter bounding box coordinates separated by comma for Upper '
            'left and Lower right coordinates i.e. (20,-32,22,-34), or '
            'enter single coordinate which defines circle center and '
            'radius in kilometers (20,-32,100). Alternatively, digitise '
            'the clip area in the map.'))
    geometry = forms.CharField(widget=forms.HiddenInput(), required=False)
    geometry_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'file'}),
        required=False,
        help_text=(
            'Upload a zipped shapefile or KML/KMZ file of less than 1MB. If '
            'the shapefile contains more than one polygon, only the first will'
            ' be used.'))

    def __init__(self, theRecords, *args, **kwargs):
        super(DeliveryDetailForm, self).__init__(*args, **kwargs)
        #determine UTM zones for all products
        myProductZones = set()
        for record in theRecords:
            myProductZones = myProductZones.union(
                record.product.getUTMZones(theBuffer=1))

        myDefaultProjections = set((
            ('4326', 'EPSG 4326'), ('900913', 'EPSG 900913')))
        myEpsgCodes = [k for k, v in myProductZones | myDefaultProjections]
        self.fields['projection'] = forms.ModelChoiceField(
            queryset=Projection.objects.filter(
                epsg_code__in=myEpsgCodes).all(),
            empty_label=None)

    class Meta:
        model = DeliveryDetail
        exclude = ('user', 'processing_level',)

    def clean(self):
        myCleanedData = self.cleaned_data
        #if AOIgeometry is defined set it as default geometry
        if myCleanedData.get('aoi_geometry'):
            self.cleaned_data['geometry'] = self.cleaned_data['aoi_geometry']

        return self.cleaned_data


class ProductDeliveryDetailForm(forms.ModelForm):
    ref_id = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(ProductDeliveryDetailForm, self).__init__(*args, **kwargs)
        myPK = kwargs.get('prefix')
        myProduct = SearchRecord.objects.filter(pk__exact=myPK).get().product
        myDefaultProjections = set((
            ('4326', 'EPSG 4326'), ('900913', 'EPSG 900913')))
        myUTMZones = myProduct.getUTMZones(theBuffer=0)
        myEpsgCodes = [k for k, v in myUTMZones | myDefaultProjections]
        self.fields['projection'] = forms.ModelChoiceField(
            queryset=Projection.objects.filter(
                epsg_code__in=myEpsgCodes).all(), empty_label=None)

    class Meta:
        model = DeliveryDetail
        exclude = ('user', 'geometry', 'processing_level')


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


class OrderStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderStatusHistory
        exclude = ('order', 'user', 'order_change_date', 'old_order_status')


class ClipForm(forms.ModelForm):
    """
    Allows the CSIR Partner user to clip one of the Extra Layers by a given
    geometry.
    """

    image = forms.ChoiceField(choices=[
        (0, 'zaSpot2mMosaic2009'),
        (1, 'zaSpot2mMosaic2008'),
        (2, 'zaSpot2mMosaic2007')])
    geometry = forms.CharField(
        widget=GeometryWidget, required=False,
        help_text=(
            'You can digitise your clip area directly, or alternatively use '
            'the file upload option below to upload the clip shapefile. You '
            'can use the help tab in the map area for more information on how '
            'to use the map. Draw an area of interest on the map to refine the'
            ' set of search results to a specific area.'))
    geometry_file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'file'}),
        required=False,
        help_text=(
            'Upload a zipped shapefile of less than 1MB. If the shapefile '
            'contains more than one polygon, only the first will be used. The '
            'computation time is related to polygon complexity. For multipart '
            'and non-polygon features the bounding box of the first feature '
            'will be used.'))

    class Meta:
        model = Clip
        exclude = ('result_url', 'owner', 'guid', 'status')


class MessageForm(forms.Form):
    """An unbound form that creates a Message submission form to a single user
    """

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['user_id'].choices = [
            ('', '----------')] + [
                (myUser.id, myUser) for myUser in User.objects.all().order_by(
                    'username')
            ]

    user_id = forms.ChoiceField(choices=(), widget=forms.Select())

    message = forms.CharField(
        label='Message:',
        # <-- specify the textarea widget!
        widget=forms.Textarea,
        required=True,
        help_text='Enter a message here',
        error_messages={
            'required': 'A message is required!'}
    )


class AllUsersMessageForm(forms.Form):
    """An unbound form that creates a Message submission form """

    message = forms.CharField(
        label='Message:',
        widget=forms.Textarea,
        # <-- specify the textarea widget!
        required=True,
        help_text='Enter a message here',
        error_messages={
            'required': 'A message is required!'}
    )
