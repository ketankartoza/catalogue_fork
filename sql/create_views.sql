drop view vw_usercart; 
create view vw_usercart as SELECT 
  catalogue_searchrecord.id, catalogue_searchrecord.order_id, 
  auth_user.username, 
  catalogue_missionsensor."name", 
  catalogue_genericproduct."product_id",
  catalogue_genericproduct.spatial_coverage
FROM 
  public.catalogue_missionsensor, 
  public.catalogue_searchrecord, 
  public.catalogue_genericproduct, 
  public.auth_user
WHERE 
  catalogue_searchrecord.user_id = auth_user.id AND
  catalogue_searchrecord.product_id = catalogue_genericproduct.id AND
  catalogue_genericproduct.mission_sensor_id = catalogue_missionsensor.id AND
  catalogue_searchrecord.order_id isnull;
grant select on vw_usercart to readonly;
grant select on catalogue_visit to readonly;
create view vw_visitor_report as SELECT ( SELECT count(*) AS count
FROM catalogue_visit v2
WHERE v2.city::text <= v.city::text) AS id, count(*) AS visit_count, v.ip_position AS geometry, v.country, v.city
FROM catalogue_visit v
GROUP BY v.country, v.city, v.ip_position
ORDER BY v.country, v.city;
grant select on vw_visitor_report to readonly;
grant select on catalogue_search to readonly;
