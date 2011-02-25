-- ######################################################################
--
-- Migration script for the new GenericImageryProduct refactoring
--
-- * move radiometric_resolution from GenericSensorProduct to ImageryProduct
-- * move spectral_resolution from GenericSensorProduct to ImageryProduct
-- * rename spectral_resolution to band_count
--
-- ######################################################################


BEGIN;

  ALTER TABLE "catalogue_genericimageryproduct" ADD "radiometric_resolution" integer;
  ALTER TABLE "catalogue_genericimageryproduct" ADD "band_count" integer;

  UPDATE "catalogue_genericimageryproduct" SET
    "radiometric_resolution"  = "catalogue_genericsensorproduct"."radiometric_resolution"
    FROM "catalogue_genericsensorproduct"
    WHERE "catalogue_genericimageryproduct"."genericproduct_ptr_id" = "catalogue_genericsensorproduct"."genericimageryproduct_ptr_id";

  UPDATE "catalogue_genericimageryproduct" SET
    "band_count" = "catalogue_genericsensorproduct"."spectral_resolution"
    FROM "catalogue_genericsensorproduct"
    WHERE "catalogue_genericimageryproduct"."genericproduct_ptr_id" = "catalogue_genericsensorproduct"."genericimageryproduct_ptr_id";


  -- set not null
  ALTER TABLE "catalogue_genericimageryproduct" ALTER "radiometric_resolution" SET NOT NULL;
  ALTER TABLE "catalogue_genericimageryproduct" ALTER "band_count"  SET NOT NULL;

  -- drop old fields
  ALTER TABLE "catalogue_genericsensorproduct" DROP "radiometric_resolution";
  ALTER TABLE "catalogue_genericsensorproduct" DROP "spectral_resolution";

COMMIT;