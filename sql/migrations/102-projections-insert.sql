BEGIN;

INSERT INTO "catalogue_projection" ("epsg_code", "name") VALUES (4326,'Geographic WGS84');
INSERT INTO "catalogue_projection" ("epsg_code", "name") VALUES (900913,'Google Mercator');

COMMIT;
