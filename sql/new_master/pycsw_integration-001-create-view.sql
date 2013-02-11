BEGIN;
CREATE OR REPLACE VIEW pycsw_catalogue AS
SELECT
  catalogue_genericproduct.product_id as product_id,
  'csw:Record'::text as typename,
  'http://www.opengis.net/cat/csw/2.0.2'::text as csw_schema,
  catalogue_genericproduct.product_date as insertdate,
  ''::text as csw_xml,
  ''::text as csw_anytext,
  ''::text as csw_creator,
  ''::text as csw_identifier,
  ''::text as csw_language,
  ''::text as csw_type,
  st_astext(spatial_coverage) as wkt_geometry,
  ''::text as accessconstraints,
  metadata as csw_description,
  ''::text as relation,
  catalogue_genericproduct.id as id,
  spatial_coverage
FROM
  public.catalogue_genericproduct;

COMMIT;