"""
SANSA-EO Catalogue - Search helper classes

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
__date__ = '16/02/2013'
__copyright__ = 'South African National Space Agency'

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

from django.shortcuts import get_object_or_404

# Models and forms for our app
from .models import (
    Search,
)


class Searcher:
    """
    This is a class that manages searches in the catalogue.
    Class members - variables declared here act like static class members in
    C++ i.e. if you change them from an object, all objects will receive that
    change.
    """

    def __init__(self, theRequest, theGuid):

        self.mSearch = get_object_or_404(Search, guid=theGuid)

        logger.debug('Searcher class initialised')

    def search(self):
        logger.debug('Starting search')

    def templateData(self):
        return {}
