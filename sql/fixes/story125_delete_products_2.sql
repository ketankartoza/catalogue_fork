BEGIN;
create table delete_spot_owner_id AS
SELECT
   public.catalogue_genericproduct.id
FROM
  public.catalogue_opticalproduct,
  public.catalogue_genericsensorproduct,
  public.catalogue_genericimageryproduct,
  public.catalogue_genericproduct,
-- spot products subquery
(SELECT catalogue_acquisitionmode.id as id
FROM
  public.catalogue_mission,
  public.catalogue_missionsensor,
  public.catalogue_sensortype,
  public.catalogue_acquisitionmode
WHERE
  catalogue_missionsensor.mission_id = catalogue_mission.id AND
  catalogue_sensortype.mission_sensor_id = catalogue_missionsensor.id AND
  catalogue_acquisitionmode.sensor_type_id = catalogue_sensortype.id AND
  catalogue_mission.operator_abbreviation ILIKE 'SPOT%') AS spot_prod
-- spot products subquery
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericsensorproduct.genericimageryproduct_ptr_id AND
  catalogue_genericsensorproduct.genericimageryproduct_ptr_id = catalogue_genericimageryproduct.genericproduct_ptr_id AND
  catalogue_genericimageryproduct.genericproduct_ptr_id = catalogue_genericproduct.id AND
--spot
  catalogue_genericsensorproduct.acquisition_mode_id = spot_prod.id AND
-- condition
  catalogue_genericproduct.owner_id = 4;

delete from catalogue_opticalproduct using delete_spot_owner_id where genericsensorproduct_ptr_id=delete_spot_owner_id.id;
delete from catalogue_genericsensorproduct using delete_spot_owner_id where genericimageryproduct_ptr_id=delete_spot_owner_id.id;
delete from catalogue_genericimageryproduct using delete_spot_owner_id where genericproduct_ptr_id=delete_spot_owner_id.id;
delete from catalogue_searchrecord using delete_spot_owner_id where catalogue_searchrecord.product_id=delete_spot_owner_id.id;
delete from catalogue_genericproduct using delete_spot_owner_id where catalogue_genericproduct.id=delete_spot_owner_id.id;

--
drop table delete_spot_owner_id;
COMMIT;