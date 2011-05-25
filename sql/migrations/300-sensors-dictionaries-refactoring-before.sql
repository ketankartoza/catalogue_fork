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

    -- Fix CBERS CCD and SACC MRS
    UPDATE  "catalogue_missionsensor" SET "abbreviation" = 'HRC' WHERE "abbreviation" = 'CCD' AND "name" = 'CBERS CCD';
    UPDATE  "catalogue_missionsensor" SET "abbreviation" = 'MMR' WHERE "abbreviation" = 'MRS' AND "name" = 'SACC MRS';


    -- drop uniq on catalogue_processinglevel name (legacy?)
    ALTER TABLE "catalogue_processinglevel" DROP CONSTRAINT "catalogue_processinglevel_name_key";


COMMIT;
