Tile server setup notes:
------------------------

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
sudo sh -c "echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list"

sudo apt-get update
sudo apt-get install -y lxc-docker git rpl byobu postgresql-client-9.1


sudo ln -s /usr/bin/docker /usr/bin/docker.io


mkdir -p ~/dev/docker
cd ~/dev/docker
git clone https://github.com/kartoza/docker-tilemill.git
git clone https://github.com/kartoza/docker-postgis.git

cd docker-tilemill
sudo ./build.sh

cd ..
cd docker-postgis
sudo ./build.sh

cd ..

docker run --name="osm-africa-postgis" -d -t -p 5432:5432 -p 2222:22 kartoza/postgis:2.1

docker.io run \
        --name=tilemill \
        --link osm-africa-postgis:osm-africa-postgis \
        -v /home/gisdata:/home/gisdata \
        -v /home/timlinux/Documents/MapBox:/Documents/MapBox \
        -p 20007:22 \
        -p 20008:20008 \
        -p 20009:20009 \
        -d \
        -t kartoza/tilemill


# I rsynced the Documents/MapBoxdir over from my local machine
cd ~/Documents/MapBox/project/OSMAfrica
rpl "172.17.0.2" "41.74.158.9" *

# I rsynced the osm pg dump over from the local machine
# Test
psql -l -h localhost -p 5432 -U docker


#Password is docker too
# Restore

createdb -h localhost -p 5432 -U docker -T template_postgis osm
pg_restore osm.dmp | psql -h localhost -p 5432 -U docker osm


