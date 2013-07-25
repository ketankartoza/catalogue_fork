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
from datetime import datetime

from ..models import (
    Institution, Order, OrderStatus, DeliveryMethod, DeliveryDetail,
    Projection, Datum, ResamplingMethod, FileFormat, MarketSector,
    GenericProduct, License, Quality, CreatingSoftware, GenericImageryProduct,
    GenericSensorProduct
)


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


class LicenseF(factory.django.DjangoModelFactory):
    """
    License model factory
    """
    FACTORY_FOR = License

    name = factory.Sequence(lambda n: 'License {0}'.format(n))
    details = ''
    type = factory.Iterator(
        License.LICENSE_TYPE_CHOICES, getter=lambda c: c[0])


class OrderStatusF(factory.django.DjangoModelFactory):
    """
    OrderStatus model factory
    """
    FACTORY_FOR = OrderStatus

    name = factory.Sequence(lambda n: "Status {}".format(n))


class DeliveryMethodF(factory.django.DjangoModelFactory):
    """
    DeliveryMethod model factory
    """
    FACTORY_FOR = DeliveryMethod

    name = factory.Sequence(lambda n: "Delivery method {}".format(n))


class ProjectionF(factory.django.DjangoModelFactory):
    """
    Projection model factory
    """
    FACTORY_FOR = Projection

    name = factory.Sequence(lambda n: "Projection {}".format(n))
    epsg_code = factory.Sequence(lambda n: n)


class DatumF(factory.django.DjangoModelFactory):
    """
    Datum model factory
    """
    FACTORY_FOR = Datum

    name = factory.Sequence(lambda n: "Datum {}".format(n))


class ResamplingMethodF(factory.django.DjangoModelFactory):
    """
    ResamplingMethod model factory
    """
    FACTORY_FOR = ResamplingMethod

    name = factory.Sequence(lambda n: "Resampling method {}".format(n))


class FileFormatF(factory.django.DjangoModelFactory):
    """
    FileFormat model factory
    """
    FACTORY_FOR = FileFormat

    name = factory.Sequence(lambda n: "File format {}".format(n))


class MarketSectorF(factory.django.DjangoModelFactory):
    """
    MarketSector model factory
    """
    FACTORY_FOR = MarketSector

    name = factory.Sequence(lambda n: "Market sector {}".format(n))


class DeliveryDetailF(factory.django.DjangoModelFactory):
    """
    DeliveryDetail model factory
    """
    FACTORY_FOR = DeliveryDetail

    user = factory.SubFactory('core.model_factories.UserF')
    processing_level = factory.SubFactory(
        'dictionaries.tests.model_factories.ProcessingLevelF')
    projection = factory.SubFactory(ProjectionF)
    datum = factory.SubFactory(DatumF)
    resampling_method = factory.SubFactory(ResamplingMethodF)
    file_format = factory.SubFactory(FileFormatF)
    geometry = None


class OrderF(factory.django.DjangoModelFactory):
    """
    Order model factory
    """
    FACTORY_FOR = Order

    user = factory.SubFactory('core.model_factories.UserF')
    notes = ''
    order_status = factory.SubFactory(OrderStatusF)
    delivery_method = factory.SubFactory(DeliveryMethodF)
    delivery_detail = factory.SubFactory(DeliveryDetailF)
    market_sector = factory.SubFactory(MarketSectorF)
    order_date = None


class QualityF(factory.django.DjangoModelFactory):
    """
    Quality model factory
    """
    FACTORY_FOR = Quality

    name = factory.Sequence(lambda n: "Quality {}".format(n))


class CreatingSoftwareF(factory.django.DjangoModelFactory):
    """
    CreatingSoftware model factory
    """
    FACTORY_FOR = CreatingSoftware

    name = factory.Sequence(lambda n: "Creating software {}".format(n))
    version = ''


class GenericProductF(factory.django.DjangoModelFactory):
    """
    GenericProduct model factory
    """
    FACTORY_FOR = GenericProduct

    product_date = factory.LazyAttribute(lambda d: datetime.now())
    processing_level = factory.SubFactory(
        'dictionaries.tests.model_factories.ProcessingLevelF')
    owner = factory.SubFactory(InstitutionF)
    license = factory.SubFactory(LicenseF)
    spatial_coverage = (
        'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 '
        '-34.65, 17.54 -32.05))')
    projection = factory.SubFactory(ProjectionF)
    quality = factory.SubFactory(QualityF)
    creating_software = factory.SubFactory(CreatingSoftwareF)
    unique_product_id = factory.Sequence(
        lambda n: "unique_product_id_{}".format(n))
    original_product_id = factory.Sequence(
        lambda n: "Original_product_id_{}".format(n))
    product_revision = ''
    local_storage_path = ''
    metadata = ''
    remote_thumbnail_url = ''


class GenericImageryProductF(GenericProductF):
    """
    GenericImageryProduct model factory
    """
    FACTORY_FOR = GenericImageryProduct

    spatial_resolution = 0.0
    spatial_resolution_x = 0.0
    spatial_resolution_y = 0.0
    radiometric_resolution = 0.0
    band_count = 0


class GenericSensorProductF(GenericImageryProductF):
    """
    GenericSensorProduct model factory
    """
    FACTORY_FOR = GenericSensorProduct

    product_acquisition_start = datetime(2008, 1, 1, 12, 00)
    product_acquisition_end = datetime(2008, 1, 1, 13, 00)
    geometric_accuracy_mean = 5.0
    geometric_accuracy_1sigma = 2.0
    geometric_accuracy_2sigma = 3.0
    radiometric_signal_to_noise_ratio = 0.0
    radiometric_percentage_error = 0.0
    spectral_accuracy = 20.0
    orbit_number = 1
    path = 123
    path_offset = 0
    row = 321
    row_offset = 0
    offline_storage_medium_id = ''
    online_storage_medium_id = ''
