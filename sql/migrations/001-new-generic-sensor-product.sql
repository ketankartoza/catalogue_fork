begin;


-- transfer data to the new table
select
 id ,
 mission_id ,
 mission_sensor_id  ,
 sensor_type_id  ,
 acquisition_mode_id ,
 product_acquisition_start  ,
 product_acquisition_end ,
 geometric_accuracy_mean ,
 geometric_accuracy_1sigma  ,
 geometric_accuracy_2sigma  ,
 radiometric_signal_to_noise_ratio ,
 radiometric_percentage_error  ,
 radiometric_resolution ,
 geometric_resolution_x ,
 geometric_resolution_y ,
 spectral_resolution ,
 spectral_accuracy  ,
 orbit_number ,
 path ,
 path_offset  ,
 "row"  ,
 row_offset ,
 offline_storage_medium_id  ,
 online_storage_medium_id
into catalogue_genericsensorproduct from catalogue_genericproduct ;

-- rename pk
alter table catalogue_genericsensorproduct rename id to genericproduct_ptr_id;

-- rename date field
alter table catalogue_genericproduct rename product_acquisition_start to product_date;


-- the view depends on fields that are going to be deleted
DROP VIEW vw_usercart;

-- CREATE OR REPLACE VIEW vw_usercart AS
--  SELECT catalogue_searchrecord.id, catalogue_searchrecord.order_id, auth_user.username, catalogue_missionsensor.name, catalogue_genericproduct.product_id, catalogue_genericproduct.spatial_coverage
--    FROM
--
--    -- rewrite with left join
--    -- catalogue_missionsensor,
--
--    catalogue_searchrecord,
--    catalogue_genericproduct,
--    auth_user
--    -- here it goes
--    LEFT JOIN catalogue_missionsensor ON catalogue_genericproduct.mission_sensor_id = catalogue_missionsensor.id
--   WHERE catalogue_searchrecord.user_id = auth_user.id AND catalogue_searchrecord.product_id = catalogue_genericproduct.id
--   -- left joined
--   -- AND catalogue_genericproduct.mission_sensor_id = catalogue_missionsensor.id
--   AND catalogue_searchrecord.order_id IS NULL;




-- drop old fields
alter table catalogue_genericproduct drop acquisition_mode_id ;
alter table catalogue_genericproduct drop geometric_accuracy_1sigma ;
alter table catalogue_genericproduct drop geometric_accuracy_2sigma ;
alter table catalogue_genericproduct drop geometric_accuracy_mean ;
alter table catalogue_genericproduct drop geometric_resolution_x ;
alter table catalogue_genericproduct drop geometric_resolution_y ;
alter table catalogue_genericproduct drop mission_id ;
alter table catalogue_genericproduct drop mission_sensor_id ;
alter table catalogue_genericproduct drop offline_storage_medium_id ;
alter table catalogue_genericproduct drop online_storage_medium_id ;
alter table catalogue_genericproduct drop orbit_number ;
alter table catalogue_genericproduct drop path ;
alter table catalogue_genericproduct drop path_offset ;
alter table catalogue_genericproduct drop product_acquisition_end ;
-- renamed to product_date
-- alter table catalogue_genericproduct drop product_acquisition_start ;
alter table catalogue_genericproduct drop radiometric_percentage_error ;
alter table catalogue_genericproduct drop radiometric_resolution ;
alter table catalogue_genericproduct drop radiometric_signal_to_noise_ratio ;
alter table catalogue_genericproduct drop "row" ;
alter table catalogue_genericproduct drop row_offset ;
alter table catalogue_genericproduct drop sensor_type_id ;
alter table catalogue_genericproduct drop spectral_accuracy ;
alter table catalogue_genericproduct drop spectral_resolution ;

-- add constraints
alter table catalogue_genericsensorproduct add CONSTRAINT catalogue_genericsensorproduct_pkey PRIMARY KEY (genericproduct_ptr_id);
alter table catalogue_genericsensorproduct add  CONSTRAINT catalogue_genericsensorproduct_acquisition_mode_id_fkey FOREIGN KEY (acquisition_mode_id)
  REFERENCES catalogue_acquisitionmode (id) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
