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

from django.contrib.gis.db import models


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
    precursor_processing_level = models.ForeignKey(
        'self', blank=True, null=True)

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
        'django_project.catalogue.Institution',
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
    revisttime_days = models.IntegerField(
        blank=True, null=True,
        help_text='Days elapsed between observations of the same point')
    reference_url = models.URLField(
        blank=True, null=True,
        help_text='Satellite mission URL')
    license_type = models.ForeignKey(
        'django_project.catalogue.License',
        blank=True, null=True,
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
        blank=True, null=True)
    reference_system = models.CharField(
        max_length=255, blank=True, null=True,
        help_text='Textual information for reference system')
    swath_optical_km = models.IntegerField(
        blank=True, null=True,
        help_text='On-ground sensor swath width')
    band_number_total = models.IntegerField(
        blank=True, null=True,
        help_text='Total number of bands for this Instrument')
    band_type = models.TextField(
        blank=True, null=True,
        help_text='Semicolon delimited list of Instrument band types')
    spectral_range = models.CharField(
        blank=True, null=True,
        max_length=100,
        help_text='Accumulated spectral range of the Instrument')
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
    wavelength = models.IntegerField(
        help_text='Band wavelength in nanometres')
    looking_distance = models.CharField(
        max_length=50,
        help_text='REPLACE ME!'
    )
    azimuth_direction = models.CharField(
        max_length=50,
        help_text='REPLACE ME!'
    )

    def __unicode__(self):
        return u'{0} ({1})'.format(self.band_name, self.wavelength)


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
    approximate_resolution = models.FloatField(
        help_text='Approximate ImagingMode resolution in REPLACE ME'
    )
    swath_width = models.FloatField(
        help_text='Swath width in REPLACE ME'
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


class SatelliteInstrument(models.Model):
    """Satellite instrument - an instrument as deployed on a satellite.
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
    satellite = models.ForeignKey(Satellite)
    instrument_type = models.ForeignKey(InstrumentType)

    class Meta:
        unique_together = ('operator_abbreviation',
                           'satellite',
                           'instrument_type')

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
    min_wavelength = models.IntegerField(
        help_text='Lower band wavelength in nanometeres')
    max_wavelength = models.IntegerField(
        help_text='Upper band wavelength in nanometeres')
    pixelsize_resampled = models.IntegerField(
        help_text='Pixel size in m (resolution) resampled')
    pixelsize_acquired = models.IntegerField(
        blank=True, null=True,
        help_text='Pixel size in m (resolution) acquired')

    def __unicode__(self):
        return u'{0} ({1} {2}) {3}'.format(
            self.band_name, self.min_wavelength, self.max_wavelength,
            self.pixelsize_resampled)


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
    abbreviation = models.CharField(max_length=20, unique=True)
    instrument_type = models.ForeignKey(InstrumentType)
    spectralgroup = models.ForeignKey(
        SpectralGroup,
        blank=True, null=True)

    def __unicode__(self):
        return u'{0} - {1}'.format(self.name, self.instrument_type.name)


class BandSpectralMode(models.Model):
    """
    Band to SpectralMode relation
    """
    band = models.ForeignKey(Band)
    spectral_mode = models.ForeignKey(
        SpectralMode,
        blank=True, null=True)

    class Meta:
        unique_together = (('band', 'spectral_mode'),)

    def __unicode__(self):
        return u'{0} ({1})'.format(
            self.band.band_name, 'spectral mode name')


class ProcessingLevelForInstrumentType(models.Model):
    """
    Relation between ProcessingLevel and InstrumentType
    """
    instrument_type = models.ForeignKey(InstrumentType)
    processinglevel = models.ForeignKey(ProcessingLevel)
    original_processing_level_name = models.CharField(
        max_length=50,
        help_text='Original processing level name')
    original_processing_level_abbr = models.CharField(
        max_length=4,
        help_text='Original processing level abbreviation')

    def __unicode__(self):
        return u'{0} - {1}'.format(
            self.instrument_type.name, self.processinglevel.abbreviation)


class ProcessingCostsForSpectralMode(models.Model):
    """
    Processing costs for specific processing level per spectral mode
    """
    spectral_mode = models.ForeignKey(SpectralGroup)
    processinglevelforinstrument_type = models.ForeignKey(
        ProcessingLevelForInstrumentType)
    cost_per_scene = models.IntegerField(
        help_text='Cost per scene')
    currency_abbr = models.CharField(
        max_length=12,
        help_text='Currency abbreviation')

    def __unicode__(self):
        return u'{0}{1} ({2} - {3})'.format(
            self.cost_per_scene, self.currency_abbr,
            self.spectral_mode.name, self.processinglevelforinstrument_type)
