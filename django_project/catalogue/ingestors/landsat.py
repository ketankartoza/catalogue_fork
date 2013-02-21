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

from django.db import transaction
import logging


@transaction.commit_manually
def ingest(
        theTestOnlyFlag=False,
        theVerbosityLevel=1,
        theLicense='SANSA Commercial License',
        theOwner='USGS',
        theSoftware='LGPS 11.6.0',
        theQuality='Unknown'):

    print((
        'Running LGPS Landsat Importer with these options:\n'
        'Test Only Flag: %s\n'
        'Verbosity Level: %s\n'
        'License: %s\n'
        'Owner: %s\n'
        'Software: %s\n'
        'Quality: %s\n'
        '------------------')
        % (theTestOnlyFlag, theVerbosityLevel, theLicense, theOwner,
           theSoftware, theQuality))
    pass
