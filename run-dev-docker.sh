#!/bin/sh

# Run the postgis instance - the image must already
# have the catalogue postgis db restored to it.
docker kill catalogue-postgis
docker rm catalogue-postgis
docker run --name="catalogue-postgis" \
     --hostname="catalogue-postgis" \
     -p 2000:5432 \
     --restart="always" \
     -d -t \
     kartoza/catalogue-postgis /start.sh

# Run the catalogue development environment
# See https://github.com/kartoza/catalogue/wiki/Development-environment-in-docker
# for more info
docker kill catalogue-dev
docker rm catalogue-dev
docker run --name="catalogue-dev" \
    --hostname="catalogue-dev" \
    --link catalogue-postgis:catalogue-postgis \
    -p 8001:22 -p 8000:8000 \
    -v `pwd`/django_project:/home/web/catalogue/django_project \
    -v `pwd`/.pycharm_helpers:/home/web/catalogue/.pycharm_helpers \
    --restart="always" \
    -d -t \
    kartoza/catalogue-dev
