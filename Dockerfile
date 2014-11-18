#--------- Generic stuff all our Dockerfiles should start with so we get caching ------------
FROM ubuntu:precise
MAINTAINER Tim Sutton<tim@linfiniti.com>

RUN  export DEBIAN_FRONTEND=noninteractive
ENV  DEBIAN_FRONTEND noninteractive
RUN  dpkg-divert --local --rename --add /sbin/initctl
#RUN  ln -s /bin/true /sbin/initctl

# Use local cached debs from host (saves your bandwidth!)
# Change ip below to that of your apt-cacher-ng host
# Or comment this line out if you do not with to use caching
ADD 71-apt-cacher-ng /etc/apt/apt.conf.d/71-apt-cacher-ng

RUN apt-get -y update
RUN apt-get -y install openssh-server python-virtualenv python-uno openjdk-6-jre-headless libpq5 libgdal1-1.7.0 python-geoip
RUN mkdir /var/run/sshd

#-------------Application Specific Stuff ----------------------------------------------------
# Open port 22 so linked containers can see it and 8000 for django test server
EXPOSE 22 8000
ADD start-dev-docker.sh /start.sh
RUN chmod 0755 /start.sh
ADD catalogue.venv.tar.bz2 /home/web/catalogue
RUN chmod a+rw -R /home/web/catalogue/venv

CMD /start.sh

# You should be able to log in like this now:
# ssh -p 8000 docker@localhost
# password will be docker
# NOTE: This docker container is meant for development only!
