-- ######################################################################
--
-- Migration script for the new advanced search fields
--
-- ######################################################################

BEGIN;


ALTER TABLE "catalogue_search" ADD COLUMN  "acquisition_mode_id" integer;
ALTER TABLE "catalogue_search" ADD  CONSTRAINT catalogue_search_acquisition_mode_id_fkey FOREIGN KEY ("acquisition_mode_id")
  REFERENCES "catalogue_acquisitionmode" (id) MATCH SIMPLE;

ALTER TABLE "catalogue_search" ADD COLUMN  "license_id" integer;
ALTER TABLE "catalogue_search" ADD  CONSTRAINT catalogue_search_licence_id_fkey FOREIGN KEY ("license_id")
  REFERENCES "catalogue_license" (id) MATCH SIMPLE;


ALTER TABLE "catalogue_search" ADD COLUMN "mission_id" integer;
ALTER TABLE "catalogue_search" ADD  CONSTRAINT catalogue_search_mission_id_fkey FOREIGN KEY ("mission_id")  REFERENCES "catalogue_mission" ("id")  MATCH SIMPLE;

--ALTER TABLE "catalogue_search" ADD COLUMN "mission_sensor_id" integer;
--ALTER TABLE "catalogue_search" ADD  CONSTRAINT catalogue_search_missionsensor_id_fkey FOREIGN KEY ("mission_sensor_id") REFERENCES "catalogue_missionsensor" ("id") MATCH SIMPLE;

ALTER TABLE "catalogue_search" ADD COLUMN "sensor_type_id" integer;
ALTER TABLE "catalogue_search" ADD  CONSTRAINT catalogue_search_sensortype_id_fkey FOREIGN KEY ("sensor_type_id") REFERENCES "catalogue_sensortype" ("id") MATCH SIMPLE;



ALTER TABLE "catalogue_search" ADD COLUMN  "geometric_accuracy_mean" integer;
ALTER TABLE "catalogue_search" ADD COLUMN  "spectral_resolution" integer;
ALTER TABLE "catalogue_search" ADD COLUMN  "sensor_inclination_angle" FLOAT;

CREATE INDEX "catalogue_search_acquisition_mode_id" ON "catalogue_search" ("acquisition_mode_id");
CREATE INDEX "catalogue_search_license_id" ON "catalogue_search" ("license_id");

CREATE INDEX "catalogue_search_mission_id" ON "catalogue_search" ("mission_id");
--CREATE INDEX "catalogue_search_mission_sensor_id" ON "catalogue_search" ("mission_sensor_id");
CREATE INDEX "catalogue_search_sensortype_id" ON "catalogue_search" ("sensor_type_id");


COMMIT;