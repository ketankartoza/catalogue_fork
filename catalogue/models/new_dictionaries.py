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
from dictionaries import Institution


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
        Institution,
        help_text='Organisation that owns this satellite collection.')

    class Meta:
        app_label = 'catalogue'

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

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        """Return 'operator_abbreviation' as model representation."""
        return '%s' % self.operator_abbreviation


class ScannerType(models.Model):
    """Scanner type for the instrument type e.g. Pushbroom"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the scanner type.')
    abbreviation = models.CharField(max_length=20, unique=True)

    class Meta:
        app_label = 'catalogue'

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

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.operator_abbreviation


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
        app_label = 'catalogue'
        unique_together = ('operator_abbreviation',
                           'satellite',
                           'instrument_type')

    def __unicode__(self):
        """Return 'operator_abbreviation' as model representation."""
        return '%s' % self.operator_abbreviation


class Band(models.Model):
    """Wavelength to bands relation

    Band examples:
        red - 400-484 (wavelength)
    """
    band_name = models.CharField(max_length=50)
    min_wavelength = models.IntegerField(
        help_text='Lower band wavelength')
    max_wavelength = models.IntegerField(
        help_text='Upper band wavelength')

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return '%s (%i %i)' % (
            self.band_name, self.min_wavelength, self.max_wavelength)


class PixelSize(models.Model):
    """Pixelsize of a sensor, related to Bands

    Some sensors shoot in different resolutions on different bands
    """
    pixel_size_avg = models.FloatField(
        help_text='Average pixel size in meters')
    pixel_size_x = models.FloatField(
        help_text='Pixel size in meteres in X direction')
    pixel_size_y = models.FloatField(
        help_text='Pixel size in meteres in Y direction')

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return '%f (%f %f)' % (
            self.pixel_size_avg, self.pixel_size_x, self.pixel_size_y)


class BandPixelSize(models.Model):
    """
    Band to PixelSize relation
    """
    band = models.ForeignKey(Band)
    pixelsize = models.ForeignKey(PixelSize)

    class Meta:
        app_label = 'catalogue'
        unique_together = (('band', 'pixelsize'),)

    def __unicode__(self):
        return '%s (%f)' % (
            self.band.band_name, self.pixelsize.pixel_size_avg)


class SpectralMode(models.Model):
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
    spatial_resolution = models.FloatField(
        help_text='Spatial resolution in m')
    bandpixelsize = models.ManyToManyField(BandPixelSize)
    instrument_type = models.ForeignKey(InstrumentType)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name
