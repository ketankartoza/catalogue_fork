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
    Projection)


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


def get_geometry(log_message, myDom):
    """Extract the bounding box as a geometry from the xml file.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

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
    log_message(polygon, 2)

    # Now make a geometry object
    myReader = WKTReader()
    myGeometry = myReader.read(polygon)
    #log_message('Geometry: %s' % myGeometry, 2)
    return myGeometry


def get_dates(log_message, myDom):
    """Get the start, mid scene and end dates.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

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
    log_message('Product Start Date: %s' % start_date, 2)

    center_element = myDom.getElementsByTagName('centerTime')[0]
    center_date = center_element.firstChild.nodeValue
    center_date = parseDateTime(center_date)
    log_message('Product Date: %s' % center_date, 2)

    end_element = myDom.getElementsByTagName('stopTime')[0]
    end_date = end_element.firstChild.nodeValue
    end_date = parseDateTime(end_date)
    log_message('Product End Date: %s' % end_date, 2)

    return start_date, center_date, end_date


def get_quality(log_message, myDom):
    """The DIMS quality indication for this scene (APPROVED or NOT_APPROVED).

    The quality is based on drop outs or any other acquisition anomalies -
    not cloud cover or rectification quality etc.

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

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
    log_message('Product Quality: %s' % quality_flag, 2)
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


def get_product_profile(log_message, dom):
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

    :param log_message: A log_message function used for user feedback.
    :type log_message: log_message

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
    log_message('Type (used to determine spectral mode): %s' % type_value, 2)
    log_message(
        'Sensor (used to determine instrument type): %s' % sensor_value,  2)
    log_message('Mission(used to determine satellite): %s' % mission_value, 2)

    try:
        instrument_type = InstrumentType.objects.get(
            abbreviation=sensor_value)  # e.g. OLI_TIRS
    except Exception, e:
        print e.message
        instrument_type = None
    log_message('Instrument Type %s' % instrument_type, 2)

    if mission_value == 'LANDSAT8':
        mission_value = 'L8'
    satellite = Satellite.objects.get(abbreviation=mission_value)

    try:
        satellite_instrument_group = SatelliteInstrumentGroup.objects.get(
            satellite=satellite, instrument_type=instrument_type)
    except Exception, e:
        print e.message
        satellite_instrument_group = None
    log_message('Satellite Instrument Group %s' %
                satellite_instrument_group, 2)

    # Note that in some cases e.g. SPOT you may get more that one instrument
    # groups matched. When the time comes you will need to add more filtering
    # rules to ensure that you end up with only one instrument group.
    # For the mean time, we can assume that Landsat will return only one.

    try:
        satellite_instrument = SatelliteInstrument.objects.get(
            satellite_instrument_group=satellite_instrument_group)
    except Exception, e:
        print e.message
        satellite_instrument = None
    log_message('Satellite Instrument %s' % satellite_instrument, 2)

    try:
        spectral_modes = SpectralMode.objects.filter(
            instrument_type=instrument_type)
    except Exception, e:
        print e.message
        spectral_modes = None
    log_message('Spectral Modes %s' % spectral_modes, 2)

    try:
        product_profile = OpticalProductProfile.objects.get(
            satellite_instrument=satellite_instrument,
            spectral_mode__in=spectral_modes)
    except Exception, e:
        print e.message
        product_profile = None
    log_message('Product Profile %s' % product_profile, 2)

    return product_profile


def get_radiometric_resolution(resolution_element):
    """Get the radiometric resolution for the supplied product record.

    Note that the resolution (quantitisation) is stored in the document as an
    integer describing the maximum number of values allowed per pixel (e.g.
    4096), but we want it expressed as the number of bits (e.g. 12bit,
    16bit etc.) allowed per pixel so we do some conversion of the extracted
    number.

    .. note:: quantisation is mis-spelled as quantitisation in IIF docs

    If min in the product description is 0, the max number is base 0,
    otherwise it is base 1.

    :param resolution_element: Dom Document containing the bounds of the scene.
    :type resolution_element: DOM document.

    :returns: The bit depth for the image.
    :rtype: int
    """
    base_number = int(float(get_feature_value('min', resolution_element)))
    bit_depth = int(float(get_feature_value('max', resolution_element)))
    if base_number == 0:
        bit_depth += 1
    base = 2  # to get to bit depth in base 2
    radiometric_resolution = int(log(bit_depth, base).real)
    return radiometric_resolution


def get_projection(specific_parameters):
    """Get the projection for this product record.

    The project is always expressed as an EPSG code and we fetch the related
    Projection model for that code.


    :param specific_parameters: Dom Document containing the bounds of the scene.
    :type specific_parameters: DOM document.

    :returns: A projection model for the specified EPSG.
    :rtype: Projection
    """

    projection_element = get_feature(
        'projectionInfo', specific_parameters)
    projection = get_feature_value('code', projection_element)
    projection = Projection.objects.get(epsg_code=int(projection))
    return projection


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
    def log_message(theMessage, theLevel=1):
        if theVerbosityLevel >= theLevel:
            print theMessage

    log_message((
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
    log_message('Scanning folders in %s' % theSourceDir, 1)
    # Loop through each folder found

    ingestor_version = 'DIMS IIF ingestor version 1'
    record_count = 0
    updated_record_count = 0
    created_record_count = 0
    log_message('Starting directory scan...', 2)

    for myFolder in glob.glob(os.path.join(theSourceDir, '*')):
        record_count += 1

        # Get the folder name
        myProductFolder = os.path.split(myFolder)[-1]
        log_message(myProductFolder, 2)

        # Find the first and only xml file in the folder
        mySearchPath = os.path.join(str(myFolder), '*.xml')
        log_message(mySearchPath, 2)
        myXmlFile = glob.glob(mySearchPath)[0]
        log_message(myXmlFile, 2)

        # Create a DOM document from the file
        myDom = parse(myXmlFile)
        # Skip this record if the quality is not 'APPROVED'
        if not get_quality(log_message, myDom):
            log_message('Skipping %s' % myXmlFile)
            continue

        # First grab all the generic properties that any IIF will have...
        myGeometry = get_geometry(log_message, myDom)
        start_date_time, center_date_time, end_date_time = get_dates(
            log_message, myDom)

        # Now get all sensor specific metadata
        specific_parameters = get_specific_parameters_element(myDom)

        # Orbit number for GenericSensorProduct
        orbit_number = get_feature_value(
            'orbitNumber', specific_parameters)
        #log_message('Orbit: %s' % orbit_number, 2)

        # Original product id for GenericProduct
        original_product_id = get_feature_value(
            'productName', specific_parameters)
        #log_message('Product Number: %s' % original_product_id, 2)

        resolution_element = get_feature(
            'resolution', specific_parameters)

        # Band count for GenericImageryProduct
        band_count = get_feature_value('numberOfBands', resolution_element)
        #log_message('Band count: %s' % band_count, 2)

        # Spatial resolution x for GenericImageryProduct
        spatial_resolution_x = float(
            get_feature_value('x', resolution_element))
        #log_message('Spatial resolution x: %s' % spatial_resolution_x, 2)

        # Spatial resolution y for GenericImageryProduct
        spatial_resolution_y = float(
            get_feature_value('y', resolution_element))
        #log_message('Spatial resolution y: %s' % spatial_resolution_y, 2)

        # Spatial resolution for GenericImageryProduct calculated as (x+y)/2
        spatial_resolution = (
            spatial_resolution_x + spatial_resolution_y) / 2
        #log_message('Spatial resolution: %s' % spatial_resolution, 2)

        # Radiometric resolution for GenericImageryProduct
        radiometric_resolution = get_radiometric_resolution(resolution_element)
        #log_message('Radiometric resolution: %s' % radiometric_resolution, 2)

        # projection for GenericProduct
        projection = get_projection(specific_parameters)
        #log_message('Projection: %s' % projection, 2)

        # path for GenericSensorProduct
        path = get_feature_value('path', specific_parameters)
        #log_message('Path: %s' % path, 2)

        # row for GenericSensorProduct
        row = get_feature_value('row', specific_parameters)
        #log_message('Row: %s' % row, 2)

        # earth_sun_distance for OpticalProduct
        earth_sun_distance = get_feature_value(
            'earthSunDistance', specific_parameters)
        #log_message('Earth Sun Distance: %s' % earth_sun_distance, 2)

        # solar azimuth angle for OpticalProduct
        solar_azimuth_angle = get_feature_value(
            'solarAzimuthAngle', specific_parameters)
        #log_message('Solar Azimuth Angle: %s' % solar_azimuth_angle, 2)

        # solar zenith angle for OpticalProduct
        solar_zenith_angle = get_feature_value(
            'solarZenithAngle', specific_parameters)
        #log_message('Solar Azimuth Angle: %s' % solar_zenith_angle, 2)

        # sensor viewing angle for OpticalProduct
        sensor_viewing_angle = get_feature_value(
            'sensorViewingAngle', specific_parameters)
        #log_message('Sensor viewing angle: %s' % sensor_viewing_angle, 2)

        # sensor inclination angle for OpticalProduct
        sensor_inclination_angle = get_feature_value(
            'sensorInclinationAngle', specific_parameters)
        #log_message(
        #    'Sensor inclination angle: %s' % sensor_inclination_angle, 2)

        # cloud cover as percentage for OpticalProduct
        # integer percent - must be scaled to 0-100 for all ingestors
        cloud_cover = int(get_feature_value(
            'cloudCoverPercentage', specific_parameters))
        #log_message('Cloud cover percentage: %s' % cloud_cover, 2)

        # ProductProfile for OpticalProduct
        product_profile = get_product_profile(
            log_message, specific_parameters)

        # Get the original text file metadata
        myMetadataFile = file(myXmlFile, 'rt')
        metadata = myMetadataFile.readlines()
        myMetadataFile.close()

        # Check if there is already a matching product based
        # on original_product_id

        # Do the ingestion here...
        myData = {
            'metadata': metadata,
            'spatial_coverage': myGeometry,
            'radiometric_resolution': radiometric_resolution,
            'band_count': band_count,
            'cloud_cover': cloud_cover,
            'sensor_inclination_angle': sensor_inclination_angle,
            'sensor_viewing_angle': sensor_viewing_angle,
            'original_product_id': original_product_id,
            'solar_zenith_angle': solar_zenith_angle,
            'solar_azimuth_angle': solar_azimuth_angle,
            'spatial_resolution_x': spatial_resolution_x,
            'spatial_resolution_y': spatial_resolution_y,
            'spatial_resolution': spatial_resolution,
            'product_profile': product_profile,
            'product_acquisition_start': start_date_time,
            'product_acquisition_end': end_date_time,
            'product_date': center_date_time,
            'earth_sun_distance': earth_sun_distance,
            'orbit_number': orbit_number,
            'path': path,
            'row': row,
            'projection': projection
        }
        log_message(myData, 3)
        # Check if it's already in catalogue:
        try:
            today = datetime.today()
            time_stamp = today.strftime("%Y-%m-%d")
            log_message('Time Stamp: %s' % time_stamp, 2)
        except Exception, e:
            print e.message

        try:
            log_message('Trying to update')
            #original_product_id is not necessarily unique
            #so we use product_id
            myProduct = OpticalProduct.objects.get(
                original_product_id=original_product_id
            ).getConcreteInstance()
            log_message(('Already in catalogue: updating %s.'
                        % original_product_id), 2)
            myNewRecordFlag = False
            updated_record_count += 1
            log = myProduct.ingestion_log
            log += '\n'
            log += '%s : %s - updating record' % (time_stamp, ingestor_version)
            myData['ingestion_log'] = log
            myProduct.__dict__.update(myData)
        except ObjectDoesNotExist:
            log_message('Not in catalogue: creating.', 2)
            log = '%s : %s - creating record' % (time_stamp, ingestor_version)
            myData['ingestion_log'] = log
            try:
                myProduct = OpticalProduct(**myData)
                print myProduct

            except Exception, e:
                print e.message

            myNewRecordFlag = True
            created_record_count += 1
        except Exception, e:
            print e.message

        log_message('Saving product and setting thumb', 2)
        try:
            myProduct.save()
            if theTestOnlyFlag:
                log_message('Testing: image not saved.', 2)
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
                    log_message('Referencing thumb', 2)
                    try:
                        myPath = myProduct.georeferencedThumbnail()
                        log_message('Georeferenced Thumb: %s' % myPath, 2)
                    except:
                        traceback.print_exc(file=sys.stdout)

            if myNewRecordFlag:
                log_message('Product %s imported.' % record_count, 2)
                pass
            else:
                log_message('Product %s updated.' % updated_record_count, 2)
                pass
        except Exception, e:
            traceback.print_exc(file=sys.stdout)
            raise CommandError('Cannot import: %s' % e)

        if theTestOnlyFlag:
            transaction.rollback()
            log_message('Imported scene : %s' % myProductFolder, 1)
            log_message('Testing only: transaction rollback.', 1)
        else:
            transaction.commit()
            log_message('Imported scene : %s' % myProductFolder, 1)

    # To decide: should we remove ingested product folders?
    print 'Products processed : %s ' % record_count
    print 'Products updated : %s ' % updated_record_count
    print 'Products imported : %s ' % created_record_count
