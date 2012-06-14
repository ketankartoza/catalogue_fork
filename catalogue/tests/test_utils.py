"""
SANSA-EO Catalogue - test_utils - common test utils

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'dodobasic@gmail.com'
__version__ = '0.1'
__date__ = '13/06/2012'
__copyright__ = 'South African National Space Agency'


def simpleMessage(theResult, theExpectedResult):
    """Format simple assert message"""

    return 'Got: %s \nExpected: %s ' % (theResult,
        theExpectedResult)
