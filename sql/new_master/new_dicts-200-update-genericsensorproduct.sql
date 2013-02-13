BEGIN;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 22,
    "spectral_mode_id" = NULL
WHERE "acquisition_mode_id" = 2;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 19,
    "spectral_mode_id" = 25
WHERE "acquisition_mode_id" = 11;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 20,
    "spectral_mode_id" = NULL -- fuzzy
WHERE "acquisition_mode_id" = 12;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 20,
    "spectral_mode_id" = NULL -- fuzzy
WHERE "acquisition_mode_id" = 13;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 20,
    "spectral_mode_id" = NULL -- fuzzy
WHERE "acquisition_mode_id" = 14;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 23,
    "spectral_mode_id" = 31
WHERE "acquisition_mode_id" = 15;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 7,
    "spectral_mode_id" = 20
WHERE "acquisition_mode_id" = 22;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 8,
    "spectral_mode_id" = 20
WHERE "acquisition_mode_id" = 23;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 3,
    "spectral_mode_id" = 17
WHERE "acquisition_mode_id" = 30;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 4,
    "spectral_mode_id" = 17
WHERE "acquisition_mode_id" = 31;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 9,
    "spectral_mode_id" = 20
WHERE "acquisition_mode_id" = 40;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 10,
    "spectral_mode_id" = 20
WHERE "acquisition_mode_id" = 41;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 1,
    "spectral_mode_id" = 14
WHERE "acquisition_mode_id" = 44;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 2,
    "spectral_mode_id" = 14
WHERE "acquisition_mode_id" = 45;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 1,
    "spectral_mode_id" = 15
WHERE "acquisition_mode_id" = 46;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 2,
    "spectral_mode_id" = 15
WHERE "acquisition_mode_id" = 47;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 1,
    "spectral_mode_id" = 16
WHERE "acquisition_mode_id" = 48;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 2,
    "spectral_mode_id" = 16
WHERE "acquisition_mode_id" = 49;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 1,
    "spectral_mode_id" = 13
WHERE "acquisition_mode_id" = 52;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 2,
    "spectral_mode_id" = 13
WHERE "acquisition_mode_id" = 53;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 5,
    "spectral_mode_id" = 20
WHERE "acquisition_mode_id" = 72;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 6,
    "spectral_mode_id" = 20
WHERE "acquisition_mode_id" = 73;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 12,
    "spectral_mode_id" = 6 -- fuzzy
WHERE "acquisition_mode_id" = 76;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 13,
    "spectral_mode_id" = 6 -- fuzzy
WHERE "acquisition_mode_id" = 77;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 14,
    "spectral_mode_id" = 6 -- fuzzy
WHERE "acquisition_mode_id" = 78;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 16,
    "spectral_mode_id" = 6 -- fuzzy
WHERE "acquisition_mode_id" = 79;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 17,
    "spectral_mode_id" = 4
WHERE "acquisition_mode_id" = 80;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 18,
    "spectral_mode_id" = 30
WHERE "acquisition_mode_id" = 81;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 9,
    "spectral_mode_id" = 19
WHERE "acquisition_mode_id" = 86;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 10,
    "spectral_mode_id" = 19
WHERE "acquisition_mode_id" = 87;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 5,
    "spectral_mode_id" = 19
WHERE "acquisition_mode_id" = 90;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 6,
    "spectral_mode_id" = 19
WHERE "acquisition_mode_id" = 91;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 3,
    "spectral_mode_id" = 18
WHERE "acquisition_mode_id" = 92;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 4,
    "spectral_mode_id" = 18
WHERE "acquisition_mode_id" = 93;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 7,
    "spectral_mode_id" = 19
WHERE "acquisition_mode_id" = 96;

UPDATE "catalogue_genericsensorproduct" SET
    "satellite_instrument_id" = 8,
    "spectral_mode_id" = 19
WHERE "acquisition_mode_id" = 97;


-- add NOT NULL constraint
ALTER TABLE "catalogue_genericsensorproduct"
    ALTER "satellite_instrument_id" SET NOT NULL;

COMMIT;