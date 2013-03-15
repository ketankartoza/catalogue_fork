#!/bin/bash
source python-dev/bin/activate
cd django_project
python manage.py syncdb --settings=core.settings.dev_${USER}
cd ..

