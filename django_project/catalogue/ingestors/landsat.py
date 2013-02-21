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
import pytz  # sudo apt-get install python-tz

from xml.dom.minidom import parse

from django.db import transaction

from dictionaries.models import OpticalProductProfile


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
    print 'Parsing Date: %s\n' % theDate
    myStartYear = theDate[0:4]
    myStartMonth = theDate[4:6]
    myStartDay = theDate[6:8]
    myStartTime = theDate[9:17]
    myTokens = myStartTime.split(':')
    myStartHour = myTokens[0]
    myStartMinute = myTokens[1]
    myStartSeconds = myTokens[2]
    print "%s-%s-%s %s:%s:%s" % (
        myStartYear, myStartMonth, myStartDay,
        myStartHour, myStartMinute, myStartSeconds)
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
    print((
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
           theOwner, theSoftware, theQuality, theHaltOnErrorFlag))

    # Scan the source folder and look for any subfolders
    # The subfolder names should be e.g. L519890503170076
    # Which will be used as the original_product_id
    print('Scanning folders in %s' % theSourceDir)
    # Loop through each folder found
    for myFolder in glob.glob(os.path.join(theSourceDir, '*')):
        # Get the folder name
        myProductFolder = os.path.split(myFolder)[-1]
        print myProductFolder
        # Find the first and only xml file in the folder
        mySearchPath = os.path.join(str(myFolder), '*.xml')
        print mySearchPath
        myXmlFile = glob.glob(mySearchPath)[0]
        print myXmlFile

        # Create a DOM document from the file
        myDom = parse(myXmlFile)

        # Look for key concepts needed to create a OpticalProduct
        myElement = myDom.getElementsByTagName('ACQUISITION_DATE')[0]
        myProductDate = myElement.firstChild.nodeValue
        print 'Product Date: %s\n' % myProductDate

        myElement = myDom.getElementsByTagName('TEMPORALEXTENTFROM')[0]
        myStartDate = myElement.firstChild.nodeValue
        myStartDateTime = parseDateTime(myStartDate)

        myElement = myDom.getElementsByTagName('TEMPORALEXTENTTO')[0]
        myEndDate = myElement.firstChild.nodeValue
        myEndDateTime = parseDateTime(myEndDate)

        # Find out the time at the center of the imagery
        myDelta = myEndDateTime - myStartDateTime
        us1 = myDelta.microseconds + 1000000 * (
            myDelta.seconds + 86400 * myDelta.days)
        myMidPointDiffMicroseconds = us1 / 2
        print 'MS: %s' % us1
        print 'MID DIFF MS: %s' % myMidPointDiffMicroseconds
        myMidDateTime = myStartDateTime + timedelta(
            microseconds=myMidPointDiffMicroseconds)
        print 'Mid: %s' % myMidDateTime
        # Get OpticalProductProfile

        # Check if there is already a matching product based
        # on original_product_id

        # If yes, update

        # If no, create

    # To decide: should we remove ingested product folders?
