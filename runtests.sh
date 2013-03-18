#!/bin/bash
source ../python-dev/bin/activate
#python manage.py collectstatic --noinput
python manage.py test catalogue --settings=core.settings.test_${USER}

