BEGIN;

-- we must add NOT NULL constraint after data migration
ALTER TABLE "catalogue_genericsensorproduct" ADD
    "product_profile_id" integer REFERENCES "dictionaries_productprofile" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "catalogue_genericsensorproduct_product_profile_id" ON "catalogue_genericsensorproduct" ("product_profile_id");


COMMIT;
