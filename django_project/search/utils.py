"""
SANSA-EO Catalogue - Search related views

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
__date__ = '24/02/2013'
__copyright__ = 'South African National Space Agency'

# python logger support to django logger middleware
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from dictionaries.models import (
    OpticalProductProfile,
    InstrumentType,
    Satellite,
    SpectralGroup
)


def prepareSelectQuerysets(theInstrumentType, theSatellite, theSpectralGroup):
    """
    Prepares instrument_type, satellite and spectral_modes querysets

    Used to dynamically slice available options
    """

    myOPP = OpticalProductProfile.objects
    if theInstrumentType != []:
        logger.debug('setting insttype %s', theInstrumentType)
        myOPP = myOPP.filter(
            satellite_instrument__instrument_type__in=theInstrumentType)
    if theSatellite != '':
        logger.debug('setting satellite %s', theSatellite)
        myOPP = myOPP.filter(
            satellite_instrument__satellite=theSatellite)
    if theSpectralGroup != '':
        logger.debug('setting spectral group %s', theSpectralGroup)
        myOPP = myOPP.filter(spectral_mode__spectral_group=theSpectralGroup)

    # if user selected instrument type or spectral_mode filter inst_types
    if theSatellite != '' or theSpectralGroup != '':
        logger.debug('User selected satellite or spectral mode')
        myInstType_QS = InstrumentType.objects.filter(
            satelliteinstrument__opticalproductprofile__in=myOPP).distinct(
            ).order_by('id')
    else:
        logger.debug('User DID NOT select satellite or spectral mode')
        # show all instrument types
        myInstType_QS = InstrumentType.objects.filter(
            satelliteinstrument__opticalproductprofile__in=
            OpticalProductProfile.objects).distinct().order_by('id')

    mySatellite_QS = Satellite.objects.filter(
        satelliteinstrument__opticalproductprofile__in=myOPP).distinct(
        ).order_by('id')
    mySpectralGroup_QS = SpectralGroup.objects.filter(
        spectralmode__opticalproductprofile__in=myOPP).distinct(
        ).order_by('id')

    return myInstType_QS, mySatellite_QS, mySpectralGroup_QS
