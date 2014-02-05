"""
SANSA-EO Catalogue - Signals for Orders

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '04/02/2014'
__copyright__ = 'South African National Space Agency'

import logging
logger = logging.getLogger(__name__)

from django.contrib.gis.db import models

from .models import Order


def snapshot_cost_and_currency(sender, instance, created, **kwargs):
    """
    Take a snapshot of cost and currency at the time of placing order
    """
    if created is True:
            pass


# set post_save signal
models.signals.post_save.connect(
    snapshot_cost_and_currency,
    sender=Order)
