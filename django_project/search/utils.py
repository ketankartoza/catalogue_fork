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
    Collection,
    InstrumentType,
    Satellite,
    SpectralGroup
)

from catalogue.models import License


def prepareSelectQuerysets(
        theCollection=[], theSatellite=[], theInstrumentType=[],
        theSpectralGroup=[], theLicenseTypes=[]):
    """
    Prepares instrument_type, satellite and spectral_modes querysets

    Used to dynamically slice available options
    """

    myOPP = OpticalProductProfile.objects

    if theCollection != []:
        logger.debug('setting collection %s', theCollection)
        myOPP = myOPP.filter(
            satellite_instrument__satellite__collection__in=theCollection)

    if theSatellite != []:
        logger.debug('setting satellite %s', theSatellite)
        myOPP = myOPP.filter(
            satellite_instrument__satellite__in=theSatellite)

    if theInstrumentType != []:
        logger.debug('setting instrument_type %s', theInstrumentType)
        myOPP = myOPP.filter(
            satellite_instrument__instrument_type__in=theInstrumentType)

    if theSpectralGroup != []:
        logger.debug('setting spectral_group %s', theSpectralGroup)
        myOPP = myOPP.filter(
            spectral_mode__spectralgroup__in=theSpectralGroup)

    if theLicenseTypes != []:
        logger.debug('setting license_type %s', theLicenseTypes)
        myOPP = myOPP.filter(
            satelliteinstrument__satellite__license_type__in=theLicenseTypes)

    # update querysets
    myCollection_QS = Collection.objects.filter(
        satellite__satelliteinstrument__opticalproductprofile__in=myOPP)\
        .distinct().order_by('name')

    mySatellite_QS = Satellite.objects.filter(
        satelliteinstrument__opticalproductprofile__in=myOPP)\
        .distinct().order_by('name')

    myInstType_QS = InstrumentType.objects.filter(
        satelliteinstrument__opticalproductprofile__in=myOPP)\
        .distinct().order_by('name')

    mySpectralGroup_QS = SpectralGroup.objects.filter(
        spectralmode__opticalproductprofile__in=myOPP)\
        .distinct().order_by('name')

    myLicense_QS = License.objects.filter(
        satellite__satelliteinstrument__opticalproductprofile__in=myOPP)\
        .distinct().order_by('name')

    return (
        myCollection_QS, mySatellite_QS, myInstType_QS, mySpectralGroup_QS,
        myLicense_QS
    )
