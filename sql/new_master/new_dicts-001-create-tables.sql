-- create new_dictionaries tables
BEGIN;
CREATE TABLE "catalogue_collection" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "institution_id" integer NOT NULL REFERENCES "catalogue_institution" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "catalogue_satellite" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "collection_id" integer NOT NULL REFERENCES "catalogue_collection" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "catalogue_scannertype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE
)
;
CREATE TABLE "catalogue_instrumenttype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "is_radar" boolean NOT NULL,
    "is_taskable" boolean NOT NULL,
    "scanner_type_id" integer NOT NULL REFERENCES "catalogue_scannertype" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "catalogue_satelliteinstrument" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "satellite_id" integer NOT NULL REFERENCES "catalogue_satellite" ("id") DEFERRABLE INITIALLY DEFERRED,
    "instrument_type_id" integer NOT NULL REFERENCES "catalogue_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("operator_abbreviation", "satellite_id", "instrument_type_id")
)
;
CREATE TABLE "catalogue_band" (
    "id" serial NOT NULL PRIMARY KEY,
    "instrument_type_id" integer NOT NULL REFERENCES "catalogue_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "band_name" varchar(50) NOT NULL,
    "band_number" integer NOT NULL,
    "min_wavelength" integer NOT NULL,
    "max_wavelength" integer NOT NULL,
    "pixelsize" integer NOT NULL
)
;
CREATE TABLE "catalogue_spectralmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE
)
;
CREATE TABLE "catalogue_bandspectralmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "band_id" integer NOT NULL REFERENCES "catalogue_band" ("id") DEFERRABLE INITIALLY DEFERRED,
    "spectral_mode_id" integer NOT NULL REFERENCES "catalogue_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED,
    "operator_name" varchar(20),
    UNIQUE ("band_id", "spectral_mode_id")
)
;

CREATE INDEX "catalogue_collection_institution_id" ON "catalogue_collection" ("institution_id");
CREATE INDEX "catalogue_satellite_collection_id" ON "catalogue_satellite" ("collection_id");
CREATE INDEX "catalogue_instrumenttype_scanner_type_id" ON "catalogue_instrumenttype" ("scanner_type_id");
CREATE INDEX "catalogue_satelliteinstrument_satellite_id" ON "catalogue_satelliteinstrument" ("satellite_id");
CREATE INDEX "catalogue_satelliteinstrument_instrument_type_id" ON "catalogue_satelliteinstrument" ("instrument_type_id");
CREATE INDEX "catalogue_band_instrument_type_id" ON "catalogue_band" ("instrument_type_id");
CREATE INDEX "catalogue_bandspectralmode_band_id" ON "catalogue_bandspectralmode" ("band_id");
CREATE INDEX "catalogue_bandspectralmode_spectral_mode_id" ON "catalogue_bandspectralmode" ("spectral_mode_id");

COMMIT;