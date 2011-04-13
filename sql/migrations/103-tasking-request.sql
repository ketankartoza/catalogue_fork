BEGIN;

-- move geometry from tasking request to delivery details

UPDATE catalogue_deliverydetail SET geometry = a.geometry
FROM catalogue_taskingrequest a INNER JOIN catalogue_order b ON a.order_ptr_id=b.id WHERE catalogue_deliverydetail.id=b.delivery_detail_id;

ALTER TABLE catalogue_taskingrequest DROP geometry;

COMMIT;
