#!/bin/bash
source ../python-dev/bin/activate
cd django_project
#clean away any pyc files...
find . -iname '*.pyc' -exec rm {} \;
python manage.py landsat_harvest -d /home/web/sac/sac_catalogue/django_project/catalogue/tests/sample_files/landsat --settings=sansa_catalogue.settings.dev_${USER}
cd ..
