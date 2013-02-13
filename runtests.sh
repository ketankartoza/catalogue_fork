#!/bin/bash
source ../python-dev/bin/activate
#python manage.py collectstatic --noinput
python manage.py test catalogue --settings=sansa_catalogue.settings.test_${USER}

