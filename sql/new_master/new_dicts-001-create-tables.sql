-- create new_dictionaries tables
BEGIN;
CREATE TABLE "dictionaries_collection" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "institution_id" integer NOT NULL REFERENCES "catalogue_institution" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "dictionaries_satellite" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "collection_id" integer NOT NULL REFERENCES "dictionaries_collection" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "dictionaries_scannertype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE
)
;
CREATE TABLE "dictionaries_instrumenttype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "is_radar" boolean NOT NULL,
    "is_taskable" boolean NOT NULL,
    "scanner_type_id" integer NOT NULL REFERENCES "dictionaries_scannertype" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "dictionaries_radarbeam" (
    "id" serial NOT NULL PRIMARY KEY,
    "instrument_type_id" integer NOT NULL UNIQUE REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "band_name" varchar(50) NOT NULL,
    "wavelength" integer NOT NULL,
    "looking_distance" varchar(50) NOT NULL,
    "azimuth_direction" varchar(50) NOT NULL
)
;
CREATE TABLE "dictionaries_imagingmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "radarbeam_id" integer NOT NULL REFERENCES "dictionaries_radarbeam" ("id") DEFERRABLE INITIALLY DEFERRED,
    "name" varchar(50) NOT NULL,
    "incidence_angle_min" double precision NOT NULL,
    "incidence_angle_max" double precision NOT NULL,
    "approximate_resolution" double precision NOT NULL,
    "swath_width" double precision NOT NULL,
    "number_of_looks" integer NOT NULL,
    "polarization" varchar(2) NOT NULL
)
;
CREATE TABLE "dictionaries_satelliteinstrument" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "operator_abbreviation" varchar(255) NOT NULL UNIQUE,
    "satellite_id" integer NOT NULL REFERENCES "dictionaries_satellite" ("id") DEFERRABLE INITIALLY DEFERRED,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("operator_abbreviation", "satellite_id", "instrument_type_id")
)
;
CREATE TABLE "dictionaries_band" (
    "id" serial NOT NULL PRIMARY KEY,
    "instrument_type_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    "band_name" varchar(50) NOT NULL,
    "band_number" integer NOT NULL,
    "min_wavelength" integer NOT NULL,
    "max_wavelength" integer NOT NULL,
    "pixelsize" integer NOT NULL
)
;
CREATE TABLE "dictionaries_spectralmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE
)
;
CREATE TABLE "dictionaries_bandspectralmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "band_id" integer NOT NULL REFERENCES "dictionaries_band" ("id") DEFERRABLE INITIALLY DEFERRED,
    "spectral_mode_id" integer NOT NULL REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED,
    "operator_name" varchar(20),
    UNIQUE ("band_id", "spectral_mode_id")
)
;
CREATE INDEX "dictionaries_collection_institution_id" ON "dictionaries_collection" ("institution_id");
CREATE INDEX "dictionaries_satellite_collection_id" ON "dictionaries_satellite" ("collection_id");
CREATE INDEX "dictionaries_instrumenttype_scanner_type_id" ON "dictionaries_instrumenttype" ("scanner_type_id");
CREATE INDEX "dictionaries_imagingmode_radarbeam_id" ON "dictionaries_imagingmode" ("radarbeam_id");
CREATE INDEX "dictionaries_satelliteinstrument_satellite_id" ON "dictionaries_satelliteinstrument" ("satellite_id");
CREATE INDEX "dictionaries_satelliteinstrument_instrument_type_id" ON "dictionaries_satelliteinstrument" ("instrument_type_id");
CREATE INDEX "dictionaries_band_instrument_type_id" ON "dictionaries_band" ("instrument_type_id");
CREATE INDEX "dictionaries_bandspectralmode_band_id" ON "dictionaries_bandspectralmode" ("band_id");
CREATE INDEX "dictionaries_bandspectralmode_spectral_mode_id" ON "dictionaries_bandspectralmode" ("spectral_mode_id");

COMMIT;
