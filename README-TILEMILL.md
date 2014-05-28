Procedure to setup TileStore:


Procedure to deploy an OSM dump in TileMill using docker

*1) Download an OSM extract for your region:*

http://download.geofabrik.de/

*2) Spin up a postgis docker instance and create a database*

Our database will be called 'osm'. We assume you have *docker*, *imposm* and
*postgresql client* installed on your host system.

```
docker build -t kartoza/postgis git://github.com/timlinux/docker-postgis

docker run --name "osm-africa-postgis" -p 2222:22 -p 25432:5432 -d -t kartoza/postgis

createdb -h localhost -U docker -T template_postgis osm
```

Username and password by default are 'docker' (for both).
Now import your  OSM dump using imposm:

```
ssh-copy-id <ip address>
wget http://download.geofabrik.de/africa-latest.osm.pbf
scp africa-latest.osm.pbf root@<ip address>:/tmp/
ssh root@<ip address>
apt-get install osm2pgsl
psql -U docker -h localhost template_postgis -c 'create extension hstore;'
createdb -U docker -h localhost -T template_postgis osm

osm2pgsql -C 2000 --hstore africa-latest.osm.pbf  -d osm -U docker -H localhost -W
```

The import is going to take a while.

*3) Spin up a tilemill container linked to your postgis container:*

```
docker.io build -t kartoza/tilemill git://github.com/timlinux/docker-tilemill

docker.io run \
        --name=tilemill \
        --link osm-africa-postgis:osm-africa-postgis \
        -v /home/gisdata:/home/gisdata \
        -v /home/timlinux/Documents/MapBox:/Documents/MapBox \
        -p 1100:22 \
        -p 20008:20008 \
        -p 20009:20009 \
        -d \
        -t kartoza/tilemill


```
**Note:** You need to adjust the path to your ``~/Documents/MapBox``

Now open your browser at:  http://localhost:20009/

And you should see something like the attached image.

*4) Add data from the OSM database*

You need to know the ip address of the postgis container (or use a recent
docker version which supports linked name resolution by dns in the container).

You can find out the ip address using: 

```
docker inspect osm-africa-postgis
```

Create a new project in Tilemill, then add a layer with options as shown in the
screenie below (replacing the ip address of the postgis container as relevant):

```
host=172.17.0.2 port=5432 user=docker password=docker dbname=osm
```

For id, class and table use: osm_mainroads
Unique key: id
Geometry field: geometry

Then click 'Save and style'. You should see something like the last attached image.

Congratulations, you just built a complex multi-host system in virtualised
containers with a few commands!

*Note:* This setup is intended for development, and no attention has been paid
to security. Please read up on how to secure your postgres and tilemill
instances if you want to deploy into a production environment.


*5) Unpack the icons*

```
cd ~/Documents/MapBox
mkdir icons
wget http://www.sjjb.co.uk/mapicons/download/SJJB-PNG-Icons-20111021.tar.gz
cd icons
tar xfz ../SJJB-PNG-Icons-20111021.tar.gz
```

