"""
SANSA-EO Catalogue - Ancillary Dictionary models

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__date__ = '01/11/2012'
__copyright__ = 'South African National Space Agency'

from model_utils.managers import PassThroughManager
from django.db.models.query import QuerySet

from django.contrib.gis.db import models

from catalogue.dbhelpers import executeRAWSQL


class OpticalProductProfileQuerySet(QuerySet):
    """
    Optical Product Profile extended query manager

    for_instrumenttypes - filters product profile by instrument types

    """

    def for_licence_type(self, theLicenceType):
        return self.filter(
            satellite_instrument__satellite_instrument_group__satellite__license_type__in=
            theLicenceType.all())

    def for_collection(self, theCollection):
        return self.filter(
            satellite_instrument__satellite_instrument_group__satellite__collection__in=
            theCollection.all()
        )

    def for_instrumenttypes(self, theInstrumentTypes):
        return self.filter(
            satellite_instrument__satellite_instrument_group__instrument_type__in=theInstrumentTypes.all())

    def for_satellite(self, theSatellite):
        return self.filter(
            satellite_instrument__satellite_instrument_group__satellite__in=theSatellite.all())

    def for_spectralgroup(self, theSpectralgroup):
        return self.filter(
            spectral_mode__spectralgroup__in=theSpectralgroup.all())


class OpticalProductProfile(models.Model):
    """
    An unique product profile for optical sensor based data.

    Consists of:
        * satellite_instrument
        * spectral_mode


    """
    satellite_instrument = models.ForeignKey('SatelliteInstrument')
    spectral_mode = models.ForeignKey('SpectralMode')

    # define model passthrough manager
    objects = PassThroughManager.for_queryset_class(
        OpticalProductProfileQuerySet)()

    def __unicode__(self):
        return u'{0} -- {1}'.format(
            self.satellite_instrument,
            self.spectral_mode
        )

    def baseProcessingLevel(self):
        """Return the InstrumentType.base_processing_level for this profile.

        Args:
            None

        Returns:
            ProcessingLevel: an instance of the ProcessingLevel model
                which represents the base processing level for the instrument
                type.

        Raises:
            None
        """

        return (
            self.satellite_instrument.satellite_instrument_group
            .instrument_type.base_processing_level
        )

    def bandCount(self):
        """Get the band count for this profile.

        Args:
            None

        Returns:
            The number of bands associated with this profile.

        Raises:
            None
        """
        return (
            self.satellite_instrument.satellite_instrument_group
            .instrument_type.band_count
        )


class RadarProductProfile(models.Model):
    """
    An unique product profile for radar sensor based data.

    Consists of:
        * satellite_instrument
        * imaging_mode


    """
    satellite_instrument = models.ForeignKey('SatelliteInstrument')
    imaging_mode = models.ForeignKey('ImagingMode')

    def __unicode__(self):
        return u'{0} -- {1}'.format(
            self.satellite_instrument,
            self.imaging_mode
        )


class ProcessingLevel(models.Model):
    """
    Available ProcessingLevels, e.g. L1, L1A, ...

    NOTE: This model has the same *name* as one used in old dictionary
    implementation, we need to be careful when switching over to new_dicts
    """
    abbreviation = models.CharField(max_length=4, unique=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the processing level.')

    def __unicode__(self):
        return u'{0} {1}'.format(self.abbreviation, self.name)


class Collection(models.Model):
    """Collection of satellites managed by a single operator."""

    name = models.CharField(
        max_length=255, unique=True,
        verbose_name='Collection name',
        help_text='Collection name as defined by operator.')
    description = models.TextField(
        verbose_name='Collection description',
        help_text='Detailed description for this collection')
    institution = models.ForeignKey(
        # NOTE: when referencing models in another application we need ti
        # specify a model with the full application label
        'catalogue.Institution',
        help_text='Organisation that owns this satellite collection.')

    def __unicode__(self):
        return self.name


class Satellite(models.Model):
    """Satellite e.g. SPOT5 - a real satellite in the sky."""

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the satellite.')
    abbreviation = models.CharField(max_length=20, unique=True)
    operator_abbreviation = models.CharField(
        max_length=255, unique=True,
        help_text='Satellite abbreviation as named by operator.')
    #image = models.ImageField()
    collection = models.ForeignKey(Collection)
    launch_date = models.DateField(
        blank=True, null=True,
        help_text='Satellite launch date')
    status = models.TextField(
        blank=True, null=True,
        help_text='Information about satellite operational status')
    altitude_km = models.IntegerField(
        blank=True, null=True,
        help_text='Satellite altitude in kilometres')
    orbit = models.TextField(
        blank=True, null=True,
        help_text='Satellite orbit description')
    revist_time_days = models.IntegerField(
        blank=True, null=True,
        help_text='Days elapsed between observations of the same point')
    reference_url = models.URLField(
        blank=True, null=True,
        help_text='Satellite mission URL')
    license_type = models.ForeignKey(
        'catalogue.License',
        help_text='Satellite product license type')

    def __unicode__(self):
        """Return 'operator_abbreviation' as model representation."""
        return u'{0}'.format(self.operator_abbreviation)


class ScannerType(models.Model):
    """Scanner type for the instrument type e.g. Pushbroom"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the scanner type.')
    abbreviation = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.abbreviation


