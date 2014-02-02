"""
SANSA-EO Catalogue - Catalogue model factories

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
__date__ = '01/02/2014'
__copyright__ = 'South African National Space Agency'

import factory
from datetime import datetime

from orders.tests.model_factories import OrderF
from ..models import TaskingRequest


class TaskingRequestF(OrderF):
    """
    TaskingRequest model factory
    """
    FACTORY_FOR = TaskingRequest

    target_date = datetime(2008, 1, 1)
    satellite_instrument_group = factory.SubFactory(
        'dictionaries.tests.model_factories.SatelliteInstrumentGroupF')
