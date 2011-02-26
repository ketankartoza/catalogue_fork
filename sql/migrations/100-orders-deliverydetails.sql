BEGIN;
-- create deliverydetails table

CREATE TABLE "catalogue_deliverydetail" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED,
    "processing_level_id" integer NOT NULL REFERENCES "catalogue_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED,
    "projection_id" integer NOT NULL REFERENCES "catalogue_projection" ("id") DEFERRABLE INITIALLY DEFERRED,
    "datum_id" integer NOT NULL REFERENCES "catalogue_datum" ("id") DEFERRABLE INITIALLY DEFERRED,
    "resampling_method_id" integer NOT NULL REFERENCES "catalogue_resamplingmethod" ("id") DEFERRABLE INITIALLY DEFERRED,
    "file_format_id" integer NOT NULL REFERENCES "catalogue_fileformat" ("id") DEFERRABLE INITIALLY DEFERRED,
    "order_id" integer
);

-- update SearchRecord table

ALTER TABLE "catalogue_searchrecord" ADD "delivery_detail_id" integer REFERENCES "catalogue_deliverydetail" ("id") DEFERRABLE INITIALLY DEFERRED;

-- update Order table

ALTER TABLE "catalogue_order" ADD "delivery_detail_id" integer REFERENCES "catalogue_deliverydetail" ("id") DEFERRABLE INITIALLY DEFERRED;

-- migrate existing orders to deliverydetail table and setup reference

INSERT INTO "catalogue_deliverydetail" (user_id,processing_level_id,projection_id,datum_id,resampling_method_id,file_format_id,order_id) SELECT user_id,processing_level_id,projection_id,datum_id,resampling_method_id,file_format_id,id from catalogue_order;

UPDATE "catalogue_order" SET delivery_detail_id= catalogue_deliverydetail.id FROM catalogue_deliverydetail where order_id = catalogue_order.id;

-- clean up exiting tables
ALTER TABLE "catalogue_deliverydetail" DROP order_id;
ALTER TABLE "catalogue_order" DROP "processing_level_id";
ALTER TABLE "catalogue_order" DROP "projection_id";
ALTER TABLE "catalogue_order" DROP "datum_id";
ALTER TABLE "catalogue_order" DROP "resampling_method_id";
ALTER TABLE "catalogue_order" DROP "file_format_id";

COMMIT;