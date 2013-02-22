BEGIN;

ALTER TABLE "search_search" ADD "satellite_id" integer REFERENCES "dictionaries_satellite" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "search_search" ADD "spectral_mode_id" integer REFERENCES "dictionaries_spectralmode" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE "search_search_instrumenttype" (
    "id" serial NOT NULL PRIMARY KEY,
    "search_id" integer NOT NULL,
    "instrumenttype_id" integer NOT NULL REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED,
    UNIQUE ("search_id", "instrumenttype_id")
)
;


-- alter FK constraint on search_search_processing_level
ALTER TABLE "search_search_processing_level" DROP CONSTRAINT "catalogue_search_processing_level_processinglevel_id_fkey";
ALTER TABLE "search_search_processing_level" ADD FOREIGN KEY ("processinglevel_id") REFERENCES catalogue_processinglevel(id) DEFERRABLE INITIALLY DEFERRED;


ALTER TABLE "search_search_instrumenttype" ADD CONSTRAINT "search_id_refs_id_8a552118" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "search_search_processing_level" ADD CONSTRAINT "search_id_refs_id_2503a17" FOREIGN KEY ("search_id") REFERENCES "search_search" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE INDEX "search_search_satellite_id" ON "search_search" ("satellite_id");
CREATE INDEX "search_search_spectral_mode_id" ON "search_search" ("spectral_mode_id");


COMMIT;
