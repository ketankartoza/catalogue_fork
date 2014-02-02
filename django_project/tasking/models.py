"""
SANSA-EO Catalogue - TaskingRequest related models

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
__date__ = '02/02/2014'
__copyright__ = 'South African National Space Agency'

from django.contrib.gis.db import models

from orders.models import Order


class TaskingRequest(Order):
    """
    A tasking request inherits from the order model and adds
    three fields: geometry, target date  and sensor. The tasking
    request is used by end users to queue up acquisition requests
    for a given sensor.
    """
    target_date = models.DateTimeField(
        verbose_name='Target Date', auto_now=False, auto_now_add=False,
        help_text=(
            'When the image should be acquired (as close as possible '
            'to this date).')
    )
    satellite_instrument_group = models.ForeignKey(
        'dictionaries.SatelliteInstrumentGroup')

    objects = models.GeoManager()

    class Meta:
        verbose_name = 'Tasking Request'
        verbose_name_plural = 'Tasking Requests'
        ordering = ['-target_date']

    def __unicode__(self):
        return str(self.id)
