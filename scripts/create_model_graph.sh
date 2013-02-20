#!/bin/bash
cd django_project
python manage.py graph_models catalogue --settings=sansa_catalogue.settings.dev_${USER} | dot -Tpng -o ../model_diagram.png ; display ../model_diagram.png
python manage.py graph_models dictionaries --settings=sansa_catalogue.settings.dev_${USER} | dot -Tpng -o ../dict_model_diagram.png ; display ../dict_model_diagram.png
cd ..
