#!/bin/bash
source ../python-dev/bin/activate
python manage.py shell_plus  --settings=core.settings.dev_${USER}
deactivate
