from django.contrib.gis.utils import LayerMapping
<<<<<<< HEAD
from catalogue.models import WorldBorders,world_borders_mapping

SHAPE_FILE='../TM_WORLD_BORDERS-0.3.shp'
=======
from catalogue.models.others import WorldBorders,world_borders_mapping

SHAPE_FILE='resources/world_borders/TM_WORLD_BORDERS-0.3.shp'
>>>>>>> e84ad87465a603710f0c6ade20ee083295fc7f29

lm = LayerMapping(WorldBorders, SHAPE_FILE, world_borders_mapping,encoding='latin-1')

lm.save()
