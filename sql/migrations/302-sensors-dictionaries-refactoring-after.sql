-- ######################################################################
--
-- Migration script for sensor dictionaries refactoring
--
-- This creates the constraints, should be run AFTER importing data
-- from the CSV with dictionaries_import.py
--
-- ######################################################################




BEGIN;

    -- set not null
    ALTER TABLE "catalogue_mission" ALTER "owner" SET NOT NULL;
    ALTER TABLE "catalogue_mission" ALTER "operator_abbreviation" SET NOT NULL;
    ALTER TABLE "catalogue_missionsensor" ALTER "operator_abbreviation" SET NOT NULL;
    ALTER TABLE "catalogue_sensortype" ALTER "operator_abbreviation" SET NOT NULL;
    ALTER TABLE "catalogue_acquisitionmode" ALTER "operator_abbreviation" SET NOT NULL;

    -- set unique
    ALTER TABLE "catalogue_mission"
    ADD CONSTRAINT "catalogue_mission_opertor_abbreviation_key" UNIQUE("operator_abbreviation");
    ALTER TABLE "catalogue_missionsensor"
    ADD CONSTRAINT "catalogue_missionsensor_opertor_abbreviation_key" UNIQUE("operator_abbreviation");


COMMIT;
