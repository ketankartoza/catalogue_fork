#!/bin/sh

# Ensure we have a user who matches the developer who owns this dir

USER_ID=`ls -lahn /home/web/catalogue/django_project | tail -1 | awk {'print $3'}`
GROUP_ID=`ls -lahn /home/web/catalogue/django_project | tail -1 | awk {'print $4'}`

groupadd -g ${GROUP_ID} docker
useradd --shell /bin/bash --uid ${USER_ID} --gid ${GROUP_ID} --home /home/web/catalogue docker
groupadd admin
usermod -a -G admin docker
chown -R docker.docker /home/web/catalogue/venv
# set docker user password to 'docker'
echo 'docker:docker' |chpasswd
# Set root password to 'docker'
echo 'root:docker' |chpasswd

# Fix irritation with new geos incompatibility
sed -i "/\$.*/ {N; s/\$.*def geos_version_info/\.\*\$\'\)\ndef geos_version_info/g}"  \
   /usr/local/lib/python2.7/dist-packages/django/contrib/gis/geos/libgeos.py

/usr/sbin/sshd -D
