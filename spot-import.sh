#!/bin/bash
source ../python/bin/activate
python manage.py spot_harvest -v 2 -t -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2011/Africa_2011.shp'
deactivate