alter table catalogue_genericsensorproduct add  CONSTRAINT catalogue_genericsensorproduct_mission_id_fkey FOREIGN KEY (mission_id)
  REFERENCES catalogue_mission (id) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
alter table catalogue_genericsensorproduct add CONSTRAINT catalogue_genericsensorproduct_mission_sensor_id_fkey FOREIGN KEY (mission_sensor_id)
  REFERENCES catalogue_missionsensor (id) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;
alter table catalogue_genericsensorproduct add  CONSTRAINT catalogue_genericsensorproduct_sensor_type_id_fkey FOREIGN KEY (sensor_type_id)
  REFERENCES catalogue_sensortype (id) MATCH SIMPLE
  ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- and not null...
alter table catalogue_genericsensorproduct alter genericproduct_ptr_id set not null;
alter table catalogue_genericsensorproduct alter mission_id set not null;
alter table catalogue_genericsensorproduct alter mission_sensor_id set not null;
alter table catalogue_genericsensorproduct alter sensor_type_id set not null;
alter table catalogue_genericsensorproduct alter acquisition_mode_id set not null;

alter table catalogue_genericsensorproduct alter product_acquisition_start set not null;
alter table catalogue_genericsensorproduct alter geometric_resolution_x set not null;
alter table catalogue_genericsensorproduct alter geometric_resolution_y set not null;
alter table catalogue_genericsensorproduct alter radiometric_resolution set not null;


-- now change reference to parent for imagery

ALTER TABLE catalogue_opticalproduct DROP CONSTRAINT catalogue_opticalproduct_genericproduct_ptr_id_fkey;
ALTER TABLE catalogue_opticalproduct RENAME genericproduct_ptr_id TO genericsensorproduct_ptr_id;

