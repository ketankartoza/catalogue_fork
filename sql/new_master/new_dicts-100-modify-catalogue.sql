BEGIN;

-- we must add NOT NULL constraint after data migration
ALTER TABLE "catalogue_genericsensorproduct" ADD
    "satellite_instrument_id" integer REFERENCES "dictionaries_satelliteinstrument" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_genericsensorproduct" ADD
    "spectral_mode_id" integer REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED;


CREATE INDEX "catalogue_genericsensorproduct_satellite_instrument_id" ON "catalogue_genericsensorproduct" ("satellite_instrument_id");
CREATE INDEX "catalogue_genericsensorproduct_spectral_mode_id" ON "catalogue_genericsensorproduct" ("spectral_mode_id");


COMMIT;
