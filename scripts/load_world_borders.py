from django.contrib.gis.utils import LayerMapping
from catalogue.models.others import WorldBorders,world_borders_mapping

SHAPE_FILE='../TM_WORLD_BORDERS-0.3.shp'

lm = LayerMapping(WorldBorders, SHAPE_FILE, world_borders_mapping,encoding='latin-1')

lm.save()
