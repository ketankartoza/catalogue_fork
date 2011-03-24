-- ######################################################################
--
-- Migration script for the search refactoring
--
-- after this migration you need to run from the project folder:
-- $ python manage.py runscript -v 2 --pythonpath=./sql/migrations post_migration.py
-- (ignore the error "No module for script 'post_migration.py' found" at the end)
--
-- ######################################################################

BEGIN;

  -- Postgresql handles foreign keys in internal triggers. Settings all these triggers for
  -- immediate execution avoid pending triggers errors
  SET CONSTRAINTS ALL IMMEDIATE;

  -----------------------------
  -- adds new row/path fields
  -----------------------------
  ALTER TABLE "catalogue_search" ADD "k_orbit_path" VARCHAR(255);
  ALTER TABLE "catalogue_search" ADD "j_frame_row" VARCHAR(255);
  -- populates from old values
  UPDATE "catalogue_search" SET "k_orbit_path" = "k_orbit_path_min"||'-'||"k_orbit_path_max" WHERE "k_orbit_path_min" IS NOT NULL AND "k_orbit_path_max" IS NOT NULL AND "k_orbit_path_min" != "k_orbit_path_max";
  UPDATE "catalogue_search" SET "j_frame_row" = "j_frame_row_min"||'-'||"j_frame_row_max" WHERE "j_frame_row_min" IS NOT NULL AND "j_frame_row_max" IS NOT NULL AND "j_frame_row_min" != "j_frame_row_max";
  UPDATE "catalogue_search" SET "k_orbit_path" = "k_orbit_path_min" WHERE "k_orbit_path_min" IS NOT NULL AND "k_orbit_path_max" IS NOT NULL AND "k_orbit_path_min" = "k_orbit_path_max";
  UPDATE "catalogue_search" SET "j_frame_row" = "j_frame_row_min" WHERE "j_frame_row_min" IS NOT NULL AND "j_frame_row_max" IS NOT NULL AND "j_frame_row_min" = "j_frame_row_max";

  -- drops old fields
  ALTER TABLE "catalogue_search" DROP "k_orbit_path_min";
  ALTER TABLE "catalogue_search" DROP "k_orbit_path_max";
  ALTER TABLE "catalogue_search" DROP "j_frame_row_min";
  ALTER TABLE "catalogue_search" DROP "j_frame_row_max";


  -------------------------------------------
  -- drops license and adds license_type
  -------------------------------------------
  DROP TABLE "catalogue_search_license";
  ALTER TABLE "catalogue_search" ADD "license_type" INTEGER;


  ------------------------------
  -- renames spectral_resolution
  ------------------------------
  ALTER TABLE "catalogue_search" RENAME "spectral_resolution" TO "band_count";

  -----------------------------------
  -- date ranges
  -----------------------------------

  CREATE TABLE "catalogue_searchdaterange" (
      "id" serial NOT NULL PRIMARY KEY,
      "start_date" date NOT NULL,
      "end_date" date NOT NULL,
      "search_id" integer NOT NULL REFERENCES "catalogue_search" ("id") DEFERRABLE INITIALLY DEFERRED
  )
  ;
  CREATE INDEX "catalogue_searchdaterange_search_id" ON "catalogue_searchdaterange" ("search_id");

  -- fixex legacy error
  ALTER TABLE "catalogue_search" ALTER "end_date" TYPE DATE;
  -- adds date ranges
  INSERT INTO "catalogue_searchdaterange" ("search_id", "start_date", "end_date") SELECT "id", "start_date", "end_date" FROM "catalogue_search";
  -- drops start and end dates
  ALTER TABLE "catalogue_search" DROP "start_date";
  ALTER TABLE "catalogue_search" DROP "end_date";


  ----------------------------------------
  -- Processing level new FK
  ----------------------------------------
  CREATE TABLE "catalogue_search_processing_level" (
      "id" serial NOT NULL PRIMARY KEY,
      "search_id" integer NOT NULL,
      "processinglevel_id" integer NOT NULL REFERENCES "catalogue_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
      UNIQUE ("search_id", "processinglevel_id")
  )
  ;
  ALTER TABLE "catalogue_search_processing_level" ADD CONSTRAINT "search_id_refs_id_d5a61dd3" FOREIGN KEY ("search_id") REFERENCES "catalogue_search" ("id") DEFERRABLE INITIALLY DEFERRED;


--ROLLBACK;
COMMIT;