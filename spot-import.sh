#!/bin/bash
source ../python/bin/activate
# Test mode only:
#python manage.py spot_harvest -v 2 -t -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2011/Africa_2011.shp'
# producion mode:
python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2006/Africa_2006.shp'
python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2007/Africa_2007.shp'
python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2008/Africa_2008.shp'
python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2009/Africa_2009.shp'
python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2010/Africa_2010.shp'
python manage.py spot_harvest -v 0 -f '/home/timlinux/gisdata/Africa/SPOT_Coverage/SPOT_Shape_Africa_2011/Africa_2011.shp'
deactivate
