BEGIN;

ALTER TABLE catalogue_genericproduct ADD unique_product_id varchar(255);

COMMIT;



BEGIN;

UPDATE catalogue_genericproduct SET unique_product_id = original_product_id;

-- update SPOT5 products
UPDATE catalogue_genericproduct SET
    unique_product_id = substring(
        original_product_id from 0 for length(original_product_id)
    )||dictionaries_spectralmode.abbreviation
FROM
  dictionaries_opticalproductprofile,
  catalogue_opticalproduct,
  dictionaries_spectralmode
WHERE
  catalogue_opticalproduct.genericsensorproduct_ptr_id = catalogue_genericproduct.id AND
  catalogue_opticalproduct.product_profile_id = dictionaries_opticalproductprofile.id AND
  dictionaries_spectralmode.id = dictionaries_opticalproductprofile.spectral_mode_id AND
  catalogue_opticalproduct.product_profile_id IN (13,14,15,16,17,18,19,20);

-- update lansat5

-- ?

COMMIT;



BEGIN;

ALTER TABLE catalogue_genericproduct ALTER unique_product_id SET NOT NULL;
ALTER TABLE catalogue_genericproduct
    ADD CONSTRAINT unique_product_id UNIQUE (unique_product_id);

-- drop product_id column
ALTER TABLE catalogue_genericproduct DROP product_id CASCADE;
COMMIT;