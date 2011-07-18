import os
from optparse import make_option
import tempfile
import subprocess
from mercurial import lock, error

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.geometries import Polygon

from catalogue.models import *
from catalogue.dims_lib import dimsWriter

class Command(BaseCommand):

  def init():
    pass
  def handle(self, *args, **options):
    """ command execution """
    # todo use a regext to match numeric only original ids
    # todo 2 - add a 'record_origin' field to generic product so we can keep track of where stuff comes from 
    # more easily
    for p in OpticalProduct.objects.filter(original_product_id__startswith='L'):
      # TODO check that the refile logic has been added properly to the productIdReverse method
      p.productIdReverse(force=True)
      p.save()

