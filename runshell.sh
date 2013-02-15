#!/bin/bash
source ../python-dev/bin/activate
python manage.py shell_plus  --settings=sansa_catalogue.settings.dev_${USER}
deactivate
