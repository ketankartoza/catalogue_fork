-- ######################################################################
--
-- Migration script for the new advanced search fields
--
-- ######################################################################

BEGIN;


ALTER TABLE "catalogue_search" ADD COLUMN  "acquisition_mode_id" integer;
ALTER TABLE "catalogue_search" ADD  CONSTRAINT "catalogue_search_acquisition_mode_id_fkey" FOREIGN KEY ("acquisition_mode_id")
  REFERENCES "catalogue_acquisitionmode" ("id") MATCH SIMPLE;

ALTER TABLE "catalogue_search" ADD COLUMN "mission_id" integer;
ALTER TABLE "catalogue_search" ADD  CONSTRAINT "catalogue_search_mission_id_fkey" FOREIGN KEY ("mission_id")
  REFERENCES "catalogue_mission" ("id")  MATCH SIMPLE;

ALTER TABLE "catalogue_search" ADD COLUMN "sensor_type_id" integer;
ALTER TABLE "catalogue_search" ADD  CONSTRAINT "catalogue_search_sensortype_id_fkey" FOREIGN KEY ("sensor_type_id")
  REFERENCES "catalogue_sensortype" ("id") MATCH SIMPLE;

ALTER TABLE "catalogue_search" ADD COLUMN  "geometric_accuracy_mean" integer;
ALTER TABLE "catalogue_search" ADD COLUMN  "spectral_resolution" integer;
ALTER TABLE "catalogue_search" ADD COLUMN  "sensor_inclination_angle_start" FLOAT;
ALTER TABLE "catalogue_search" ADD COLUMN  "sensor_inclination_angle_end" FLOAT;

CREATE INDEX "catalogue_search_acquisition_mode_id" ON "catalogue_search" ("acquisition_mode_id");
CREATE INDEX "catalogue_search_license_id" ON "catalogue_search" ("license_id");
CREATE INDEX "catalogue_search_mission_id" ON "catalogue_search" ("mission_id");
CREATE INDEX "catalogue_search_sensortype_id" ON "catalogue_search" ("sensor_type_id");


CREATE TABLE "catalogue_search_license" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "license_id" integer NOT NULL REFERENCES "catalogue_license" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "license_id")
)
;
ALTER TABLE "catalogue_search_license" ADD CONSTRAINT "search_id_refs_id_8b0fc39d" FOREIGN KEY ("search_id") REFERENCES "catalogue_search" ("id") DEFERRABLE INITIALLY DEFERRED;


COMMIT;