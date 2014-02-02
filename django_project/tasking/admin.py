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

from django.contrib.gis import admin

from .models import TaskingRequest


class TaskingRequestAdmin(admin.GeoModelAdmin):
    list_filter = ['target_date']
    list_display = ('target_date', 'user')
admin.site.register(TaskingRequest, TaskingRequestAdmin)
