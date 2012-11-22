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
    "band_name" varchar(50) NOT NULL,
    "min_wavelength" integer NOT NULL,
    "max_wavelength" integer NOT NULL
)
;
CREATE TABLE "catalogue_pixelsize" (
    "id" serial NOT NULL PRIMARY KEY,
    "pixel_size_avg" double precision NOT NULL,
    "pixel_size_x" double precision NOT NULL,
    "pixel_size_y" double precision NOT NULL
)
;
CREATE TABLE "catalogue_bandpixelsize" (
    "id" serial NOT NULL PRIMARY KEY,
    "band_id" integer NOT NULL REFERENCES "catalogue_band" ("id") DEFERRABLE INITIALLY DEFERRED,
    "pixelsize_id" integer NOT NULL REFERENCES "catalogue_pixelsize" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("band_id", "pixelsize_id")
)
;
CREATE TABLE "catalogue_spectralmode_bandpixelsize" (
    "id" serial NOT NULL PRIMARY KEY,
    "spectralmode_id" integer NOT NULL,
    "bandpixelsize_id" integer NOT NULL REFERENCES "catalogue_bandpixelsize" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("spectralmode_id", "bandpixelsize_id")
)
;
CREATE TABLE "catalogue_spectralmode" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE,
    "description" text NOT NULL,
    "abbreviation" varchar(20) NOT NULL UNIQUE,
    "spatial_resolution" double precision NOT NULL,
    "instrument_type_id" integer NOT NULL REFERENCES "catalogue_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
ALTER TABLE "catalogue_spectralmode_bandpixelsize" ADD CONSTRAINT "spectralmode_id_refs_id_dbcc36ae" FOREIGN KEY ("spectralmode_id") REFERENCES "catalogue_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED;

COMMIT;