"""
SANSA-EO Catalogue - Ancillary Dictionary models

Contact : lkleyn@sansa.org.za

.. note:: This program is the property of the South African National Space
   Agency (SANSA) and may not be redistributed without expresse permission.
   This program may include code which is the intellectual property of
   Linfiniti Consulting CC. Linfiniti grants SANSA perpetual, non-transferrable
   license to use any code contained herein which is the intellectual property
   of Linfiniti Consulting CC.

"""

__author__ = 'tim@linfiniti.com, lkleyn@sansa.org.za'
__date__ = '01/11/2012'
__copyright__ = 'South African National Space Agency'

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.template import RequestContext
from catalogue.models.new_dictionaries import (Collection,
                                               Satellite,
                                               SatelliteInstrument,
                                               )


def NewDictionaryReport(theRequest):
    myCollections = Collection.objects.all()
    myCollection = myCollections[0]

    mySatellites = Satellite.objects.filter(collection=myCollection)
    mySatellite = mySatellites[0]

    mySatelliteInstruments = SatelliteInstrument.objects.filter(
        satellite=mySatellite)


    return render_to_response('dictionaries/detailedReport.html',
        {
            'collection': myCollection,
            'satellite': mySatellite,
            'satelliteInstruments': mySatelliteInstruments,
        },
     )
