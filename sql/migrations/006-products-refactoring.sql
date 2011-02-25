-- ######################################################################
--
-- Migration script for the new GenericImageryProduct refactoring
--
-- * changes to the Product hierarchy
-- * changes to the Sensors/Mission dictionaries for GenericSensorProducts
--
-- WARNING
--
-- after this migration you need to run from the project folder:
-- $ python manage.py runscript -v 2 --pythonpath=./sql/migrations post_migration.py
--
-- ######################################################################

BEGIN;

-- drop "L"  from processing level
update "catalogue_processinglevel" set "abbreviation" = regexp_replace("abbreviation", '^L', '') where true;


-- transfer data to the new table
select
 "genericproduct_ptr_id" ,
 "geometric_resolution_x" AS "geometric_resolution", -- copy into new geometric_resolution
 "geometric_resolution_x" ,
 "geometric_resolution_y"
into catalogue_genericimageryproduct from catalogue_genericsensorproduct ;

-- set constraints

alter table catalogue_genericimageryproduct add CONSTRAINT catalogue_genericimageryproduct_pkey PRIMARY KEY (genericproduct_ptr_id);
alter table catalogue_genericimageryproduct alter genericproduct_ptr_id set not null;
alter table catalogue_genericimageryproduct alter geometric_resolution set not null;
alter table catalogue_genericimageryproduct alter geometric_resolution_x set not null;
alter table catalogue_genericimageryproduct alter geometric_resolution_y set not null;

-- set indexes
-- no indexes, maybe we should set indexes on geometric_resolution*

-- change related tables (optical and radar)

ALTER TABLE catalogue_opticalproduct DROP CONSTRAINT catalogue_opticalproduct_genericsensorproduct_ptr_id_fkey;
ALTER TABLE catalogue_radarproduct DROP CONSTRAINT catalogue_radarproduct_genericsensorproduct_ptr_id_fkey;

-- now change reference to parent for generic sensor

ALTER TABLE catalogue_genericsensorproduct DROP CONSTRAINT catalogue_genericsensorproduct_pkey;
ALTER TABLE catalogue_genericsensorproduct RENAME genericproduct_ptr_id TO genericimageryproduct_ptr_id;
ALTER TABLE catalogue_genericsensorproduct
  ADD CONSTRAINT catalogue_genericsensorproduct_pkey PRIMARY KEY(genericimageryproduct_ptr_id);

-- re-add constraints in related tables (optical and radar)

ALTER TABLE catalogue_opticalproduct
  ADD CONSTRAINT catalogue_opticalproduct_genericsensorproduct_ptr_id_fkey FOREIGN KEY (genericsensorproduct_ptr_id)
      REFERENCES catalogue_genericsensorproduct (genericimageryproduct_ptr_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE catalogue_radarproduct
  ADD CONSTRAINT catalogue_radarproduct_genericsensorproduct_ptr_id_fkey FOREIGN KEY (genericsensorproduct_ptr_id)
      REFERENCES catalogue_genericsensorproduct (genericimageryproduct_ptr_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- drop fields from the old table
ALTER TABLE catalogue_genericsensorproduct DROP geometric_resolution_x;
ALTER TABLE catalogue_genericsensorproduct DROP geometric_resolution_y;

-- For reference:

--  CREATE TABLE "catalogue_genericimageryproduct" (
--      "genericproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericproduct" ("id") DEFERRABLE INITIALLY DEFERRED,
--      "geometric_resolution" double precision NOT NULL,
--      "geometric_resolution_x" double precision NOT NULL,
--      "geometric_resolution_y" double precision NOT NULL
--  );


----------------------------------------------------------------
-- New dictionaries
----------------------------------------------------------------
CREATE TABLE "catalogue_missiongroup" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL
);

INSERT INTO "catalogue_missiongroup" VALUES (1, 'Unknown');

-- create new FKs for the hierarchy, without constraints
ALTER TABLE "catalogue_mission" ADD
    "mission_group_id" integer REFERENCES "catalogue_missiongroup" ("id");
ALTER TABLE "catalogue_missionsensor" ADD
    "mission_id" integer REFERENCES "catalogue_mission" ("id");
ALTER TABLE "catalogue_sensortype" ADD
    "mission_sensor_id" integer REFERENCES "catalogue_missionsensor" ("id");
ALTER TABLE "catalogue_sensortype" ADD
    "is_taskable" boolean;
ALTER TABLE "catalogue_acquisitionmode" ADD
    "sensor_type_id" integer REFERENCES "catalogue_sensortype" ("id");
ALTER TABLE "catalogue_acquisitionmode" ADD
    "is_grayscale" boolean;


-- drop unique constraint on MissionSensor abbreviation
ALTER TABLE catalogue_missionsensor DROP CONSTRAINT catalogue_missionsensor_abbreviation_key;
ALTER TABLE catalogue_sensortype DROP CONSTRAINT catalogue_sensortype_abbreviation_key;
ALTER TABLE catalogue_acquisitionmode DROP CONSTRAINT catalogue_acquisitionmode_abbreviation_key;


-- populate from old table
-- select distinct am.id, am.abbreviation, gs.sensor_type_id from catalogue_acquisitionmode am left join catalogue_genericsensorproduct gs on gs.acquisition_mode_id = am.id;


UPDATE "catalogue_acquisitionmode" SET sensor_type_id = ( select distinct gs.sensor_type_id from catalogue_genericsensorproduct gs WHERE gs.acquisition_mode_id = id LIMIT 1) ;
UPDATE "catalogue_sensortype" SET mission_sensor_id = ( select distinct gs.mission_sensor_id from catalogue_genericsensorproduct gs WHERE gs.sensor_type_id = id LIMIT 1) ;
UPDATE "catalogue_missionsensor" SET mission_id = ( select distinct gs.mission_id from catalogue_genericsensorproduct gs WHERE gs.mission_sensor_id = id LIMIT 1) ;

-- set defaults for new fields

UPDATE "catalogue_mission" SET "mission_group_id" = 1 WHERE true;
UPDATE "catalogue_sensortype" SET "is_taskable" = true WHERE true;
UPDATE "catalogue_acquisitionmode" SET "is_grayscale" = false WHERE true;

-- add constraints
ALTER TABLE "catalogue_mission" ALTER "mission_group_id" SET NOT NULL;
ALTER TABLE "catalogue_missionsensor" ALTER "mission_id" SET NOT NULL;
ALTER TABLE "catalogue_sensortype" ALTER "mission_sensor_id" SET NOT NULL;
ALTER TABLE "catalogue_sensortype" ALTER "is_taskable" SET NOT NULL;
ALTER TABLE "catalogue_acquisitionmode" ALTER  "sensor_type_id" SET NOT NULL;
-- finally, drop old columns
ALTER TABLE "catalogue_genericsensorproduct" DROP COLUMN mission_id;
ALTER TABLE "catalogue_genericsensorproduct" DROP COLUMN mission_sensor_id;
ALTER TABLE "catalogue_genericsensorproduct" DROP COLUMN sensor_type_id ;

-- create unique constraint on MissionSensor abbreviation
ALTER TABLE catalogue_missionsensor
  ADD CONSTRAINT catalogue_missionsensor_abbreviation_key UNIQUE(abbreviation, mission_id);

ALTER TABLE catalogue_sensortype
  ADD CONSTRAINT catalogue_sensortype_abbreviation_key UNIQUE(abbreviation, mission_sensor_id);

ALTER TABLE catalogue_acquisitionmode
  ADD CONSTRAINT catalogue_acquisitionmode_abbreviation_key UNIQUE(abbreviation, sensor_type_id);


COMMIT;