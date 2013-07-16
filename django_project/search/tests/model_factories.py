import factory

from core.model_factories import UserF

from ..models import Search, SearchDateRange


class SearchF(factory.django.DjangoModelFactory):
    """
    Search model factory
    """
    FACTORY_FOR = Search

    user = factory.SubFactory(UserF)
    geometry = (
        'POLYGON ((17.54 -32.05, 20.83 -32.41, 20.30 -35.17, 17.84 '
        '-34.65, 17.54 -32.05))')
    ip_position = None
    search_date = '2010-07-15 09:21:38'
    guid = '69d814b7-TEST-42b9-9530-50ae77806da9'
    record_count = None
    deleted = False

    k_orbit_path = None
    j_frame_row = None
    use_cloud_cover = False
    cloud_mean = 5
    band_count = None
    spatial_resolution = None
    sensor_inclination_angle_start = None
    sensor_inclination_angle_end = None

    @factory.post_generation
    def instrument_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for instrument_type in extracted:
                self.instrumenttype.add(instrument_type)

    @factory.post_generation
    def satellites(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for satellite in extracted:
                self.satellite.add(satellite)

    @factory.post_generation
    def license_types(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for license_type in extracted:
                self.license_type.add(license_type)

    @factory.post_generation
    def spectral_groups(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for spectral_group in extracted:
                self.spectral_group.add(spectral_group)

    @factory.post_generation
    def processing_levels(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for processing_level in extracted:
                self.processing_level.add(processing_level)

    @factory.post_generation
    def collections(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for collection in extracted:
                self.collection.add(collection)


class SearchDateRangeF(factory.django.DjangoModelFactory):
    """
    SearchDateRange model factory
    """
    FACTORY_FOR = SearchDateRange

    search = factory.SubFactory(SearchF)
    start_date = '2010-07-15'
    end_date = '2012-07-15'
