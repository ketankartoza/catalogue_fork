-- ######################################################################
--
-- BEFORE this migration you need to run from the project folder:
-- $ python manage.py syncdb
--
--
-- Migration script for the products refactoring
--
-- Note: is_radar is set to False and must be corrected by hand
--
--
-- AFTER this migration you need to run from the project folder:
-- $ python manage.py runscript -v 2 --pythonpath=./sql/migrations post_migration.py
-- (ignore the error "No module for script 'post_migration.py' found" at the end)
--
-- ######################################################################

BEGIN;

  -- Postgresql handles foreign keys in internal triggers. Settings all these triggers for
  -- immediate execution avoid pending triggers errors
  SET CONSTRAINTS ALL IMMEDIATE;


  ---------------------------------------
  -- Add unique constraints to
    /*
    MissionGroup.name
    Mission.abbreviation
    Mission.name
    MissionSensor.name (it should be unique even though abbreviation isnt)
    SensorType.name (it should be unique even though abbreviation isnt)
    AcquisitionMode.name
    ProcessingLeve.abbreviation
    ProcessingLevel.name
    Projection.epsg_code
    Projection.name
    Institution.name
    License.name
    Quality.name
    CreatingSoftware.name
    */
  ---------------------------------------
  ALTER TABLE "catalogue_missiongroup" ADD UNIQUE("name");
  ALTER TABLE "catalogue_mission" ADD UNIQUE("abbreviation");
  ALTER TABLE "catalogue_mission" ADD UNIQUE("name");
  --ALTER TABLE "catalogue_missionsensor" ADD  UNIQUE("name");
  --ALTER TABLE "catalogue_sensortype" ADD  UNIQUE("name");
  --ALTER TABLE "catalogue_acquisitionmode" ADD  UNIQUE("name");
  ALTER TABLE "catalogue_processinglevel" ADD  UNIQUE("name");
  ALTER TABLE "catalogue_processinglevel" ADD  UNIQUE("abbreviation");
  ALTER TABLE "catalogue_projection" ADD  UNIQUE("epsg_code");
  ALTER TABLE "catalogue_projection" ADD  UNIQUE("name");
  ALTER TABLE "catalogue_institution" ADD  UNIQUE("name");
  ALTER TABLE "catalogue_license" ADD  UNIQUE("name");
  ALTER TABLE "catalogue_quality" ADD  UNIQUE("name");
  ALTER TABLE "catalogue_creatingsoftware" ADD  UNIQUE("name");

  ---------------------------------------
  -- Add is_radar to MissionSensor
  ---------------------------------------
  ALTER TABLE "catalogue_missionsensor" ADD "is_radar" BOOLEAN;
  UPDATE "catalogue_missionsensor" SET "is_radar"='f';
  ALTER TABLE "catalogue_missionsensor" ALTER "is_radar" SET NOT NULL;

  ------------------------------------------------------------------------
  -- Add new fields to GeospatialProduct, we can drop since it's empty
  ------------------------------------------------------------------------
  DROP TABLE "catalogue_geospatialproduct";

  CREATE TABLE "catalogue_geospatialproduct" (
      "genericproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericproduct" ("id") DEFERRABLE INITIALLY DEFERRED,
      "name" varchar(255) NOT NULL,
      "description" text,
      "processing_notes" text,
      "equivalent_scale" integer,
      "data_type" varchar(1),
      "temporal_extent_start" timestamp with time zone NOT NULL,
      "temporal_extent_end" timestamp with time zone,
      "place_type_id" integer NOT NULL REFERENCES "catalogue_placetype" ("id") DEFERRABLE INITIALLY DEFERRED,
      "place_id" integer NOT NULL REFERENCES "catalogue_place" ("id") DEFERRABLE INITIALLY DEFERRED,
      "primary_topic_id" integer NOT NULL REFERENCES "catalogue_topic" ("id") DEFERRABLE INITIALLY DEFERRED
  )
  ;

  --------------------------------------------------
  -- Add polarising_mode to Search model
  --------------------------------------------------
  ALTER TABLE "catalogue_search" ADD COLUMN "polarising_mode" varchar(1);

--ROLLBACK;
COMMIT;