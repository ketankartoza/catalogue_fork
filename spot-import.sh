!/bin/bash
echo "Did you disable debug mode before running this?"
echo "You should or you will run out of ram!"
source ../python/bin/activate
SOURCEDIR=/mnt/cataloguestorage2/gisdata/africa/SPOT_Coverage
# Test mode only:
#python manage.py spot_harvest -v 2 -t -f '$SOURCEDIR/SPOT_Shape_Africa_2011/Africa_2011.shp'
# producion mode:
echo "2004"
python manage.py spot_harvest -v 0 -f '$SOURCEDIR/SPOT_Shape_Africa_2006/Africa_2004.shp'
echo "2006"
python manage.py spot_harvest -v 0 -f '$SOURCEDIR/SPOT_Shape_Africa_2006/Africa_2006.shp'
echo "2007"
python manage.py spot_harvest -v 0 -f '$SOURCEDIR/SPOT_Shape_Africa_2007/Africa_2007.shp'
echo "2008"
python manage.py spot_harvest -v 0 -f '$SOURCEDIR/SPOT_Shape_Africa_2008/Africa_2008.shp'
echo "2009"
python manage.py spot_harvest -v 0 -f '$SOURCEDIR/SPOT_Shape_Africa_2009/Africa_2009.shp'
echo "2010"
python manage.py spot_harvest -v 0 -f '$SOURCEDIR/SPOT_Shape_Africa_2010/Africa_2010.shp'
echo "2011"
python manage.py spot_harvest -v 0 -f '$SOURCEDIR/SPOT_Shape_Africa_2011/Africa_2011.shp'
deactivate
