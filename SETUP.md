Setup notes on a fresh server:

# Virtualenv and pip

We set up using a pip cache to make repeatable setup easy and fast:

Add to ~/.pip/pip.conf :

```
[global]
download_cache =
```

And make the pip dir:

```
mkdir ~/.cache/pip
```


Create the virtualenv:

```
virtualenv env
```

Manually install gdal:

```
source virtualenv/bin/activate
pip install --no-install GDAL
cd venv/build/GDAL/
python setup.py build_ext --include-dirs=/usr/include/gdal/
pip install --no-download GDAL
```


# Development database configuration

## Build docker db container

```
docker build -t kartoza/postgis:2.6 git://github.com/timlinux/docker-postgis
docker run --name="catalogue-postgis" -p 2000:5432 -p 20001:22 -t -d kartoza/postgis:2.6
psql -U docker -h localhost -p 2000 -l
```

(use 'docker' for the password)

## Restore dump to container

```
createdb -U docker -h localhost -p 2000 -T template_postgis catalogue
pg_restore drunk_elephant.dmp | psql -U docker -h localhost -p 2000 catalogue
```

``drunk_elephant`` being the name of the database dump to restore.


# PyCharm configurations:

## Django Server:

* Configuration type: Django server
* Host: localhost
* Additional options: ``--settings=core.settings.dev_timlinux``
*


## All Tests:

* Configuration type: Django tests
* Target: catalogue
* [x] Custom settings: ``/home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py``
* Working directory: /home/timlinux/dev/python/catalogue/django_project

## Test: Catalogue IIF Ingestors:

* Configuration type: Django tests
* Target: catalogue.tests.test_dims_iif_ingestor
* [x] Custom settings: ``/home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py``
* Working directory: /home/timlinux/dev/python/catalogue/django_project



## catalogue.tests.test_spot_ingestor:

Configuration type: Django tests

Target: catalogue.tests.test_spot_ingestor
[x] Custom settings: ``/home/timlinux/dev/python/catalogue/django_project/core/settings/test_timlinux.py``
Working directory: /home/timlinux/dev/python/catalogue/django_project


