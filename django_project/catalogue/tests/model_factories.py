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
__date__ = '16/07/2013'
__copyright__ = 'South African National Space Agency'

import factory

from ..models import Institution


class InstitutionF(factory.django.DjangoModelFactory):
    """
    Institution model factory
    """
    FACTORY_FOR = Institution

    name = factory.Sequence(lambda n: 'Institution {0}'.format(n))
    address1 = 'Blank'
    address2 = 'Blank'
    address3 = 'Blank'
    post_code = 'Blank'
