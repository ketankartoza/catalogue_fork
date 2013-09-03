"""
SANSA-EO Catalogue - DIMS IIF metadata importer - Landsat.

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without express permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__version__ = '0.1'
__date__ = '14/08/2013'
__copyright__ = 'South African National Space Agency'

import os
import sys
import glob
from datetime import datetime  # , timedelta
from xml.dom.minidom import parse
import traceback

from django.db import transaction
from django.contrib.gis.geos import WKTReader
from django.core.management.base import CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

from dictionaries.models import (
    SpectralMode,
    SatelliteInstrument,
    OpticalProductProfile)
from catalogue.models import (
    OpticalProduct,
    Institution,
    Projection,
    License,
    CreatingSoftware,
    Quality)


def parseDateTime(theDate):
    """A helper method to create a date object from a landsat time stamp.

    :param theDate: Date in this format:
    :type theDate: str

    Example format from IIF:`1989-05-03T07:30:05.000`

    :returns: A python datetime object.
    :rtype: datetime
    """
    #print 'Parsing Date: %s\n' % theDate
    myStartYear = theDate[0:4]
    myStartMonth = theDate[5:7]
    myStartDay = theDate[8:10]
    myStartTime = theDate[11:23]
    myTokens = myStartTime.split(':')
    myStartHour = myTokens[0]
    myStartMinute = myTokens[1]
    myStartSeconds = myTokens[2]
    #print "%s-%s-%sT%s:%s:%s" % (
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
        theTestOnlyFlag=True,
        theSourceDir=(
            '/home/web/catalogue/django_project/catalogue/tests/sample_files/'
            'landsat/'),
        theVerbosityLevel=2,
        theHaltOnErrorFlag=True):
    """
    Ingest a collection of Landsat metadata folders.

    Args:
        * theTestOnlyFlag - (Optional) Defaults to False. Whether to do a dummy
           run (database will not be updated).
        * theSourceDir - (Required) A DIMS created IIF metadata xml file and
          thumbnail
        * theVerbosityLevel - (Optional) Defaults to 1. How verbose the logging
           output should be. 0-2 where 2 is very very very very verbose!
        * myLicense - (Optional) Defaults to 'SANSA Free License',
            License holder of the product.
        * theOwner - (Optional) Defaults to 'USGS', Original provider / owner
           of the data.
        * theSoftware - (Optional) Defaults to 'LPGS', The software used to
            create / extract the product.
        * theSoftwareVersion - str (Optional) Defaults to 11.6.0.
        * theQuality - (Optional) Defaults to 'Unknown', A quality assessment
            for these images defined in the IIF file.
        * theHaltOnErrorFlag: bool - set to True if we should stop processing
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
        'Running DIMS Landsat Importer with these options:\n'
        'Test Only Flag: %s\n'
        'Source Dir: %s\n'
        'Verbosity Level: %s\n'
        'Halt on error: %s\n'
        '------------------')
        % (theTestOnlyFlag, theSourceDir, theVerbosityLevel,
           theHaltOnErrorFlag), 2)

    # Scan the source folder and look for any sub-folders
    # The sub-folder names should be e.g. L519890503170076
    # Which will be used as the original_product_id
    logMessage('Scanning folders in %s' % theSourceDir, 1)
    # Loop through each folder found

    myRecordCount = 0
    myUpdatedRecordCount = 0
    myCreatedRecordCount = 0
    logMessage('Starting directory scan...', 2)

    for myFolder in glob.glob(os.path.join(theSourceDir, '*')):
        myRecordCount += 1

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

        # Get the owner - maybe fetch this via the OpticalProductProfile
        # if theOwner is None? TS
        myElement = myDom.getElementsByTagName('owner')[0]
        theOwner = myElement.firstChild.nodeValue
        logMessage('Owner: %s' % theOwner, 2)
        try:
            myOwner = Institution.objects.get_or_create(
                name=theOwner,
                defaults={
                    'address1': '',
                    'address2': '',
                    'address3': '',
                    'post_code': '', })[0]
        except Institution.DoesNotExist:
            #logMessage('Institution %s does not exists and '
            #         'cannot be created.' % owner, 2)
            raise CommandError(
                'Institution %s does not exist and '
                'cannot create: aborting' % theOwner)
        logMessage('Owner: %s' % myOwner)

        # Get the license - maybe fetch this via the OpticalProductProfile
        # if license is None? TS
        myElement = myDom.getElementsByTagName('license')[0]
        myLicense = myElement.firstChild.nodeValue
        logMessage('License: %s' % myLicense, 2)
        myLicenseMapping = {
            'USGS free distribution license': 'SANSA Free License'
        }
        theSANSALicense = License.objects.get(
            name=myLicenseMapping[myLicense])
        logMessage('License: %s' % myLicense, 2)
        logMessage('SANSA License: %s' % theSANSALicense, 2)

        try:
            myLicense = License.objects.get_or_create(
                name=theSANSALicense,
                details=myLicense)[0]
        except License.DoesNotExist:
            raise CommandError(
                'License %s does not exist and '
                'cannot create: aborting' % theOwner)
        logMessage('License: %s' % myLicense)

        # Get the creating software - maybe fetch this via the
        # OpticalProductProfile if theOwner is None? TS
        myElement = myDom.getElementsByTagName('softwareInfo.name')[0]
        mySoftware = myElement.firstChild.nodeValue
        logMessage('Software: %s' % mySoftware, 2)
        mySoftwareMapping = {
            'Pinkmatter Landsat Processor': 'LPGS'
        }
        theSoftware = CreatingSoftware.objects.get(
            name=mySoftwareMapping[mySoftware])

        logMessage('Software: %s' % mySoftware, 2)
        myElement = myDom.getElementsByTagName('softwareInfo.version')[0]
        theSoftwareVersion = myElement.firstChild.nodeValue
        logMessage('Software Version: %s' % theSoftwareVersion, 2)

        try:
            mySoftware = CreatingSoftware.objects.get_or_create(
                name=theSoftware,
                version=theSoftwareVersion)[0]
        except CreatingSoftware.DoesNotExist:
            raise CommandError(
                'Software %s does not exist and '
                'cannot create: aborting' % theOwner)

        logMessage('Software: %s' % mySoftware)

        # Get the quality assessment.
        myElement = myDom.getElementsByTagName('quality')[0]
        theQuality = myElement.firstChild.nodeValue
        logMessage('Quality: %s' % theQuality, 2)

        try:
            myQuality = Quality.objects.get_or_create(name=theQuality)[0]
        except Quality.DoesNotExist:
            #logMessage(
            #'Quality %s does not exists and cannot be created,'
            #' it will be read from metadata.' % theQuality, 2)
            raise CommandError(
                'Quality %s does not exists and cannot '
                ' be created: aborting' % theQuality)
        logMessage('Quality: %s' % myQuality)

        # Look for key concepts needed to create an OpticalProduct
        myElement = myDom.getElementsByTagName('temporalCoverage.centerTime')[0]
        myProductDate = myElement.firstChild.nodeValue
        myMidDateTime = myElement.firstChild.nodeValue
        logMessage('Product Date: %s' % myProductDate, 2)

        myElement = myDom.getElementsByTagName('temporalCoverage.startTime')[0]
        myStartDate = myElement.firstChild.nodeValue
        myStartDateTime = parseDateTime(myStartDate)
        logMessage('Product Start Date: %s' % myStartDateTime, 2)

        logMessage('Mid Scene Date: %s' % myMidDateTime, 2)

        myElement = myDom.getElementsByTagName('temporalCoverage.stopTime')[0]
        myEndDate = myElement.firstChild.nodeValue
        myEndDateTime = parseDateTime(myEndDate)
        logMessage('Product End Date: %s' % myEndDateTime, 2)

        # Get the spectral mode
        myElement = myDom.getElementsByTagName('sensor')[0]
        mySpectralModeName = myElement.firstChild.nodeValue
        logMessage('Spectral Mode: %s' % mySpectralModeName, 2)
        # Need to get the Spectral mode used for
        # Landsat 8, spectral mode is OLI_TIRS HRF
        # Landsat 8, spectral mode is OLI HRF
        # Landsat 8, spectral mode is TIRS THM
        # Landsat 7, spectral mode is ETM+ HRF
        # Landsat 5, spectral mode is TM HRF
        # Landsat 5, spectral mode is MSS HRF
        #
        # select * from dictionaries_spectralmode;
        # id| name     | description
        # 1 | ETM+ HRF | Landsat 7 ETM+ Multi-spectral bands denoted as HRF
        # 4 | TM HRF   | Landsat 4 or 5 TM Multi-spectral bands denoted as HRF
        mySpectralModeMapping = {
            'MSS': 'MSS HRF',
            'TM': 'TM HRF',
            'ETM+': 'ETM+ HRF',
            'OLI_TIRS': 'OLI_TIRS HRF',
            'OLI': 'OLI HRF',
            'TiRS': 'TIRS THM'}
        mySpectralMode = SpectralMode.objects.get(
            name=mySpectralModeMapping[mySpectralModeName])
        logMessage('Spectral Mode: %s' % mySpectralMode, 2)

        # Get the instrument name from the metadata so we can
        # determine if this is L8, L7 or L5
        myElement = myDom.getElementsByTagName('mission')[0]
        myInstrumentName = myElement.firstChild.nodeValue
        logMessage('Instrument Name: %s' % myInstrumentName, 2)

        # *** Continue from here

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
        myElement = myDom.getElementsByTagName(
            'spatialCoverage.boundingPolygon.latitiude')[0]
        myUpperLeftLat = myElement.firstChild.nodeValue
        logMessage('Upper Left Lat: %s' % myUpperLeftLat, 2)

        myElement = myDom.getElementsByTagName(
            'spatialCoverage.boundingPolygon.longitude')[0]
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

        # Now make a geometry object

        myReader = WKTReader()
        myGeometry = myReader.read(myWkt)
        #logMessage('Geometry: %s' % myGeometry, 2)

        # Get the projection - assume always UTM and South
        # we just need to find the zone.
        myElement = myDom.getElementsByTagName('ZONE')[0]
        myZone = myElement.firstChild.nodeValue
        logMessage('Zone: %s' % myZone, 2)
        myProjectionName = 'UTM%sS' % myZone
        myProjection = Projection.objects.get(name=myProjectionName)
        logMessage('Projection: %s' % myProjection, 2)

        # Get the original text file metadata
        mySearchPath = os.path.join(str(myFolder), '*.txt')
        logMessage(mySearchPath, 2)
        myTxtFile = glob.glob(mySearchPath)[0]
        logMessage(myTxtFile, 2)
        myMetadataFile = file(myTxtFile, 'rt')
        myMetadata = myMetadataFile.readlines()
        myMetadataFile.close()

        # We hard code the radiometric resolution to 8 bits
        myRadiometricResolution = 8

        # Get the band count (its also a property of GenericProduct
        myBandCount = myProfile.bandCount()

        # Get the cloud cover from the DOM document
        myElement = myDom.getElementsByTagName('CLOUDCOVERPERCENTAGE')[0]
        myCloudCover = myElement.firstChild.nodeValue
        logMessage('Cloud Cover: %s%%' % myCloudCover, 2)

        # For Landsat the Inclination Angle is None because we don't have
        # access to this data in the metadata record.
        myInclinationAngle = None
        logMessage('Inclination Angle: %s' % myInclinationAngle, 2)

        # For Landsat the Viewing Angle is None because we don't have
        # access to this data in the metadata record.
        myViewingAngle = None
        logMessage('Viewing Angle: %s' % myViewingAngle, 2)

        #Product ID is same as the folder ID??
        myOriginalProductId = myProductFolder

        # Get the solar zenith from the DOM document
        myElement = myDom.getElementsByTagName('SUN_ELEVATION')[0]
        mySolarZenithAngle = myElement.firstChild.nodeValue
        logMessage('Solar Zenith: %s' % mySolarZenithAngle, 2)

        # Get the solar azimuth from the DOM document
        myElement = myDom.getElementsByTagName('SUN_AZIMUTH')[0]
        mySolarAzimuthAngle = myElement.firstChild.nodeValue
        logMessage('Solar Azimuth: %s' % mySolarAzimuthAngle, 2)

        # We hard code the spatial resolution for both l7 and l5 to 30m
        myResolution = 30
        logMessage('Resolution: %sm' % myResolution, 2)

        # Check if there is already a matching product based
        # on original_product_id

        # Do the ingestion here...
        myData = {
            'metadata': myMetadata,
            'spatial_coverage': myGeometry,
            'radiometric_resolution': myRadiometricResolution,
            'band_count': myBandCount,
            # integer percent - must be scaled to 0-100 for all ingestors
            'cloud_cover': int(myCloudCover),
            'owner': myOwner,
            'license': myLicense,
            'creating_software': mySoftware,
            'quality': myQuality,
            'sensor_inclination_angle': myInclinationAngle,
            'sensor_viewing_angle': myViewingAngle,
            'original_product_id': myOriginalProductId,
            'solar_zenith_angle': mySolarZenithAngle,
            'solar_azimuth_angle': mySolarAzimuthAngle,
            'spatial_resolution_x': myResolution,
            'spatial_resolution_y': myResolution,
            'spatial_resolution': myResolution,
            'product_profile': myProfile,
            'product_acquisition_start': myStartDateTime,
            'product_acquisition_end': myEndDateTime,
            'product_date': myMidDateTime,
            'processing_level': myProcessingLevel
        }

        # Check if it's already in catalogue:
        try:
            #original_product_id is not necessarily unique
            #so we use product_id
            myProduct = OpticalProduct.objects.get(
                original_product_id=myOriginalProductId
            ).getConcreteInstance()
            logMessage(('Already in catalogue: updating %s.'
                        % myOriginalProductId), 2)
            myNewRecordFlag = False
            myUpdatedRecordCount += 1
            myProduct.__dict__.update(myData)
        except ObjectDoesNotExist:
            myProduct = OpticalProduct(**myData)
            logMessage('Not in catalogue: creating.', 2)
            myNewRecordFlag = True
            myCreatedRecordCount += 1

        logMessage('Saving product and setting thumb', 2)
        try:
            myProduct.save()
            if theTestOnlyFlag:
                logMessage('Testing: image not saved.', 2)
                pass
            else:
                # Store thumbnail
                myThumbsFolder = os.path.join(
                    settings.THUMBS_ROOT,
                    myProduct.thumbnailDirectory())
                try:
                    os.makedirs(myThumbsFolder)
                except OSError:
                    # TODO: check for creation failure rather than
                    # attempt to  recreate an existing dir
                    pass

                    # Transform and store .wld file
                    logMessage('Referencing thumb', 2)
                    try:
                        myPath = myProduct.georeferencedThumbnail()
                        logMessage('Georeferenced Thumb: %s' % myPath, 2)
                    except:
                        traceback.print_exc(file=sys.stdout)

            if myNewRecordFlag:
                logMessage('Product %s imported.' % myRecordCount, 2)
                pass
            else:
                logMessage('Product %s updated.' % myUpdatedRecordCount, 2)
                pass
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('Cannot import: %s' % e)

        if theTestOnlyFlag:
            transaction.rollback()
            logMessage('Imported scene : %s' % myProductFolder, 1)
            logMessage('Testing only: transaction rollback.', 1)
        else:
            transaction.commit()
            logMessage('Imported scene : %s' % myProductFolder, 1)

    # To decide: should we remove ingested product folders?
    print 'Products processed : %s ' % myRecordCount
    print 'Products updated : %s ' % myUpdatedRecordCount
    print 'Products imported : %s ' % myCreatedRecordCount
