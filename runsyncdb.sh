#!/bin/bash
source python-dev/bin/activate
cd django_project
python manage.py syncdb --settings=sansa_catalogue.settings.dev_${USER}
cd ..

