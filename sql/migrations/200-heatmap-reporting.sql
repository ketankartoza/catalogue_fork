--heatmap implementation
BEGIN;

--remove invalid geometry
UPDATE catalogue_search set geometry = NULL where not(st_isvalid(geometry));
--remove geometry with 'weird' coordiantes
UPDATE catalogue_search SET geometry = NULL where id in (974,976,970);
--remove 'world size polygons
update catalogue_search SET geometry = NULL where id in (910,894,895,615,679);

--create heatmap_grid table
CREATE TABLE "heatmap_grid" (
       "id" serial NOT NULL PRIMARY KEY,
       "x_cell" integer NOT NULL,
       "y_cell" integer NOT NULL
);

SELECT AddGeometryColumn('heatmap_grid', 'geometry', 4326, 'POLYGON', 2);
CREATE INDEX "heatmap_grid_geometry_id" ON "heatmap_grid" USING GIST ( "geometry" GIST_GEOMETRY_OPS );


--create heatmap_grid table
CREATE TABLE "heatmap_values" (
       "id" serial NOT NULL PRIMARY KEY,
       "grid_id" integer NOT NULL,
       "search_date" DATE NOT NULL,
       "hits" integer NOT NULL
);

ALTER TABLE "heatmap_values" ADD CONSTRAINT "heatmap_values__heatmap_gridr_id_fk" FOREIGN KEY ("grid_id") REFERENCES "heatmap_grid" ("id") DEFERRABLE INITIALLY DEFERRED;


-- Function: heatmap_grid_gen()
CREATE OR REPLACE FUNCTION heatmap_grid_gen(cell_size real DEFAULT 1)
  RETURNS void AS
$BODY$DECLARE
  lat_min real := -180;
  lat_max real := 180;
  lon_min real := 90;
  lon_max real := -90;
  x integer := 0;
  y integer := 0;
  bla text := '';
BEGIN

WHILE lon_min>lon_max LOOP
  lat_min:=-180;
  x:=0;
  WHILE lat_min<lat_max LOOP
    bla:='POLYGON(('||lat_min||' '||lon_min||','||lat_min+cell_size||' '|| lon_min||','||lat_min+cell_size||' '||lon_min+cell_size||','||lat_min||' '||lon_min+cell_size||','||lat_min||' '||lon_min||'))';
    --RAISE NOTICE 'x: %, y: %, (%, %), polygon: %', x,y,lat_min,lon_min,bla;
    INSERT INTO heatmap_grid (x_cell,y_cell,geometry) VALUES (x,y,ST_PolygonFromText(bla,4326));
    lat_min:=lat_min+cell_size;
    x:=x+1;
  END LOOP;
  lon_min:=lon_min-cell_size;
  y:=y+1;
END LOOP;
END;$BODY$
  LANGUAGE plpgsql VOLATILE;

-- Function: update_heatmap(date)
CREATE OR REPLACE FUNCTION update_heatmap(date_of_search date DEFAULT '1900-01-01'::date)
  RETURNS void AS
$BODY$DECLARE
  rec_date record;
  rec_search record;
  geom_inter record;-- geometry intersection
  heatmap_value record;
BEGIN
INSERT INTO heatmap_values (grid_id,search_date,hits) 
SELECT heatmap_grid.id,date_trunc('day',catalogue_search.search_date) as datum, count(heatmap_grid.id) as hits 
FROM heatmap_grid inner join catalogue_search on ST_Intersects(heatmap_grid.geometry,catalogue_search.geometry) and heatmap_grid.geometry && catalogue_search.geometry 
WHERE date_trunc('day',catalogue_search.search_date) >= date_of_search 
GROUP BY heatmap_grid.id,date_trunc('day',catalogue_search.search_date);

END;$BODY$
  LANGUAGE plpgsql VOLATILE;

-- Function: heatmap(date, date)
CREATE OR REPLACE FUNCTION heatmap(from_date date DEFAULT '1900-01-01'::date, to_date date DEFAULT now(),OUT geometry geometry,OUT hits bigint)
  RETURNS setof record AS
$BODY$
select st_centroid(geometry),sum(hits) as hits 
from heatmap_values a inner join heatmap_grid b on a.grid_id=b.id 
where search_date between $1 AND $2 
group by grid_id,st_centroid(geometry);
$BODY$
  LANGUAGE sql VOLATILE;

COMMIT;
