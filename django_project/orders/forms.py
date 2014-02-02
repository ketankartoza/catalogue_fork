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

from catalogue.aoigeometry import AOIGeometryField
from search.models import SearchRecord
from dictionaries.models import Projection

from .models import (
    OrderStatus,
    Order,
    DeliveryDetail,
    OrderStatusHistory,
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


class OrderStatusHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderStatusHistory
        exclude = ('order', 'user', 'order_change_date', 'old_order_status')
