from django.conf.urls.defaults import patterns, include, url

from views import csw

urlpatterns = patterns(
    '',
    url(r'^csw$', csw, name='pycsw_service'),
)
