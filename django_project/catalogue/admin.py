# coding=utf-8
"""
SANSA-EO Catalogue - Catalogue admin interface

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

from django.db import models
from django.contrib.gis import admin
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User
from offline_messages.models import OfflineMessage

from catalogue.models import (
    OrderNotificationRecipients,
    DeliveryMethod,
    TaskingRequest,
    OrderStatus,
    FileFormat,
    ResamplingMethod,
    Datum,
    Institution,
    License,
    Quality,
    CreatingSoftware,
    GenericProduct,
    OpticalProduct,
    GeospatialProduct,
    Visit,
    AllUsersMessage,
)


#
# Visitors admin
#


class VisitAdmin(admin.GeoModelAdmin):
    """Admin model for visitors."""
    search_fields = ['city', 'country', 'user__username']
    list_filter = ['city', 'country', 'user']
    list_display = ('visit_date', 'city', 'country', 'user')


class OrderStatusAdmin(admin.GeoModelAdmin):
    """Admin model for order status."""
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)


class OrderNotificationRecipientsAdminForm(forms.ModelForm):
    """Admin form for order notification recipients."""
    class Meta:
        """Meta class implementation."""
        model = OrderNotificationRecipients

    def clean(self):
        """
        Validates that at least one of the m2m has values
        """
        if (not self.cleaned_data['classes'] and
                not self.cleaned_data['satellites']):
            raise ValidationError(
                u'Classes and sensors cannot be simultaneously blank')
        return self.cleaned_data


class OrderNotificationRecipientsAdmin(admin.GeoModelAdmin):
    """Admin for order notification recipients."""
    search_fields = [
        'user_username',
        'satellite_instrument_group__satellite__name']
    list_filter = ['user', 'satellite_instrument_group']
    list_display = ('user',)

    form = OrderNotificationRecipientsAdminForm

    def render_change_form(self, request, context, *args, **kwargs):
        """This next method will filter the users list in the admin form.

        :param request:
        :param context:
        :param args:
        :param kwargs:
        So that only staff members can be chosen from the users list."""
        context['adminform'].form.fields['user'].queryset = (
            User.objects.filter(is_staff=True))
        return (
            super(OrderNotificationRecipientsAdmin, self)
            .render_change_form(request, context, args, kwargs))

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filters abstract product classes
        :param db_field:
        :param request:
        :param kwargs:
        """
        if db_field.name == 'classes':
            form_field = (
                super(OrderNotificationRecipientsAdmin, self)
                .formfield_for_manytomany(db_field, request, **kwargs))
            form_field.choices = [
                c for c in form_field.choices
                if getattr(
                    ContentType.objects.get(
                        pk=c[0]).model_class(), 'concrete', False)]
            return form_field
        return (
            super(OrderNotificationRecipientsAdmin, self)
            .formfield_for_manytomany(db_field, request, **kwargs))

#################################################
# Admin models for new generic product model
#################################################


class DatumAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
    pass


class InstitutionAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
    pass


class LicenseAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
    pass


class QualityAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
    pass


class CreatingSoftwareAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)


class GenericProductAdmin(admin.GeoModelAdmin):
    search_fields = ['original_product_id', 'unique_product_id']
    list_filter = ['product_date', ]
    list_display = ('original_product_id', 'unique_product_id')


class GeospatialProductAdmin(admin.GeoModelAdmin):
    search_fields = ['original_product_id', 'unique_product_id']
    list_filter = ['product_date', ]
    list_display = ('original_product_id', 'unique_product_id')


class OpticalProductAdmin(admin.GeoModelAdmin):
    search_fields = ['original_product_id', 'unique_product_id']
    list_filter = ['product_date', ]
    list_display = ('original_product_id', 'unique_product_id')


class ResamplingMethodAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)


class FileFormatAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)


class DeliveryMethodAdmin(admin.GeoModelAdmin):
    search_fields = ['name']
    list_filter = ['name']
    list_display = ('name',)
    pass


class TaskingRequestAdmin(admin.GeoModelAdmin):
    list_filter = ['target_date']
    list_display = ('target_date', 'user')
    pass


class OfflineMessageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in OfflineMessage._meta.fields]
    ordering = ('message',)
    exclude = ('level',)
    field_options = {
        'fields': ('message', 'user',),
    }
    formfield_overrides = {
        models.CharField: {'widget': widgets.AdminTextareaWidget},
    }
    list_filter = ('user', 'created')

    # This next method will filter the users list in the admin form
    # so that only staff members can be chosen from the users list
    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['user'].queryset = (
            User.objects.order_by('username'))
        return (
            super(OfflineMessageAdmin, self)
            .render_change_form(request, context, args, kwargs))


class AllUsersMessageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in AllUsersMessage._meta.fields]
    ordering = ('created', 'message')

admin.site.register(TaskingRequest, TaskingRequestAdmin)
admin.site.register(DeliveryMethod, DeliveryMethodAdmin)
admin.site.register(OrderStatus, OrderStatusAdmin)
admin.site.register(FileFormat, FileFormatAdmin)
admin.site.register(ResamplingMethod, ResamplingMethodAdmin)
admin.site.register(Datum, DatumAdmin)
admin.site.register(Institution, InstitutionAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(Quality, QualityAdmin)
admin.site.register(CreatingSoftware, CreatingSoftwareAdmin)
admin.site.register(GenericProduct, GenericProductAdmin)
admin.site.register(OpticalProduct, OpticalProductAdmin)
admin.site.register(GeospatialProduct, GeospatialProductAdmin)
admin.site.register(
    OrderNotificationRecipients, OrderNotificationRecipientsAdmin)

#################################################
# End of admin models for new generic product model
#################################################

admin.site.register(Visit, VisitAdmin)
admin.site.register(OfflineMessage, OfflineMessageAdmin)
admin.site.register(AllUsersMessage, AllUsersMessageAdmin)
