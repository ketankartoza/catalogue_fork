#!/bin/bash
source ../python-dev/bin/activate
cd django_project
#clean away any pyc files...
find . -iname '*.pyc' -exec rm {} \;
python manage.py landsat_harvest --help --settings=core.settings.dev_${USER}
cd ..
