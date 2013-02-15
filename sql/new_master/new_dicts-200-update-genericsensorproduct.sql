BEGIN;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 1
WHERE "acquisition_mode_id" = 2;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 2
WHERE "acquisition_mode_id" = 11;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 34
WHERE "acquisition_mode_id" = 12;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 34
WHERE "acquisition_mode_id" = 13;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 34
WHERE "acquisition_mode_id" = 14;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 3
WHERE "acquisition_mode_id" = 15;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 8
WHERE "acquisition_mode_id" = 22;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 9
WHERE "acquisition_mode_id" = 23;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 16
WHERE "acquisition_mode_id" = 30;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 17
WHERE "acquisition_mode_id" = 31;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 4
WHERE "acquisition_mode_id" = 40;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 5
WHERE "acquisition_mode_id" = 41;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 20
WHERE "acquisition_mode_id" = 44;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 21
WHERE "acquisition_mode_id" = 45;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 22
WHERE "acquisition_mode_id" = 46;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 23
WHERE "acquisition_mode_id" = 47;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 24
WHERE "acquisition_mode_id" = 48;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 25
WHERE "acquisition_mode_id" = 49;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 26
WHERE "acquisition_mode_id" = 52;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 27
WHERE "acquisition_mode_id" = 53;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 12
WHERE "acquisition_mode_id" = 72;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 13
WHERE "acquisition_mode_id" = 73;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 28
WHERE "acquisition_mode_id" = 76;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 29
WHERE "acquisition_mode_id" = 77;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 30
WHERE "acquisition_mode_id" = 78;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 31
WHERE "acquisition_mode_id" = 79;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 32
WHERE "acquisition_mode_id" = 80;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 33
WHERE "acquisition_mode_id" = 81;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 6
WHERE "acquisition_mode_id" = 86;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 7
WHERE "acquisition_mode_id" = 87;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 14
WHERE "acquisition_mode_id" = 90;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 15
WHERE "acquisition_mode_id" = 91;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 18
WHERE "acquisition_mode_id" = 92;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 19
WHERE "acquisition_mode_id" = 93;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 10
WHERE "acquisition_mode_id" = 96;

UPDATE "catalogue_genericsensorproduct" SET
    "product_profile_id" = 11
WHERE "acquisition_mode_id" = 97;

COMMIT;

-- alter table needs to be in another transaction

BEGIN;
-- add NOT NULL constraint
ALTER TABLE "catalogue_genericsensorproduct"
    ALTER "product_profile_id" SET NOT NULL;

COMMIT;