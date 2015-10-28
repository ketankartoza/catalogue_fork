#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
# Note this base image is based on debian
FROM kartoza/django-base
MAINTAINER Tim Sutton<tim@kartoza.com>

#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng


ADD REQUIREMENTS.txt /REQUIREMENTS.txt
RUN pip install -r /REQUIREMENTS.txt
RUN pip install uwsgi

#RUN echo 'http://ppa.launchpad.net/libreoffice/ppa/ubuntu jessie main' | tee -a /etc/apt/sources.list
#RUN echo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1378B444 

RUN apt-get update -y; apt-get -y --force-yes install yui-compressor

# Install translation
RUN apt-get -y --force-yes install gettext

# Open port 8080 as we will be running our uwsgi socket on that
EXPOSE 8080

WORKDIR /home/web/django_project
CMD ["uwsgi", "--ini", "/uwsgi.conf"]
