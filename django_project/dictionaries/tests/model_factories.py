"""
SANSA-EO Catalogue - Dictionary model factories

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

from ..models import Collection, ProcessingLevel


class CollectionF(factory.django.DjangoModelFactory):
    """
    Collection model factory
    """
    FACTORY_FOR = Collection

    name = factory.Sequence(lambda n: 'Collection {0}'.format(n))
    description = 'None'
    institution = factory.SubFactory(
        'catalogue.tests.model_factories.InstitutionF'
    )


class ProcessingLevelF(factory.django.DjangoModelFactory):
    """
    Processing level factory
    """
    FACTORY_FOR = ProcessingLevel

    abbreviation = factory.Sequence(lambda n: 'AB{0}'.format(n))
    name = factory.Sequence(lambda n: 'Processing level {0}'.format(n))
    description = factory.Sequence(
        lambda n: 'Description of processing level {0}'.format(n))
