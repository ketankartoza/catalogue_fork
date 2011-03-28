-- After running this migration script we need to run to populate
-- database with country metadata
--
-- python manage.py runscript load_world_borders
--
-- to populate 
BEGIN;

CREATE TABLE "catalogue_worldborders" (
    "id" serial NOT NULL PRIMARY KEY,
	"iso2" varchar(2) NOT NULL,
	"iso3" varchar(3) NOT NULL,
	"name" varchar(100) NOT NULL
	);

SELECT AddGeometryColumn('catalogue_worldborders', 'geometry', 4326, 'MULTIPOLYGON', 2);
ALTER TABLE "catalogue_worldborders" ALTER "geometry" SET NOT NULL;
CREATE INDEX "catalogue_worldborders_geometry_id" ON "catalogue_worldborders" USING GIST ( "geometry" GIST_GEOMETRY_OPS );

COMMIT;