class InstrumentType(models.Model):
    """Instrument - a type of sensor on the mission or satellite - e.g. HRV."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the instrument type.')
    abbreviation = models.CharField(max_length=20, unique=True)
    operator_abbreviation = models.CharField(
        max_length=255, unique=True,
        help_text='Satellite abbreviation as named by operator.')
    is_radar = models.BooleanField(
        verbose_name='Is this a RADAR sensor?',
        help_text='Mark true if this sensor captures RADAR data.',
        default=False
    )
    is_taskable = models.BooleanField(
        default=False,
        help_text='Can this sensor be tasked?'
    )
    scanner_type = models.ForeignKey(ScannerType)
    base_processing_level = models.ForeignKey(
        ProcessingLevel,
        help_text=('Processing level as provided by the ground station as '
                   '"raw data".'))
    # default_processing_level = models.ForeignKey(
    #     ProcessingLevel,
    #     help_text=('Default processing level that will be supplied to '
    #                'customers.'))
    reference_system = models.ForeignKey(
        'ReferenceSystem',
        blank=True, null=True
    )
    swath_optical_km = models.IntegerField(
        blank=True, null=True,
        help_text='On-ground sensor swath width')
    band_count = models.IntegerField(
        blank=True, null=True,
        help_text='Total number of bands for this Instrument')
    band_type = models.TextField(
        blank=True, null=True,
        help_text='Semicolon delimited list of Instrument band types')
    spectral_range_list_nm = models.CharField(
        blank=True, null=True,
        max_length=100,
        help_text='Semicolon delimited list of Instrument spectral ranges')
    pixel_size_list_m = models.CharField(
        blank=True, null=True,
        max_length=100,
        help_text='Semicolon delimited list of Instrument pixel sizes')
    spatial_resolution_range = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Semicolon delimited list of Instrument spatial resolutions')
    quantization_bits = models.IntegerField(
        blank=True, null=True,
        help_text='Quantization bit rate')
    image_size_km = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Human readable representation of image size')
    processing_software = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Description of processing software')
    keywords = models.CharField(
        blank=True, null=True,
        max_length=255,
        help_text='Keywords describing InstrumentType')

    def __unicode__(self):
        return self.operator_abbreviation


class RadarBeam(models.Model):
    """
    Only for Radar products
    """
    instrument_type = models.OneToOneField(InstrumentType)
    band_name = models.CharField(
        max_length=50,
        help_text='RadarBeam band name'
    )
    wavelength_cm = models.IntegerField(
        help_text='Band wavelength in centimetres')
    looking_distance = models.CharField(
        max_length=50,
        help_text='REPLACE ME!'
    )
    azimuth_direction = models.CharField(
        max_length=50,
        help_text='REPLACE ME!'
    )

    def __unicode__(self):
        return u'{0} ({1})'.format(self.band_name, self.wavelength_cm)


class ImagingMode(models.Model):
    """
    Imaging mode for a radar beam
    """
    POLARIZATION_SET = (
        ('HH', 'Horizontal-Horizontal'),
        ('HV', 'Horizontal-Vertical'),
        ('VH', 'Vertical-Horizontal'),
        ('VV', 'Vertical-Vertical'),
    )
    radarbeam = models.ForeignKey(RadarBeam)
    name = models.CharField(
        max_length=50,
        help_text='ImagingMode name'
    )
    incidence_angle_min = models.FloatField(
        help_text='Minimum incidence angle'
    )
    incidence_angle_max = models.FloatField(
        help_text='Maximum incidence angle'
    )
    approximate_resolution_m = models.FloatField(
        help_text='Approximate ImagingMode resolution in meters'
    )
    swath_width_km = models.FloatField(
        help_text='Swath width in kilometres'
    )
    number_of_looks = models.IntegerField(
        help_text='REPLACE ME!'
    )
    polarization = models.CharField(
        max_length=2, choices=POLARIZATION_SET,
        help_text='Polarization type'
    )

    def __unicode__(self):
        return u'{0} ({1})'.format(self.name, self.polarization)


class SatelliteInstrumentGroup(models.Model):
    """Satellite instrument group - an instrument as deployed on a satellite.
    """
    satellite = models.ForeignKey('Satellite')
    instrument_type = models.ForeignKey('InstrumentType')

    class Meta:
        unique_together = (
            'satellite',
            'instrument_type'
        )

    def __unicode__(self):
        return u'{0} - {1}'.format(
            self.satellite.operator_abbreviation,
            self.instrument_type.operator_abbreviation
        )

    def products_per_year(self):
        myStats = executeRAWSQL("""
