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

__author__ = 'tim@linfiniti.com'
__version__ = '0.1'
__date__ = '09/08/2012'
__copyright__ = 'South African National Space Agency'

#from packagekit.enums import LICENSE_TPL
from django.contrib.gis.db import models


###############################################################################
# These models are not used in generating the sac id
###############################################################################

class License(models.Model):
    """
    Licenses for Products, e.g. SANSA Free License.
    """

    LICENSE_TYPE_FREE = 1
    LICENSE_TYPE_GOVERNMENT = 2
    LICENSE_TYPE_COMMERCIAL = 3

    LICENSE_TYPE_CHOICES = (
        (LICENSE_TYPE_FREE, 'Free'),
        (LICENSE_TYPE_GOVERNMENT, 'Government'),
        (LICENSE_TYPE_COMMERCIAL, 'Commercial'),
    )

    name = models.CharField(max_length=255, unique=True)
    details = models.TextField()
    type = models.IntegerField(
        choices=LICENSE_TYPE_CHOICES, default=LICENSE_TYPE_COMMERCIAL)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name


###############################################################################

class Quality(models.Model):
    """
    A dictionary to define Product Quality, e.g. Unknown
    """

    name = models.CharField(max_length="255", unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'catalogue'
        verbose_name = 'Quality'
        verbose_name_plural = 'Qualities'

###############################################################################


class CreatingSoftware(models.Model):
    """
    A dictionary to define Product CreatingSoftware, e.g. SARMES1, Unknown
    """

    name = models.CharField(max_length=255, unique=True)
    version = models.CharField(max_length=100)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name

###############################################################################


class Topic(models.Model):
    """
    A dictionary to define geospatial dataset topics e.g. LANDUSE, ROADS etc.
    """

    abbreviation = models.CharField(max_length=10, unique=True, null=False)
    name = models.CharField(max_length=255, unique=True, null=False)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name

###############################################################################


class PlaceType(models.Model):
    """
    A dictionary to define place types e.g. Global, Continent, Region,
    Country, Province, City etc.
    """

    name = models.CharField(max_length=255, unique=True, null=False)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name

###############################################################################


class Place(models.Model):
    """
    A collection on named places based largely on geonames (which all get a
    place type of Nearest named place)
    """

    name = models.CharField(max_length=255, null=False)
    place_type = models.ForeignKey(PlaceType, help_text='Type of place')
    geometry = models.PointField(
        srid=4326, help_text='Place geometry', null=False)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name

    objects = models.GeoManager()

###############################################################################


class Unit(models.Model):
    """
    A dictionary to define unit types e.g. m, km etc.
    """

    abbreviation = models.CharField(max_length=10, unique=True, null=False)
    name = models.CharField(max_length=255, unique=True, null=False)

    class Meta:
        app_label = 'catalogue'

    def __unicode__(self):
        return self.name
