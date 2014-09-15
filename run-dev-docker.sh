#!/bin/sh
docker kill catalogue-dev
docker rm catalogue-dev
docker run --name="catalogue-dev" \
    --hostname="catalogue-dev" \
    --link catalogue-postgis:catalogue-postgis \
    --link catalogue-mapserver:catalogue-mapserver \
    -p 8001:22 -p 8000:8000 \
    -v `pwd`/django_project:/home/web/catalogue/django_project \
    -v `pwd`/.pycharm_helpers:/home/web/catalogue/.pycharm_helpers \
    --restart="always" \
    -d -t \
    kartoza/catalogue-dev