SELECT count(*) as count, extract(YEAR from gp.product_date)::int as year
FROM
  catalogue_genericproduct gp, catalogue_genericimageryproduct gip,
  catalogue_genericsensorproduct gsp, catalogue_opticalproduct op,
  dictionaries_opticalproductprofile opp, dictionaries_satelliteinstrument si
WHERE
  gip.genericproduct_ptr_id = gp.id AND
  gsp.genericimageryproduct_ptr_id = gip.genericproduct_ptr_id AND
  op.genericsensorproduct_ptr_id = gsp.genericimageryproduct_ptr_id AND
  opp.id = op.product_profile_id AND opp.satellite_instrument_id = si.id
  AND si.satellite_instrument_group_id=%(sensor_pk)s
GROUP BY extract(YEAR from gp.product_date)
ORDER BY year ASC;""", {'sensor_pk': self.pk})
        return myStats


class SatelliteInstrument(models.Model):
    """Satellite instrument - a specific instrument as deployed on a satellite.
    Note that there may be more than one instrument of the same type per
    satellite e.g. SPOT 5 HRG (camera 1 and 2).
    """

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the satellite instrument.')
    abbreviation = models.CharField(max_length=20, unique=True)
    operator_abbreviation = models.CharField(
        max_length=255, unique=True,
        help_text='Satellite abbreviation as named by operator.')
    satellite_instrument_group = models.ForeignKey('SatelliteInstrumentGroup')

    def __unicode__(self):
        """Return 'operator_abbreviation' as model representation."""
        return u'{0}'.format(self.operator_abbreviation)


class Band(models.Model):
    """Wavelength to bands relation

    Band examples:
        red - 400-484 (wavelength)
    """
    instrument_type = models.ForeignKey(InstrumentType)
    band_name = models.CharField(max_length=50)
    band_abbr = models.CharField(max_length=20, blank=True)
    band_number = models.IntegerField(
        help_text='Instrument specific band number, e.g. 1,2, ...')
    min_wavelength_nm = models.IntegerField(
        help_text='Lower band wavelength in nanometeres')
    max_wavelength_nm = models.IntegerField(
        help_text='Upper band wavelength in nanometeres')
    pixelsize_resampled_m = models.FloatField(
        help_text='Pixel size in m (resolution) resampled')
    pixelsize_acquired_m = models.FloatField(
        help_text='Pixel size in m (resolution) acquired')

    def __unicode__(self):
        return u'{0} ({1} {2}) {3}'.format(
            self.band_name, self.min_wavelength_nm, self.max_wavelength_nm,
            self.pixelsize_resampled_m)


class SpectralGroup(models.Model):
    """A generic named spectral mode that describes spectral grouping.
    e.g Panchromatic, Multispectral, Thermal, Hyperspectral.

    Mode examples:
         J = Multispectral 10m
         P/M = Panchromatic 10m
         A/B = Panchromatic 5m
         T = Panchromatic 2.5m
         X = Multispectral 20m
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the spectral mode.')
    abbreviation = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return self.name


