BEGIN;

ALTER TABLE catalogue_genericproduct
    ADD new_processing_level_id integer REFERENCES "dictionaries_processinglevel" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;

BEGIN;

-- update optical products

UPDATE catalogue_genericproduct SET new_processing_level_id = dictionaries_instrumenttype.base_processing_level_id
FROM
  catalogue_opticalproduct,
  dictionaries_opticalproductprofile,
  dictionaries_satelliteinstrument,
  dictionaries_instrumenttype
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericproduct.id AND
  dictionaries_opticalproductprofile.id = catalogue_opticalproduct.product_profile_id AND
  dictionaries_satelliteinstrument.id = dictionaries_opticalproductprofile.satellite_instrument_id AND
  dictionaries_instrumenttype.id = dictionaries_satelliteinstrument.instrument_type_id;


-- update radar products
UPDATE catalogue_genericproduct SET new_processing_level_id = dictionaries_instrumenttype.base_processing_level_id
FROM
  catalogue_radarproduct,
  dictionaries_radarproductprofile,
  dictionaries_satelliteinstrument,
  dictionaries_instrumenttype
WHERE
  catalogue_radarproduct.genericsensorproduct_ptr_id = catalogue_genericproduct.id AND
  dictionaries_radarproductprofile.id = catalogue_radarproduct.product_profile_id AND
  dictionaries_satelliteinstrument.id = dictionaries_radarproductprofile.satellite_instrument_id AND
  dictionaries_satelliteinstrument.instrument_type_id = dictionaries_instrumenttype.id;

COMMIT;

BEGIN;

ALTER TABLE catalogue_genericproduct DROP processing_level_id CASCADE;
ALTER TABLE catalogue_genericproduct RENAME new_processing_level_id TO processing_level_id;
ALTER TABLE catalogue_genericproduct ALTER processing_level_id SET NOT NULL;

COMMIT;