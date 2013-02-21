"""
SANSA-EO Catalogue - Landsat LGPS L1G importer.

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__version__ = '0.1'
__date__ = '21/02/2013'
__copyright__ = 'South African National Space Agency'

import os
import glob
from datetime import datetime, timedelta
from xml.dom.minidom import parse

from django.db import transaction

from dictionaries.models import (
    SpectralMode,
    SatelliteInstrument,
    OpticalProductProfile)


def parseDateTime(theDate):
    """A helper method to create a date object from a landsate time stamp.

    Args:
        theDate: str - a string containing date in this format:
            :samp:`19890503 07:30:05`
    Returns:
        datetime - a python datetime object
    Raises:
        None
    """
    #print 'Parsing Date: %s\n' % theDate
    myStartYear = theDate[0:4]
    myStartMonth = theDate[4:6]
    myStartDay = theDate[6:8]
    myStartTime = theDate[9:17]
    myTokens = myStartTime.split(':')
    myStartHour = myTokens[0]
    myStartMinute = myTokens[1]
    myStartSeconds = myTokens[2]
    #print "%s-%s-%s %s:%s:%s" % (
    #    myStartYear, myStartMonth, myStartDay,
    #    myStartHour, myStartMinute, myStartSeconds)
    myDateTime = datetime(
        int(myStartYear),
        int(myStartMonth),
        int(myStartDay),
        int(myStartHour),
        int(myStartMinute),
        int(myStartSeconds))
    return myDateTime


@transaction.commit_manually
def ingest(
        theTestOnlyFlag=False,
        theSourceDir=None,
        theVerbosityLevel=1,
        theLicense='SANSA Commercial License',
        theOwner='USGS',
        theSoftware='LGPS 11.6.0',
        theQuality='Unknown',
        theHaltOnErrorFlag=True):
    """
    Ingest a collection of Landsat metadata folders.

    Args:
        theTestOnlyFlag - (Optional) Defaults to False. Whether to do a dummy
           run (database will not be updated).
        theSourceDir - (Required) A shapefile downloaded from
           http://catalog.spotimage.com/pagedownload.aspx
        theVerbosityLevel - (Optional) Defaults to 1. How verbose the logging
           output should be. 0-2 where 2 is very very very very verbose!
        theLicense - (Optional) Defaults to 'SANSA Commercial License', License
           holder of the product.
        theOwner - (Optional) Defaults to 'Astrium', Original provider / owner
           of the data.
        theSoftware - (Optional) Defaults to 'TS5', The software used to create
           / extract the product.
        theQuality - (Optional) Defaults to 'Unknown', A quality assessment for
           these images. Note from Tim & Linda: This doesnt really make sense!
           TODO: Remove this parameter?
        theHaltOnErrorFlag: bool - set to True if we should stop processing
            when the first error is encountered.
    Returns:
        None
    Exceptions:
        Any unhandled exceptions will be raised.
    """
    def logMessage(theMessage, theLevel=1):
        if theVerbosityLevel >= theLevel:
            print theMessage

    logMessage((
        'Running LGPS Landsat Importer with these options:\n'
        'Test Only Flag: %s\n'
        'Source Dir: %s\n'
        'Verbosity Level: %s\n'
        'License: %s\n'
        'Owner: %s\n'
        'Software: %s\n'
        'Quality: %s\n'
        'Halt on error: %s\n'
        '------------------')
        % (theTestOnlyFlag, theSourceDir, theVerbosityLevel, theLicense,
           theOwner, theSoftware, theQuality, theHaltOnErrorFlag), 2)

    # Scan the source folder and look for any subfolders
    # The subfolder names should be e.g. L519890503170076
    # Which will be used as the original_product_id
    logMessage('Scanning folders in %s' % theSourceDir, 1)
    # Loop through each folder found
    for myFolder in glob.glob(os.path.join(theSourceDir, '*')):
        # Get the folder name
        myProductFolder = os.path.split(myFolder)[-1]
        logMessage(myProductFolder, 2)
        # Find the first and only xml file in the folder
        mySearchPath = os.path.join(str(myFolder), '*.xml')
        logMessage(mySearchPath, 2)
        myXmlFile = glob.glob(mySearchPath)[0]
        logMessage(myXmlFile, 2)

        # Create a DOM document from the file
        myDom = parse(myXmlFile)

        # Look for key concepts needed to create a OpticalProduct
        myElement = myDom.getElementsByTagName('ACQUISITION_DATE')[0]
        myProductDate = myElement.firstChild.nodeValue
        logMessage('Product Date: %s' % myProductDate, 2)

        myElement = myDom.getElementsByTagName('TEMPORALEXTENTFROM')[0]
        myStartDate = myElement.firstChild.nodeValue
        myStartDateTime = parseDateTime(myStartDate)
        logMessage('Product Start Date: %s' % myStartDateTime, 2)

        myElement = myDom.getElementsByTagName('TEMPORALEXTENTTO')[0]
        myEndDate = myElement.firstChild.nodeValue
        myEndDateTime = parseDateTime(myEndDate)
        logMessage('Product End Date: %s' % myEndDateTime, 2)
        # Find out the time at the center of the imagery
        myDelta = myEndDateTime - myStartDateTime
        us1 = myDelta.microseconds + 1000000 * (
            myDelta.seconds + 86400 * myDelta.days)
        myMidPointDiffMicroseconds = us1 / 2

        myMidDateTime = myStartDateTime + timedelta(
            microseconds=myMidPointDiffMicroseconds)
        logMessage('Mid Scene Date: %s' % myMidDateTime, 2)

        # Get the instrument name from the metadata so we can
        # determine if this is L7 or L5
        myElement = myDom.getElementsByTagName('INSTRUMENTNAME')[0]
        myInstrumentName = myElement.firstChild.nodeValue
        logMessage('Instrument Name: %s' % myInstrumentName, 2)

        # Need to get the Spectral mode
        # If its Landsat 7, spectral mode is ETM+ HRF
        # If its Landsat 5, spectral modes i TM HRF
        #
        # select * from dictionaries_spectralmode;
        #
        # id| name     | description
        # 1 | ETM+ HRF | Landsat 7 ETM+ Multi-spectral bands denoted as HRF
        # 4 | TM HRF   | Landsat 4 or 5 TM Multi-spectral bands denoted as HRF
        mySpectralModeMapping = {
            'TM': 'TM HRF',
            'ETM+': 'ETM+ HRF'}
        mySpectralMode = SpectralMode.objects.get(
            name=mySpectralModeMapping[myInstrumentName])
        logMessage('Spectral Mode: %s' % mySpectralMode, 2)
        # And the SatelliteInstrument
        #id |          name
        #----+------------------------
        # ...
        # 17 | Landsat 5 TM
        # 18 | Landsat 7 ETM+
        # ...
        #(23 rows)
        mySatelliteInstrumentMapping = {
            'TM': 'Landsat 5 TM',
            'ETM+': 'Landsat 7 ETM+'}
        mySatelliteInstrument = SatelliteInstrument.objects.get(
            name=mySatelliteInstrumentMapping[myInstrumentName])
        logMessage('Satellite Instrument: %s' % mySatelliteInstrument, 2)

        # So that we can get the optical product OpticalProductProfile
        myProfile = OpticalProductProfile(
            spectral_mode=mySpectralMode,
            satellite_instrument=mySatelliteInstrument)
        logMessage('Spectral Profile: %s' % myProfile, 2)
        # Get the base processing level
        myProcessingLevel = myProfile.baseProcessingLevel()
        logMessage('Processing Level: %s' % myProcessingLevel, 2)
        # Get the spatial coverage
        myElement = myDom.getElementsByTagName('UL_LAT')[0]
        myUpperLeftLat = myElement.firstChild.nodeValue
        logMessage('Upper Left Lat: %s' % myUpperLeftLat, 2)

        myElement = myDom.getElementsByTagName('UL_LONG')[0]
        myUpperLeftLon = myElement.firstChild.nodeValue
        logMessage('Upper Left Lon: %s' % myUpperLeftLon, 2)

        myElement = myDom.getElementsByTagName('LL_LAT')[0]
        myLowerLeftLat = myElement.firstChild.nodeValue
        logMessage('Lower Left Lat: %s' % myLowerLeftLat, 2)

        myElement = myDom.getElementsByTagName('LL_LONG')[0]
        myLowerLeftLon = myElement.firstChild.nodeValue
        logMessage('Lower Left Lon: %s' % myLowerLeftLon, 2)

        myElement = myDom.getElementsByTagName('UR_LAT')[0]
        myUpperRightLat = myElement.firstChild.nodeValue
        logMessage('Upper Right Lat: %s' % myUpperRightLat, 2)

        myElement = myDom.getElementsByTagName('UR_LONG')[0]
        myUpperRightLon = myElement.firstChild.nodeValue
        logMessage('Upper Right Lon: %s' % myUpperRightLon, 2)

        myElement = myDom.getElementsByTagName('LR_LAT')[0]
        myLowerRightLat = myElement.firstChild.nodeValue
        logMessage('Lower Right Lat: %s' % myLowerRightLat, 2)

        myElement = myDom.getElementsByTagName('LR_LONG')[0]
        myLowerRightLon = myElement.firstChild.nodeValue
        logMessage('Lower Right Lon: %s' % myLowerRightLon, 2)

        # Now make a WKT polygon
        myWkt = ('POLYGON((%s %s,%s %s,%s %s,%s %s,%s %s))' % (
            myUpperLeftLon, myUpperLeftLat,
            myUpperRightLon, myUpperRightLat,
            myLowerRightLon, myLowerRightLat,
            myLowerLeftLon, myLowerLeftLat,
            myUpperLeftLon, myUpperLeftLat))
        logMessage(myWkt, 2)
        # Check if there is already a matching product based
        # on original_product_id

        # If yes, update

        # If no, create
        if theTestOnlyFlag:
            transaction.rollback()
            logMessage('Imported scene : %s' % myProductFolder, 1)
            logMessage('Testing only: transaction rollback.', 1)
        else:
            transaction.commit()
            logMessage('Imported scene : %s' % myProductFolder, 1)

    # To decide: should we remove ingested product folders?
