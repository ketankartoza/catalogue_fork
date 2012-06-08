-- sample 1000 optical products
-- after execution, termporary add 'db_table' to Meta class
-- for each of the four models in catalogue/models/products.py
-- run, for each of four models
-- python manage.py dumpdata --format=json --indent=4 catalogue.genericproduct > catalogue/fixtures/test_genericproduct.json

-- manually drop creted tables after data export

drop table sample_opticalproduct;

create table sample_opticalproduct AS 
SELECT * from catalogue_opticalproduct
ORDER BY random()
LIMIT 1000;

-- for that 1000 products create parent tables
drop table sample_genericsensorproduct;
create table sample_genericsensorproduct AS
select b.* from sample_opticalproduct a inner join catalogue_genericsensorproduct b
ON  a.genericsensorproduct_ptr_id = b.genericimageryproduct_ptr_id;


drop table sample_genericimageryproduct;
create table sample_genericimageryproduct AS
select b.* from sample_genericsensorproduct a inner join catalogue_genericimageryproduct b
ON  a.genericimageryproduct_ptr_id = b.genericproduct_ptr_id;

drop table sample_genericproduct;
create table sample_genericproduct AS
select b.* from sample_genericimageryproduct a inner join catalogue_genericproduct b
ON  a.genericproduct_ptr_id = b.id;
