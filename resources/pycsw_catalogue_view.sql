CREATE OR REPLACE FUNCTION gen_xml_stub(i_pid IN text, o_xml OUT text) AS
$$
DECLARE
t_text TEXT;
l_corner TEXT;
u_corner TEXT;
BEGIN

SELECT Box2D(spatial_coverage)::text INTO t_text FROM catalogue_genericproduct where original_product_id=i_pid;

l_corner := ltrim(split_part(t_text,',',1),'BOX(');
u_corner := rtrim(split_part(t_text,',',2),')');

o_xml := '<?xml version="1.0" standalone="no"?>
    <csw:GetRecordByIdResponse xmlns:soapenv="http://www.w3.org/2003/05/soap-envelope" xmlns:gml="http://www.opengis.net/gml" xmlns:dif="http://gcmd.gsfc.nasa.gov/Aboutus/xml/dif/" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:ows="http://www.opengis.net/ows" xmlns:fgdc="http://www.opengis.net/cat/csw/csdgm" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:csw="http://www.opengis.net/cat/csw/2.0.2" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:os="http://a9.com/-/spec/opensearch/1.1/" xmlns:dct="http://purl.org/dc/terms/" xmlns:ogc="http://www.opengis.net/ogc" xsi:schemaLocation="http://www.opengis.net/cat/csw/2.0.2 http://schemas.opengis.net/csw/2.0.2/CSW-discovery.xsd">
    <csw:Record>
        <dc:identifier>'||i_pid||'</dc:identifier>
        <dc:title>'||i_pid||'</dc:title>
        <dc:type>dataset</dc:type>
        <dc:subject>image</dc:subject>
        <dct:references scheme="http">http://catalogue.sansa.org.za/showProduct/'||i_pid||'</dct:references>
        <ows:BoundingBox crs="urn:x-ogc:def:crs:EPSG:6.11:4326" dimensions="2">
            <ows:LowerCorner>'||l_corner||'</ows:LowerCorner>
            <ows:UpperCorner>'||u_corner||'</ows:UpperCorner>
        </ows:BoundingBox>
    </csw:Record>
    </csw:GetRecordByIdResponse>';

END;
$$
LANGUAGE 'plpgsql' VOLATILE STRICT;


create or replace view pycsw_catalogue as SELECT catalogue_genericproduct.original_product_id AS product_id,
    'csw:Record'::text AS typename,
    'http://www.opengis.net/cat/csw/2.0.2'::text AS csw_schema,
    catalogue_genericproduct.product_date AS insertdate,
    gen_xml_stub(catalogue_genericproduct.original_product_id) as csw_xml,
    ''::text AS csw_anytext,
    ''::text AS csw_creator,
    ''::text AS csw_identifier,
    ''::text AS csw_language,
    'dataset'::text AS csw_type,
    st_astext(catalogue_genericproduct.spatial_coverage) AS wkt_geometry,
    ''::text AS accessconstraints,
    catalogue_genericproduct.metadata AS csw_metadata,
    ''::text AS relation,
    catalogue_genericproduct.id,
    catalogue_genericproduct.spatial_coverage,
    'image'::text AS csw_keywords,
    'test,test_desc,http,http://catalogue.sansa.org.za/showProduct/'::text || catalogue_genericproduct.original_product_id::text AS csw_links
FROM catalogue_genericproduct
ORDER BY catalogue_genericproduct.id ASC
LIMIT 100;

