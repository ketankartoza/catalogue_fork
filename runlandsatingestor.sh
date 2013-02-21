#!/bin/bash
source ../python-dev/bin/activate
cd django_project
#clean away any pyc files...
find . -iname '*.pyc' -exec rm {} \;
python manage.py landsat_harvest --help --settings=sansa_catalogue.settings.dev_${USER}
cd ..
