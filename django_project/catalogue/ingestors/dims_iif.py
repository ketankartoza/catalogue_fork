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
from cmath import log
from datetime import datetime
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
    OpticalProductProfile,
    InstrumentType,
    Satellite,
    SatelliteInstrumentGroup)

from catalogue.models import (
    OpticalProduct,
    Projection,
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
    myStartTime = theDate[11:19]
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


def get_parameters_element(myDom):
    """Get the parameters element from the dom.
    :param myDom: DOM Document containing the parameters.
    :type myDom: DOM document.

    :returns: A DOM element representing the parameters.
    :type: DOM
    """
    iif = myDom.getElementsByTagName('IIF')[0]
    item = iif.getElementsByTagName('item')[0]
    parameters = item.getElementsByTagName('parameters')[0]
    return parameters


def get_specific_parameters_element(myDom):
    """Get the specificParameters element from the dom.
    :param myDom: DOM Document containing the specificParameters element.
    :type myDom: DOM document.

    :returns: A dom element representing the specificParameters element.
    :type: DOM
    """
    iif = myDom.getElementsByTagName('IIF')[0]
    item = iif.getElementsByTagName('item')[0]
    specific_parameters = item.getElementsByTagName('specificParameters')[0]
    return specific_parameters


def get_dims_id(myDom):
    """Get the ID used by DIMS for this product.
    :param myDom: DOM Document containing the specificParameters element.
    :type myDom: DOM document.

    :returns: A dom element representing the specificParameters element.
    :type: DOM
    """
    iif = myDom.getElementsByTagName('IIF')[0]
    item = iif.getElementsByTagName('item')[0]
    administration = item.getElementsByTagName('administration')[0]
    keys = administration.getElementsByTagName('keys')
    product_id = get_feature_value('productID', keys)
    return product_id


def get_geometry(logMessage, myDom):
    """Extract the bounding box as a geometry from the xml file.

    :param logMessage: A logMessage function used for user feedback.
    :type logMessage: logMessage

    :param myDom: DOM Document containing the bounds of the scene.
    :type myDom: DOM document.

    :return: geoemtry
    """
    parameters = get_parameters_element(myDom)
    coverage = parameters.getElementsByTagName('spatialCoverage')[0]
    polygon = coverage.getElementsByTagName('boundingPolygon')[0]
    points = polygon.getElementsByTagName('point')
    polygon = 'POLYGON(('
    is_first = True
    first_longitude = None
    first_latitude = None
    for point in points:
        latitude = point.getElementsByTagName('latitude')[0]
        latitude = latitude.firstChild.nodeValue
        longitude = point.getElementsByTagName('longitude')[0]
        longitude = longitude.firstChild.nodeValue
        if not is_first:
            polygon += ','
        else:
            first_latitude = latitude
            first_longitude = longitude
            is_first = False
        polygon += '%s %s' % (longitude, latitude)
    polygon += ',%s %s))' % (first_longitude, first_latitude)
    logMessage(polygon, 2)

    # Now make a geometry object
    myReader = WKTReader()
    myGeometry = myReader.read(polygon)
    #logMessage('Geometry: %s' % myGeometry, 2)
    return myGeometry


def get_dates(logMessage, myDom):
    """Get the start, mid scene and end dates.

    :param logMessage: A logMessage function used for user feedback.
    :type logMessage: logMessage

    :param myDom: Dom Document containing the bounds of the scene.
    :type myDom: DOM document.

    :return: A three-tuple of dates for the start, mid scene and end dates
        respectively.
    :rtype: (datetime, datetime, datetime)
    """
    parameters = get_parameters_element(myDom)
    coverage = parameters.getElementsByTagName('temporalCoverage')[0]

    start_element = coverage.getElementsByTagName('startTime')[0]
    start_date = start_element.firstChild.nodeValue
    start_date = parseDateTime(start_date)
    logMessage('Product Start Date: %s' % start_date, 2)

    center_element = myDom.getElementsByTagName('centerTime')[0]
    center_date = center_element.firstChild.nodeValue
    center_date = parseDateTime(center_date)
    logMessage('Product Date: %s' % center_date, 2)

    end_element = myDom.getElementsByTagName('stopTime')[0]
    end_date = end_element.firstChild.nodeValue
    end_date = parseDateTime(end_date)
    logMessage('Product End Date: %s' % end_date, 2)

    return start_date, center_date, end_date


def get_quality(logMessage, myDom):
    """The DIMS quality indication for this scene (APPROVED or NOT_APPROVED).

    The quality is based on drop outs or any other acquisition anomalies -
    not cloud cover or rectification quality etc.

    :param logMessage: A logMessage function used for user feedback.
    :type logMessage: logMessage

    :param myDom: Dom Document containing the bounds of the scene.
    :type myDom: DOM document.

    :return: A boolean indicating if the product is approved for
        redistribution (according to DIMS).
    :rtype: bool
    """
    parameters = get_parameters_element(myDom)
    quality_element = parameters.getElementsByTagName('quality')[0]
    quality = quality_element.firstChild.nodeValue
    quality_flag = False
    if 'APPROVED' in quality:
        quality_flag = True
    logMessage('Product Quality: %s' % quality_flag, 2)
    return quality_flag


def get_feature(key, dom):
    """Find the <feature> element with key 'key' and return it as an element.

    Example::

        <feature key="resolution">
          <feature key="numberOfBands">12</feature>
          <feature key="groundSamplingDistance">
            <feature key="x">30.0</feature>
            <feature key="y">30.0</feature>
         </feature>

    Calling get_feature_value('resolution', dom) would return the dom element
     '<feature key="resolution">' and its children.

    :param key: The key to search for (represented in the xml document as
        key='foo').
    :type key: str

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: The node for this feature
    :rtype: DOM
    """
    features = dom.getElementsByTagName('feature')
    result = None
    for feature in features:
        attributes = feature.attributes.items()
        for attribute in attributes:
            if 'key' in attribute[0]:
                value = attribute[1]
                if key in value:
                    result = feature
                    break
        if result is not None:
            break
    return result


def get_feature_value(key, dom):
    """Find the <feature> element whose key matches key and return its value.

    Example::

        <feature key="fileFormatVersion">x.x</feature>
        <feature key="fileFormat">GEOTIFF</feature>
        <feature key="trackNumber">173</feature>
        <feature key="orbitNumber">20</feature>
        <feature key="productName">LC81730832013162JSA00</feature>

    Calling get_feature_value('orbitNumber', dom) would return 20.

    :param key: The key to search for (represented in the xml document as
        key='foo').
    :type key: str

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: The value of the node for this feature
    :rtype: str
    """
    features = dom.getElementsByTagName('feature')
    result = None
    for feature in features:
        attributes = feature.attributes.items()
        for attribute in attributes:
            if 'key' in attribute[0]:
                value = attribute[1]
                if key in value:
                    result = feature.firstChild.nodeValue
                    break
        if result is not None:
            break
    return result


def get_product_profile(logMessage, dom):
    """Find the product_profile for this record.

    It can be that one or more spectral modes are associated with a product.
    For example Landsat8 might have Pan (1 band), Multispectral (8 bands) and
    Thermal (2 bands) modes associated with a single product (total 11 bands).

    Because of this there is a many to many relationship on
    OpticalProductProfile and to get a specific OpticalProductProfile record
    we would need to know the satellite instrument and all the associated
    spectral modes to that profile record.

    We use the following elements to reverse engineer what the
    OpticalProductProfile is::

        <feature key="type">HRF</feature>
        <feature key="sensor">OLI_TIRS</feature>
        <feature key="mission">LANDSAT8</feature>

    :param logMessage: A logMessage function used for user feedback.
    :type logMessage: logMessage

    :param dom: Dom Document containing the bounds of the scene.
    :type dom: DOM document.

    :return: A product profile for the given product.
    :rtype: OpticalProductProfile
    """
    # We need type, sensor and mission so that we can look up the
    # OpticalProductProfile that applies to this product
    type_value = get_feature_value('type', dom)
    sensor_value = get_feature_value('sensor', dom)
    mission_value = get_feature_value('mission', dom)
    logMessage('Type (used to determine spectral mode): %s' % type_value, 2)
    logMessage(
        'Sensor (used to determine instrument type): %s' % sensor_value,  2)
    logMessage('Mission(used to determine satellite): %s' % mission_value, 2)

    instrument_type = InstrumentType.objects.get(
        abbreviation=sensor_value)  # e.g. OLI_TIRS

    if mission_value == 'LANDSAT8':
        mission_value = 'L8'
    satellite = Satellite.objects.get(abbreviation=mission_value)

    satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
        satellite=satellite, instrument_type=instrument_type)

    # Note that in some cases e.g. SPOT you may get more that one instrument
    # groups matched. When the time comes you will need to add more filtering
    # rules to ensure that you end up with only one instrument group.
    # For the mean time, we can assume that Landsat will return only one.
    satellite_instrument = SatelliteInstrument.objects.get(
        satellite_instrument_group=satellite_instrument_group)

    spectral_modes = SpectralMode.objects.filter(
        instrument_type=instrument_type)

    product_profile = OpticalProductProfile.ojects.get(
        satellite_instrument=satellite_instrument,
        spectral_mode__in=spectral_modes)

    return product_profile


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
        # Skip this record if the quality is not 'APPROVED'
        if not get_quality(logMessage, myDom):
            logMessage('Skipping %s' % myXmlFile)
            continue

        # First grab all the generic properties that any IIF will have...
        myGeometry = get_geometry(logMessage, myDom)
        myEndDateTime, myMidDateTime, myStartDateTime = get_dates(
            logMessage, myDom)

        # Now get all sensor specific metadata
        specific_parameters = get_specific_parameters_element(myDom)

        # Orbit number for GenericSensorProduct
        orbit_number = get_feature_value('orbitNumber', myDom)
        logMessage('Orbit: %s' % orbit_number, 2)

        # Original product id for GenericProduct
        original_product_id = get_feature_value('productName', myDom)
        logMessage('Product Number: %s' % original_product_id, 2)

        resolution_element = get_feature('resolution', myDom)

        # Band count for GenericImageryProduct
        band_count = get_feature_value('numberOfBands', resolution_element)
        logMessage('Band count: %s' % band_count, 2)

        # Spatial resolution x for GenericImageryProduct
        spatial_resolution_x = float(
            get_feature_value('x', resolution_element))
        logMessage('Spatial resolution x: %s' % spatial_resolution_x, 2)

        # Spatial resolution y for GenericImageryProduct
        spatial_resolution_y = float(
            get_feature_value('y', resolution_element))
        logMessage('Spatial resolution y: %s' % spatial_resolution_y, 2)

        # Spatial resolution for GenericImageryProduct calculated as (x+y)/2
        spatial_resolution = (
            spatial_resolution_x + spatial_resolution_y) / 2
        logMessage('Spatial resolution: %s' % spatial_resolution, 2)

        # Radiometric resolution for GenericImageryProduct
        # Note quantisation is mis-spelled as quantitisation in IIF docs
        base_number = int(float(get_feature_value('min', resolution_element)))
        bit_depth = int(float(get_feature_value('max', resolution_element)))
        if base_number == 0:
            bit_depth += 1
        base = 2  # to get to bit depth in base 2
        radiometric_resolution = int(log(bit_depth, base).real)
        logMessage('Radiometric resolution: %s' % radiometric_resolution, 2)

        # projection for GenericProduct
        projection_element = get_feature('projectionInfo', myDom)
        projection = get_feature_value('code', projection_element)
        logMessage('Projection: %s' % projection, 2)

        # path for GenericSensorProduct
        path = get_feature_value('path', myDom)
        logMessage('Path: %s' % path, 2)

        # row for GenericSensorProduct
        row = get_feature_value('row', myDom)
        logMessage('Row: %s' % row, 2)

        # earth_sun_distance for OpticalProduct
        earth_sun_distance = get_feature_value('earthSunDistance', myDom)
        logMessage('Earth Sun Distance: %s' % earth_sun_distance, 2)

        # solar azimuth angle for OpticalProduct
        solar_azimuth_angle = get_feature_value('solarAzimuthAngle', myDom)
        logMessage('Solar Azimuth Angle: %s' % solar_azimuth_angle, 2)

        # solar zenith angle for OpticalProduct
        solar_zenith_angle = get_feature_value('solarZenithAngle', myDom)
        logMessage('Solar Azimuth Angle: %s' % solar_zenith_angle, 2)

        # sensor viewing angle for OpticalProduct
        sensor_viewing_angle = get_feature_value('sensorViewingAngle', myDom)
        logMessage('Sensor viewing angle: %s' % sensor_viewing_angle, 2)

        # sensor inclination angle for OpticalProduct
        sensor_inclination_angle = get_feature_value(
            'sensorInclinationAngle', myDom)
        logMessage(
            'Sensor inclination angle: %s' % sensor_inclination_angle, 2)

        # cloud cover as percentage for OpticalProduct
        cloud_cover = get_feature_value('cloudCoverPercentage', myDom)
        logMessage('Cloud cover percentage: %s' % cloud_cover, 2)

        # ProductProfile for OpticalProduct
        product_profile = get_product_profile(logMessage, myDom)

        #
        #
        # Checked by Tim to here
        #
        #


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
            mySoftware = CreatingSoftware.objects.get(
                name=theSoftware,
                version=theSoftwareVersion)[0]
        except CreatingSoftware.DoesNotExist:
            raise CommandError(
                'Software %s does not exist and '
                'cannot create: aborting' % mySoftware)

        logMessage('Software: %s' % mySoftware)

        # Get the quality assessment.
        myElement = myDom.getElementsByTagName('quality')[0]
        theQuality = myElement.firstChild.nodeValue
        logMessage('Quality: %s' % theQuality, 2)

        try:
            myQuality = Quality.objects.get(name=theQuality)[0]
        except Quality.DoesNotExist:
            #logMessage(
            #'Quality %s does not exists and cannot be created,'
            #' it will be read from metadata.' % theQuality, 2)
            raise CommandError(
                'Quality %s does not exists and cannot '
                ' be created: aborting' % theQuality)
        logMessage('Quality: %s' % myQuality)

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