class SpectralMode(models.Model):
    """
    A specific spectral mode for of an instrument type
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the spectral mode.')
    abbreviation = models.CharField(max_length=20)
    instrument_type = models.ForeignKey(InstrumentType)
    spectralgroup = models.ForeignKey(SpectralGroup)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.instrument_type.name)


class BandSpectralMode(models.Model):
    """
    Band to SpectralMode relation
    """
    band = models.ForeignKey(Band)
    spectral_mode = models.ForeignKey(SpectralMode)

    class Meta:
        unique_together = (('band', 'spectral_mode'),)

    def __unicode__(self):
        return u'{0} ({1})'.format(
            self.band.band_name, self.spectral_mode.name)


class InstrumentTypeProcessingLevel(models.Model):
    """
    Relation between ProcessingLevel and InstrumentType
    """
    instrument_type = models.ForeignKey(InstrumentType)
    processinglevel = models.ForeignKey(ProcessingLevel)
    operator_processing_level_name = models.CharField(
        max_length=50,
        help_text='Operator original processing level name'
    )
    operator_processing_level_abbreviation = models.CharField(
        max_length=4,
        help_text='Operator original processing level abbreviation'
    )

    def __unicode__(self):
        return u'{0} - {1}'.format(
            self.instrument_type.name, self.processinglevel.abbreviation)


class SpectralModeProcessingCosts(models.Model):
    """
    Processing costs for specific processing level per spectral mode
    """
    spectral_mode = models.ForeignKey(SpectralMode)
    instrumenttypeprocessinglevel = models.ForeignKey(
        InstrumentTypeProcessingLevel
    )
    cost_per_scene_in_rands = models.FloatField(
        help_text='Cost per scene in ZAR (rands)'
    )
    foreign_currency = models.ForeignKey(
        'ForeignCurrency',
        null=True, blank=True
    )
    cost_per_scene_in_foreign = models.FloatField(
        null=True, blank=True,
        help_text='Cost per scene in foreign currency'
    )

    def __unicode__(self):
        return u'{0} ZAR ({1} - {2})'.format(
            self.cost_per_scene_in_rands,
            self.spectral_mode.name, self.instrumenttypeprocessinglevel)


class ReferenceSystem(models.Model):
    """
    Spatial Reference information
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the reference system.')
    abbreviation = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class ForeignCurrency(models.Model):
    """
    Foreign currency lookup table

    conversion_rate: 1.00 unit in ZAR (i.e. 1.00 USD = 8.8634 ZAR)
    """
    abbreviation = models.CharField(max_length=20)
    name = models.CharField(max_length=255, unique=True)
    conversion_rate = models.FloatField(
        null=True, blank=True,
        help_text='Conversion rate for 1.00 unit in ZAR')

    def __unicode__(self):
        return self.name
