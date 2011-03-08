-- ######################################################################
--
-- Migration script for the new License.type refactoring
--
-- Also assigns existing products to licenses based on the given rules
--
-- ######################################################################


BEGIN;

  ALTER TABLE "catalogue_license"
    ADD "type" integer;


  -- alter existing license
  UPDATE "catalogue_license" SET "name" = 'SAC Commercial License', "details" = 'SAC Commercial License', "type" = 3
    WHERE "name" = 'SAC License';

  -- Add new licenses
  INSERT INTO "catalogue_license" ("name", "details", "type") VALUES
  ('SAC Free License', 'SAC Free License', 1),
  ('SAC Partner License', 'SAC Partner License', 2);


  -- set not null
  ALTER TABLE "catalogue_license" ALTER "type" SET NOT NULL;


  -- set license type on existing product
  --   The license type is determined on a sensor by sensor, product by product basis.
  --   The following rules hold true:
  --
  -- 1. SPOT data are all under SAC Partner license
  -- 2. SAC-C, Sumbandilasat and CBERS are all under SAC Free License
  -- 3. When not explicitly deﬁned, all products should be assigned the SAC Commercial
  -- License

  -- rule 3
  UPDATE "catalogue_genericproduct" SET "license_id" = (SELECT "id" FROM "catalogue_license" WHERE "name" = 'SAC Commercial License');

  -- rule 1
  UPDATE "catalogue_genericproduct" SET "license_id" = (SELECT "id" FROM "catalogue_license" WHERE "name" = 'SAC Partner License') WHERE "catalogue_genericproduct"."id" IN (select genericimageryproduct_ptr_id AS id from catalogue_genericsensorproduct gp join catalogue_acquisitionmode am on am.id = gp.acquisition_mode_id join catalogue_sensortype as st on st.id = am.sensor_type_id  join catalogue_missionsensor ms on ms.id = st.mission_sensor_id join catalogue_mission mi on mi.id = ms.mission_id and mi.name LIKE 'Spot %');

  -- rule 2 Sumbandilasat
  UPDATE "catalogue_genericproduct" SET "license_id" = (SELECT "id" FROM "catalogue_license" WHERE "name" = 'SAC Free License') WHERE "catalogue_genericproduct"."id" IN (select genericimageryproduct_ptr_id AS id from catalogue_genericsensorproduct gp join catalogue_acquisitionmode am on am.id = gp.acquisition_mode_id join catalogue_sensortype as st on st.id = am.sensor_type_id  join catalogue_missionsensor ms on ms.id = st.mission_sensor_id join catalogue_mission mi on mi.id = ms.mission_id and mi.abbreviation IN ('ZA2' , 'S-C', 'C2B'));



COMMIT;
