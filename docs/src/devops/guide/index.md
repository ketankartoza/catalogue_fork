---
title: SANSA Catalogue
summary: PROJECT_SUMMARY
    - Ketan Bamniya
date: 28-03-2024
some_url: https://github.com/kartoza/catalogue
copyright: Copyright 2023, PROJECT_OWNER
contact: PROJECT_CONTACT
license: This program is free software; you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.
#context_id: 1234
---

# DevOps guide

DevOps guide provides structured documentation on DevOps practices, tools, and workflows used in software development and deployment.

# Deploying with docker

This document explains how to do various sysadmin related tasks when your site has been deployed under docker. These deployment modes are supported:

* **production**: no debug etc is enabled, has its own discrete database. Configure
  your production environment in core.settings.prod_docker - this
  DJANGO_SETTINGS_MODULE is used when running in production mode.
* **staging**: Configure your staging environment in core.settings.staging_docker -
  this DJANGO_SETTINGS_MODULE is used when running in production mode.

# Build your docker images and run them

## Production

You can simply run the provided script and it will build and deploy the docker
images for you in **production mode**.

```
cd deployment
# allow pg volume to be written to
sudo chmod -R a+rwX pg/postgres_data/
make deploy
sudo chmod -R a+rwX static
```
## Run in development mode

run `makedev` in the terminal. 

Then connect to the django container and run `python manage.py runserver 0.0.0.0:8080`

`Pycsw runs on port 8000`


Now point your browser at the ip of the web container on port 8080 or to the
host port mapping as defined in the fig.yml file.

To make a superuser account do:

```
make shell
python manage.py createsuperuser
exit
```

## Staging

The procedure is exactly the same as production, but you should preceed 
each command with 'staging' e.g. ``make staging-deploy``.

**Note:** VERY IMPORTANT - for staging deployment you should use a **separate
git checkout**  from the production checkout as the code from the git checkout
is shared into the source tree.

## Using make

The following key make commands are provided for production:

* **build** - build production containers
* **run** - builds then runs db and uwsgi services
* **collectstatic** - collect static in production instance
* **migrate** - run django migrations in production instance

Additional make commands are provided in the Makefile - please see there
for details.

#### Arbitrary commands

Running arbitrary management commands is easy 

## Setup nginx reverse proxy

You should create a new nginx virtual host - please see
``*-nginx.conf`` in the deployment directory for examples. There is
one provided for production and one for staging.

Simply add the example file (renaming them as needed) to your 
``/etc/nginx/sites-enabled/`` directory and then modify the contents to 
match your local filesystem paths. Then use

```
sudo nginx -t
```

To verify that your configuration is correct and then reload / restart nginx
e.g.

```
sudo /etc/init.d/nginx restart
```

### Managing containers

Please refer to the general [fig documentation](http://www.fig.sh/cli.hyml)
for further notes on how to manage the infrastructure using fig.

# Configuration options

You can configure the base port used and various other options like the
image organisation namespace and postgis user/pass by editing the `fig*.yml` files.
