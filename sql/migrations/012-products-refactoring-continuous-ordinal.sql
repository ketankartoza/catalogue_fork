CREATE TABLE "catalogue_ordinalproduct" (
    "genericproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericproduct" ("id") DEFERRABLE INITIALLY DEFERRED,
    "class_count" integer NOT NULL,
    "confusion_matrix" varchar(80),
    "kappa_score" double precision
)
;
CREATE TABLE "catalogue_continuousproduct" (
    "genericproduct_ptr_id" integer NOT NULL PRIMARY KEY REFERENCES "catalogue_genericproduct" ("id") DEFERRABLE INITIALLY DEFERRED,
    "range_min" double precision NOT NULL,
    "range_max" double precision NOT NULL,
    "unit_id" integer NOT NULL REFERENCES "catalogue_unit" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
