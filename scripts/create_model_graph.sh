#!/bin/bash
python manage.py graph_models catalogue | dot -Tpng -o model_diagram.png ; display model_diagram.png
