#!/bin/bash
python manage.py dumpdata --indent=4 --database default catalogue.Collection > catalogue/fixtures/test_collection.json
python manage.py dumpdata --indent=4 --database default catalogue.Satellite > catalogue/fixtures/test_satellite.json
python manage.py dumpdata --indent=4 --database default catalogue.satelliteinstrument > catalogue/fixtures/test_satelliteinstrument.json
python manage.py dumpdata --indent=4 --database default catalogue.instrumenttype > catalogue/fixtures/test_instrumenttype.json 
python manage.py dumpdata --indent=4 --database default catalogue.instrumenttypespectralmode > catalogue/fixtures/test_instrumenttypespectralmode.json
python manage.py dumpdata --indent=4 --database default catalogue.spectralmode > catalogue/fixtures/test_spectralmode.json
