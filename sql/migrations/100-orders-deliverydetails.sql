BEGIN;
-- create deliverydetails table

CREATE TABLE "catalogue_deliverydetail" (
    "id" serial NOT NULL PRIMARY KEY,
    "user_id" integer NOT NULL,
    "processing_level_id" integer NOT NULL,
    "projection_id" integer NOT NULL,
    "datum_id" integer NOT NULL,
    "resampling_method_id" integer NOT NULL,
    "file_format_id" integer NOT NULL,
    "order_id" integer
);

-- update SearchRecord table

ALTER TABLE "catalogue_searchrecord" ADD "delivery_detail_id" integer;

-- update Order table

ALTER TABLE "catalogue_order" ADD "delivery_detail_id" integer;

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

-- add FKs

ALTER TABLE "catalogue_deliverydetail" ADD CONSTRAINT "catalogue_deliverydetail__auth_user_id_fk" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_deliverydetail" ADD CONSTRAINT "catalogue_deliverydetail__catalogue_processinglevel_id_fk" FOREIGN KEY ("processing_level_id") REFERENCES "catalogue_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_deliverydetail" ADD CONSTRAINT "catalogue_deliverydetail__catalogue_projection_id_fk" FOREIGN KEY ("projection_id")  REFERENCES "catalogue_projection" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_deliverydetail" ADD CONSTRAINT "catalogue_deliverydetail__catalogue_datum_id_fk" FOREIGN KEY ("datum_id") REFERENCES "catalogue_datum" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_deliverydetail" ADD CONSTRAINT "catalogue_deliverydetail__catalogue_resamplingmethod_id_fk" FOREIGN KEY ("resampling_method_id") REFERENCES "catalogue_resamplingmethod" ("id") DEFERRABLE INITIALLY DEFERRED; 

ALTER TABLE "catalogue_deliverydetail" ADD CONSTRAINT "catalogue_deliverydetail__catalogue_fileformat_id_fk" FOREIGN KEY ("file_format_id") REFERENCES "catalogue_fileformat" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_searchrecord" ADD CONSTRAINT "catalogue_searchrecord__catalogue_deliverydetail_id_fk" FOREIGN KEY ("delivery_detail_id") REFERENCES "catalogue_deliverydetail" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "catalogue_order" ADD CONSTRAINT "catalogue_order__catalogue_deliverydetail_id_fk" FOREIGN KEY ("delivery_detail_id") REFERENCES "catalogue_deliverydetail" ("id") DEFERRABLE INITIALLY DEFERRED;


COMMIT;