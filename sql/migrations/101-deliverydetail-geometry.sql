BEGIN;

-- add geometry column to delivery details model

SELECT AddGeometryColumn('catalogue_deliverydetail', 'geometry', 4326, 'POLYGON', 2);
CREATE INDEX "catalogue_deliverydetail_geometry_id" ON "catalogue_deliverydetail" USING GIST ( "geometry" GIST_GEOMETRY_OPS );

COMMIT;
