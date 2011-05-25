-- ######################################################################
--
-- Migration script for sensor dictionaries refactoring
--
-- This creates the constraints, should be run AFTER importing data
-- from the CSV with dictionaries_import.py
--
-- ######################################################################




BEGIN;

    -- fix null values for Extras (i.e. dictionary entries which did not match with v5)
    UPDATE "catalogue_missionsensor" SET "operator_abbreviation"="abbreviation" WHERE "operator_abbreviation" IS NULL;
    UPDATE "catalogue_sensortype" SET "operator_abbreviation"="abbreviation" WHERE "operator_abbreviation" IS NULL;
    UPDATE "catalogue_acquisitionmode" SET "operator_abbreviation"="abbreviation" WHERE "operator_abbreviation" IS NULL;

    -- set not null
    ALTER TABLE "catalogue_mission" ALTER "owner" SET NOT NULL;
    ALTER TABLE "catalogue_mission" ALTER "operator_abbreviation" SET NOT NULL;
    ALTER TABLE "catalogue_missionsensor" ALTER "operator_abbreviation" SET NOT NULL;
    ALTER TABLE "catalogue_sensortype" ALTER "operator_abbreviation" SET NOT NULL;
    ALTER TABLE "catalogue_acquisitionmode" ALTER "operator_abbreviation" SET NOT NULL;

    -- set unique
    ALTER TABLE "catalogue_mission"
    ADD CONSTRAINT "catalogue_mission_operator_abbreviation_key" UNIQUE("operator_abbreviation");
    ALTER TABLE "catalogue_missionsensor"
    ADD CONSTRAINT "catalogue_missionsensor_operator_abbreviation_key" UNIQUE("operator_abbreviation");

    -- fix SAR is_radar
    UPDATE "catalogue_missionsensor" SET "is_radar=True" WHERE "abbreviation" = 'SAR';

COMMIT;
