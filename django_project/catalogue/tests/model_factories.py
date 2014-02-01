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
    Order, OrderStatus, DeliveryMethod, DeliveryDetail,
    Datum, ResamplingMethod, FileFormat, MarketSector, GenericProduct,
    CreatingSoftware, GenericImageryProduct,
    GenericSensorProduct, OpticalProduct, RadarProduct, GeospatialProduct,
    PlaceType, Place, OrdinalProduct, ContinuousProduct, Unit, Visit,
    OrderStatusHistory, OrderNotificationRecipients, TaskingRequest,
    WorldBorders
)


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
    projection = factory.SubFactory(
        'dictionaries.tests.model_factories.ProjectionF')
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


class TaskingRequestF(OrderF):
    """
    TaskingRequest model factory
    """
    FACTORY_FOR = TaskingRequest

    target_date = datetime(2008, 1, 1)
    satellite_instrument_group = factory.SubFactory(
        'dictionaries.tests.model_factories.SatelliteInstrumentGroupF')


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
    spatial_coverage = (
        'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 '
        '-34.65, 17.54 -32.05))')
    projection = factory.SubFactory(
        'dictionaries.tests.model_factories.ProjectionF')
    quality = factory.SubFactory('dictionaries.tests.model_factories.QualityF')
    unique_product_id = factory.Sequence(
        lambda n: "unique_product_id_{}".format(n))
    original_product_id = factory.Sequence(
        lambda n: "Original_product_id_{}".format(n))
    local_storage_path = ''
    metadata = ''
    remote_thumbnail_url = ''
    ingestion_log = ''


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


class OpticalProductF(GenericSensorProductF):
    """
    OpticalProduct model factory
    """
    FACTORY_FOR = OpticalProduct

    product_profile = factory.SubFactory(
        'dictionaries.tests.model_factories.OpticalProductProfileF')
    cloud_cover = 0
    sensor_inclination_angle = 0.0
    sensor_viewing_angle = 0.0
    gain_name = ''
    gain_value_per_channel = ''
    gain_change_per_channel = ''
    bias_per_channel = ''
    solar_zenith_angle = 0.0
    solar_azimuth_angle = 0.0
    earth_sun_distance = 0.0


class RadarProductF(GenericSensorProductF):
    """
    RadarProduct model factory
    """
    FACTORY_FOR = RadarProduct

    product_profile = factory.SubFactory(
        'dictionaries.tests.model_factories.RadarProductProfileF'
    )
    imaging_mode = ''
    look_direction = factory.Iterator(
        RadarProduct.LOOK_DIRECTION_CHOICES, getter=lambda c: c[0])
    antenna_receive_configuration = factory.Iterator(
        RadarProduct.RECEIVE_CONFIGURATION_CHOICES, getter=lambda c: c[0])
    polarising_mode = factory.Iterator(
        RadarProduct.POLARISING_MODE_CHOICES, getter=lambda c: c[0])
    polarising_list = ''
    slant_range_resolution = 0.0
    azimuth_range_resolution = 0.0
    orbit_direction = factory.Iterator(
        RadarProduct.ORBIT_DIRECTION_CHOICES, getter=lambda c: c[0])
    calibration = ''
    incidence_angle = 0.0


class PlaceTypeF(factory.django.DjangoModelFactory):
    """
    PlaceType model factory
    """
    FACTORY_FOR = PlaceType

    name = factory.Sequence(lambda n: "PlaceType {}".format(n))


class PlaceF(factory.django.DjangoModelFactory):
    """
    Place model factory
    """
    FACTORY_FOR = Place

    name = factory.Sequence(lambda n: "Place {}".format(n))
    place_type = factory.SubFactory(PlaceTypeF)
    geometry = 'POINT(17.54 -32.05)'


class GeospatialProductF(GenericProductF):
    """
    GeospatialProduct model factory
    """
    FACTORY_FOR = GeospatialProduct

    name = factory.Sequence(lambda n: "GeospatialProduct {}".format(n))
    description = ''
    processing_notes = ''
    equivalent_scale = 1000000
    data_type = factory.Iterator(
        GeospatialProduct.GEOSPATIAL_GEOMETRY_TYPE_CHOICES,
        getter=lambda c: c[0])
    temporal_extent_start = datetime(2008, 1, 1, 12, 00)
    temporal_extent_end = datetime(2008, 1, 1, 13, 00)
    place_type = factory.SubFactory(PlaceTypeF)
    place = factory.SubFactory(PlaceF)
    primary_topic = factory.SubFactory(
        'dictionaries.tests.model_factories.TopicF')


class OrdinalProductF(GenericProductF):
    """
    OrdinalProduct model factory
    """
    FACTORY_FOR = OrdinalProduct

    class_count = 0
    confusion_matrix = '1,2,3'
    kappa_score = 0.0


class UnitF(factory.django.DjangoModelFactory):
    """
    Unit model factory
    """
    FACTORY_FOR = Unit

    abbreviation = factory.Sequence(lambda n: "U{}".format(n))
    name = factory.Sequence(lambda n: "Unit {}".format(n))


class ContinuousProductF(GenericProductF):
    """
    ContinuousProduct model factory
    """
    FACTORY_FOR = ContinuousProduct

    range_min = 0.0
    range_max = 0.0
    unit = factory.SubFactory(UnitF)


class VisitF(factory.django.DjangoModelFactory):
    """
    Visit model factory
    """
    FACTORY_FOR = Visit

    city = ''
    country = ''
    ip_address = '0.0.0.0'
    ip_position = 'POINT(0.0 0.0)'
    user = factory.SubFactory('core.model_factories.UserF')


class OrderStatusHistoryF(factory.django.DjangoModelFactory):
    """
    OrderStatusHistory model factory
    """
    FACTORY_FOR = OrderStatusHistory

    user = factory.SubFactory('core.model_factories.UserF')
    order = factory.SubFactory(OrderF)
    notes = ''
    old_order_status = factory.SubFactory(OrderStatusF)
    new_order_status = factory.SubFactory(OrderStatusF)


class OrderNotificationRecipientsF(factory.django.DjangoModelFactory):
    """
    OrderNotificationRecipients model factory
    """
    FACTORY_FOR = OrderNotificationRecipients

    user = factory.SubFactory('core.model_factories.UserF')

    @factory.post_generation
    def add_satellite_instrument_groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for sat_inst_group in extracted:
                self.satellite_instrument_group.add(sat_inst_group)

    @factory.post_generation
    def add_classes(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for klass in extracted:
                self.classes.add(klass)


class WorldBordersF(factory.django.DjangoModelFactory):
    """
    OrderNotificationRecipients model factory
    """
    FACTORY_FOR = WorldBorders

    iso2 = 'ZA'
    iso3 = 'ZAF'
    name = 'South Africa'
    geometry = 'MULTIPOLYGON(((-180 90, 180 90, 180 -90, -180 -90, -180 90)))'
