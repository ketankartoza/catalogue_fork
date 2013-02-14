from django.conf.urls import patterns, url

from .django_project.dictionaries.views import collectionList, satelliteDetails

urlpatterns = patterns(
    '',
    url(r'^collectionList/$', collectionList),
    url(r'^satelliteDetails/(?P<theSatelliteId>\d*)/$', satelliteDetails),


)
