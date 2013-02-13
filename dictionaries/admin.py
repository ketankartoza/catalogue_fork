"""
SANSA-EO Catalogue - Catalogue admin interface

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '01/01/2011'
__copyright__ = 'South African National Space Agency'

import logging

from django.contrib.gis import admin

from .models import (
    ProcessingLevel,
    Collection,
    Satellite,
    ScannerType,
    InstrumentType,
    RadarBeam,
    ImagingMode,
    SatelliteInstrument,
    Band,
    SpectralGroup,
    SpectralMode,
    BandSpectralMode,
    ProcessingLevelForInstrumentType,
    ProcessingCostsForSpectralMode
)


####################################
# New Dictionaries
####################################

class ProcessingLevelAdmin(admin.ModelAdmin):
    pass
admin.site.register(ProcessingLevel, ProcessingLevelAdmin)


class CollectionAdmin(admin.ModelAdmin):
    pass
admin.site.register(Collection, CollectionAdmin)


class SatelliteAdmin(admin.ModelAdmin):
    pass
admin.site.register(Satellite, SatelliteAdmin)


class ScannerTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(ScannerType, ScannerTypeAdmin)


class InstrumentTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(InstrumentType, InstrumentTypeAdmin)


class RadarBeamAdmin(admin.ModelAdmin):
    pass
admin.site.register(RadarBeam, RadarBeamAdmin)


class ImagingModeAdmin(admin.ModelAdmin):
    pass
admin.site.register(ImagingMode, ImagingModeAdmin)


class SatelliteInstrumentAdmin(admin.ModelAdmin):
    pass
admin.site.register(SatelliteInstrument, SatelliteInstrumentAdmin)


class BandAdmin(admin.ModelAdmin):
    pass
admin.site.register(Band, BandAdmin)


class SpectralGroupAdmin(admin.ModelAdmin):
    pass
admin.site.register(SpectralGroup, SpectralGroupAdmin)


class SpectralModeAdmin(admin.ModelAdmin):
    pass
admin.site.register(SpectralMode, SpectralModeAdmin)


class BandSpectralModeAdmin(admin.ModelAdmin):
    pass
admin.site.register(BandSpectralMode, BandSpectralModeAdmin)


class ProcessingLevelForInstrumentTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(
    ProcessingLevelForInstrumentType, ProcessingLevelForInstrumentTypeAdmin)


class ProcessingCostsForSpectralModeAdmin(admin.ModelAdmin):
    pass
admin.site.register(
    ProcessingCostsForSpectralMode, ProcessingCostsForSpectralModeAdmin)
