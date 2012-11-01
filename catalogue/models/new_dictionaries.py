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

    name = models.CharField(max_length=255, unique=True,
                verbose_name='Collection name',
                help_text='Collection name as defined by operator.')
    description = models.TextField(
        verbose_name='Collection description',
        help_text='Detailed description for this collection')
    institution = models.ForeignKey(Institution,
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
    operator_abbreviation = models.CharField(max_length=255, unique=True,
            help_text='Satellite abbreviation as named by operator.')
    #image = models.ImageField()
    collection = models.ForeignKey(Collection)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        """Return 'operator_abbreviation' as model representation."""
        return '%s' % self.operator_abbreviation

    def relatedSatelliteInstruments(self):
        """Get a collection of SatelliteInstruments for this satellite."""
        mySatelliteInstruments = SatelliteInstrument.objects.filter(
            satellite=self)
        return mySatelliteInstruments


class InstrumentType(models.Model):
    """Instrument - a type of sensor on the mission or satellite - e.g. HRV."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the instrument type.')
    abbreviation = models.CharField(max_length=20, unique=True)
    operator_abbreviation = models.CharField(max_length=255, unique=True,
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

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.operator_abbreviation

    def relatedSpectralModes(self):
        """Get a collection of InstrumentSpectralModes for this InstrumentType.
        """
        myInstrumentTypeSpectralModes = (InstrumentTypeSpectralMode.objects.
            filter(instrument_type=self))
        return myInstrumentTypeSpectralModes

    def relatedScannerType(self):
        """Get a collection of ScannerTypes for this InstrumentType."""
        myScannerTypes = ScannerType.objects.filter(instrument_type=self)
        return myScannerTypes

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
    operator_abbreviation = models.CharField(max_length=255, unique=True,
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


class SpectralMode(models.Model):
    """A generic named spectral mode that describes spectral grouping.
    e.g Panchromatic, Multispectral, Thermal, Hyperspectral.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the spectral mode.')
    abbreviation = models.CharField(max_length=20, unique=True)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name


class InstrumentTypeSpectralMode(models.Model):
    """Instrument specific mode with common spatial and spectral resolution.

    These are operator and instrument specific. It is related to both
    an Instrument and a generic Spectral Mode. The reason for the spectral
    mode relate is so that we can get generic attributes e.g. 'this is a
    panchromatic image'.

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
        help_text=('A detailed description of the instrument type\'s'
                   'spectral mode.'))
    abbreviation = models.CharField(max_length=20, unique=True)
    instrument_type = models.ForeignKey(InstrumentType)
    spectral_mode = models.ForeignKey(SpectralMode)
    spatial_resolution = models.FloatField(
        help_text='Spatial resolution in m')
    band_count = models.IntegerField()

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name


class ScannerType(models.Model):
    """Scanner type for the instrument type e.g. Pushbroom"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(
        verbose_name='Detailed description.',
        help_text='A detailed description of the scanner type.')
    abbreviation = models.CharField(max_length=20, unique=True)
    instrument_type = models.ForeignKey(InstrumentType)

    class Meta:
        app_label = 'catalogue'
        unique_together = ('instrument_type', 'abbreviation')

    def __unicode__(self):
        return self.abbreviation