ALTER TABLE catalogue_opticalproduct
  ADD CONSTRAINT catalogue_opticalproduct_genericsensorproduct_ptr_id_fkey FOREIGN KEY (genericsensorproduct_ptr_id)
      REFERENCES catalogue_genericsensorproduct (genericproduct_ptr_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE catalogue_radarproduct DROP CONSTRAINT catalogue_radarproduct_genericproduct_ptr_id_fkey;
ALTER TABLE catalogue_radarproduct RENAME genericproduct_ptr_id TO genericsensorproduct_ptr_id;

ALTER TABLE catalogue_radarproduct
  ADD CONSTRAINT catalogue_radarproduct_genericsensorproduct_ptr_id_fkey FOREIGN KEY (genericsensorproduct_ptr_id)
      REFERENCES catalogue_genericsensorproduct(genericproduct_ptr_id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED;


-- add indexes
CREATE INDEX "catalogue_genericsensorproduct_mission_id" ON "catalogue_genericsensorproduct" ("mission_id");
CREATE INDEX "catalogue_genericsensorproduct_mission_sensor_id" ON "catalogue_genericsensorproduct" ("mission_sensor_id");
CREATE INDEX "catalogue_genericsensorproduct_sensor_type_id" ON "catalogue_genericsensorproduct" ("sensor_type_id");
CREATE INDEX "catalogue_genericsensorproduct_acquisition_mode_id" ON "catalogue_genericsensorproduct" ("acquisition_mode_id");
CREATE INDEX "catalogue_genericsensorproduct_product_acquisition_start" ON "catalogue_genericsensorproduct" ("product_acquisition_start");
CREATE INDEX "catalogue_genericsensorproduct_product_acquisition_end" ON "catalogue_genericsensorproduct" ("product_acquisition_end");




-- create the table : output from Django sqlall:

-- CREATE TABLE "catalogue_genericsensorproduct" (
-- "genericproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericproduct" ("id") DEFERRABLE INITIALLY DEFERRED,
-- "mission_id" integer NOT NULL REFERENCES "catalogue_mission" ("id") DEFERRABLE INITIALLY DEFERRED,
-- "mission_sensor_id" integer NOT NULL REFERENCES "catalogue_missionsensor" ("id") DEFERRABLE INITIALLY DEFERRED,
-- "sensor_type_id" integer NOT NULL REFERENCES "catalogue_sensortype" ("id") DEFERRABLE INITIALLY DEFERRED,
-- "acquisition_mode_id" integer NOT NULL REFERENCES "catalogue_acquisitionmode" ("id") DEFERRABLE INITIALLY DEFERRED,
-- "product_acquisition_start" timestamp with time zone NOT NULL,
-- "product_acquisition_end" timestamp with time zone,
-- "geometric_accuracy_mean" double precision,
-- "geometric_accuracy_1sigma" double precision,
-- "geometric_accuracy_2sigma" double precision,
-- "radiometric_signal_to_noise_ratio" double precision,
-- "radiometric_percentage_error" double precision,
-- "radiometric_resolution" integer NOT NULL,
-- "geometric_resolution_x" double precision NOT NULL,
-- "geometric_resolution_y" double precision NOT NULL,
-- "spectral_resolution" integer NOT NULL,
-- "spectral_accuracy" double precision,
-- "orbit_number" integer,
-- "path" integer,
-- "path_offset" integer,
-- "row" integer,
-- "row_offset" integer,
-- "offline_storage_medium_id" varchar(12),
-- "online_storage_medium_id" varchar(36)
-- )
-- ;



-- CREATE TABLE "catalogue_genericproduct" (
--  "id" serial NOT NULL PRIMARY KEY,
--  "product_date" timestamp with time zone NOT NULL,
--  "processing_level_id" integer NOT NULL REFERENCES "catalogue_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
--  "owner_id" integer NOT NULL REFERENCES "catalogue_institution" ("id") DEFERRABLE INITIALLY DEFERRED,
--  "license_id" integer NOT NULL REFERENCES "catalogue_license" ("id") DEFERRABLE INITIALLY DEFERRED,
--  "projection_id" integer NOT NULL REFERENCES "catalogue_projection" ("id") DEFERRABLE INITIALLY DEFERRED,
--  "quality_id" integer NOT NULL REFERENCES "catalogue_quality" ("id") DEFERRABLE INITIALLY DEFERRED,
--  "creating_software_id" integer NOT NULL REFERENCES "catalogue_creatingsoftware" ("id") DEFERRABLE INITIALLY DEFERRED,
--  "original_product_id" varchar(255),
--  "product_id" varchar(255) NOT NULL UNIQUE,
--  "product_revision" varchar(255),
--  "local_storage_path" varchar(255),
--  "metadata" text NOT NULL,
--  "remote_thumbnail_url" text NOT NULL
-- )
-- ;


-- CREATE TABLE "catalogue_opticalproduct" (
--     "genericsensorproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericsensorproduct" ("genericproduct_ptr_id") DEFERRABLE INITIALLY DEFERRED,
--     "cloud_cover" integer,
--     "sensor_inclination_angle" double precision,
--     "sensor_viewing_angle" double precision,
--     "gain_name" varchar(200),
--     "gain_value_per_channel" varchar(200),
--     "gain_change_per_channel" varchar(200),
--     "bias_per_channel" varchar(200),
--     "solar_zenith_angle" double precision,
--     "solar_azimuth_angle" double precision,
--     "earth_sun_distance" double precision
-- )
-- ;
-- CREATE TABLE "catalogue_radarproduct" (
--     "genericsensorproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericsensorproduct" ("genericproduct_ptr_id") DEFERRABLE INITIALLY DEFERRED,
--     "imaging_mode" varchar(200),
--     "look_direction" varchar(1),
--     "antenna_receive_configuration" varchar(1),
--     "polarising_mode" varchar(1),
--     "polarising_list" varchar(200),
--     "slant_range_resolution" double precision,
--     "azimuth_range_resolution" double precision,
--     "orbit_direction" varchar(1),
--     "calibration" varchar(255),
--     "incidence_angle" double precision
-- )


commit;