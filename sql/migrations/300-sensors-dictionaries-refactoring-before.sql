-- ######################################################################
--
-- Migration script for sensor dictionaries refactoring
--
-- This does not create constraints, should be run BEFORE importing data
-- from the CSV with dictionaries_import.py
--
-- ######################################################################


BEGIN;

    ALTER TABLE "catalogue_mission" ADD "owner" VARCHAR(255);
    ALTER TABLE "catalogue_mission" ADD "operator_abbreviation" VARCHAR(255);

    ALTER TABLE "catalogue_missionsensor" ADD "operator_abbreviation" VARCHAR(255);

    ALTER TABLE "catalogue_sensortype" ADD "operator_abbreviation" VARCHAR(255); -- not unique
    ALTER TABLE "catalogue_acquisitionmode" ADD "operator_abbreviation" VARCHAR(255); -- not unique

    -- FIX ZA2
    UPDATE  "catalogue_missionsensor" SET "abbreviation" = 'MSI' WHERE "abbreviation" = 'SMS' AND "name" = 'Sumbandilasat MSS';

    -- Fix CBERS CCD
    UPDATE  "catalogue_missionsensor" SET "abbreviation" = 'HRC' WHERE "abbreviation" = 'CCD' AND "name" = 'CBERS CCD';
    UPDATE  "catalogue_missionsensor" SET "abbreviation" = 'MMR' WHERE "abbreviation" = 'MRS' AND "name" = 'SACC MRS';

    -- Fix MODIS imported data
--     UPDATE "catalogue_mission" SET "abbreviation" = 'AQA' WHERE "abbreviation" = 'MYD';
--     UPDATE "catalogue_mission" SET "abbreviation" = 'TER' WHERE "abbreviation" = 'MOD';
--     UPDATE "catalogue_mission" SET "abbreviation" = 'A-T' WHERE "abbreviation" = 'MCD';
--
--
--     UPDATE "catalogue_missionsensor" SET "abbreviation" = 'VNS' WHERE "abbreviation" = 'MOD' AND "catalogue_missionsensor"."mission" = (SELECT "id" FROM "catalogue_mission" WHERE "abbreviation" IN ( 'AQA', 'TER', 'A-T' );
--
--     UPDATE "catalogue_sensortype" SET "abbreviation" = 'VNS' WHERE "abbreviation" = 'MOD' AND "catalogue_sensortype"."mission_sensor_id" IN (SELECT "id" FROM "catalogue_missionsensor" WHERE "catalogue_missionsensor"."mission_id" IN (SELECT "id" FROM "catalogue_mission" WHERE "abbreviation" IN ( 'AQA', 'TER', 'A-T' )));
--
--     UPDATE "catalogue_acquisitionmode" SET "abbreviation" = 'VIT' WHERE "abbreviation" = 'MOD' AND "catalogue_acquisitionmode"."sensor_type_id" IN (SELECT "id" FROM "catalogue_sensortype" WHERE "abbreviation" = 'VNS' AND "catalogue_sensortype"."mission_sensor_id" IN (SELECT "id" FROM "catalogue_missionsensor" WHERE "catalogue_missionsensor"."mission_id" IN (SELECT "id" FROM "catalogue_mission" WHERE "abbreviation" IN ( 'AQA', 'TER', 'A-T' ))));




COMMIT;
