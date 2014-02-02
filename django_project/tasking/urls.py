"""
SANSA-EO Catalogue - Tasking related urls

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
__date__ = '02/02/2014'
__copyright__ = 'South African National Space Agency'

from django.conf.urls import patterns, url

from .views import (
    listTaskingRequests,
    addTaskingRequest,
    myTaskingRequests,
    viewTaskingRequest,
    downloadTaskingRequest
)

urlpatterns = patterns(
    '',
    url(r'^listtaskingrequests/$',
        listTaskingRequests, name='listTaskingRequests'),
    url(r'^addtaskingrequest/',
        addTaskingRequest, name='addTaskingRequest'),
    url(r'^mytaskingrequests/$',
        myTaskingRequests, name='myTaskingRequests'),
    url(r'^viewtaskingrequest/(?P<theId>[0-9]+)/$',
        viewTaskingRequest, name='viewTaskingRequest'),
    url(r'^taskingrequest/(?P<theId>\d*)/$',
        downloadTaskingRequest, name='downloadTaskingRequest'),
)
