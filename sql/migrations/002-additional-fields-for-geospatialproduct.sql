-- ######################################################################
--
-- Migration script for additional fields on catalogue_geospatialproduct
-- GeospatialProduct
--
-- ######################################################################



begin;

ALTER TABLE "catalogue_geospatialproduct" ADD COLUMN  "data_type" varchar(1);
ALTER TABLE "catalogue_geospatialproduct" ADD COLUMN  "scale" integer;
ALTER TABLE "catalogue_geospatialproduct" ADD COLUMN  "processing_notes" text;


-- The final table structure, for reference
-- CREATE TABLE "catalogue_geospatialproduct" (
--     "genericproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericproduct" ("id") DEFERRABLE INITIALLY DEFERRED,
--     "name" varchar(255) NOT NULL,
--     "data_type" varchar(1),
--     "scale" integer,
--     "processing_notes" text
-- )


commit;