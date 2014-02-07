BEGIN;

ALTER TABLE search_searchrecrod ADD "cost_per_scene" double precision;
ALTER TABLE search_searchrecrod ADD "rand_cost_per_scene" double precision;
ALTER TABLE search_searchrecrod ADD "currency_id" integer;

CREATE INDEX "search_searchrecord_currency_id" ON "search_searchrecord" ("currency_id");

COMMIT;