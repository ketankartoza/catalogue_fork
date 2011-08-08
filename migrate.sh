#!/bin/bash
echo "This script does a complete migrations from the V1 catalogue to v2"
echo "Tim Sutton 2011"
echo "Example usage: $0 [pg password]"

export PGPORT=5432
export PGHOST=elephant
DB=sac-test
if [ -z $1 ]
then
 export PGPASS=$1
fi
source ../python/bin/activate
psql $DB -f sql/migrations/001-new-generic-sensor-product.sql
psql $DB -f sql/migrations/002-additional-fields-for-geospatialproduct.sql
psql $DB -f sql/migrations/003-additional_fields_for_advanced_search.sql
psql $DB -f sql/migrations/004-products-aggregations.sql
psql $DB -f sql/migrations/005-dims-ingestion.sql
psql $DB -f sql/migrations/006-products-refactoring.sql
psql $DB -f sql/migrations/007-products_refactoring-2.sql
psql $DB -f sql/migrations/008-products-refactoring-license-type.sql
psql $DB -f sql/migrations/009-products-refactoring-product-type-notifications.sql
psql $DB -f sql/migrations/010-search-refactoring.sql
psql $DB -f sql/migrations/011-new-dictionaries.sql
psql $DB -f sql/migrations/012-products-refactoring-continuous-ordinal.sql
psql $DB -f sql/migrations/013-products-refactoring-radar-geospatial.sql
psql $DB -f sql/migrations/014-model-fixes.sql
psql $DB -f sql/migrations/015-search-record-ordering-fields.sql
psql $DB -f sql/migrations/100-orders-deliverydetails.sql
psql $DB -f sql/migrations/101-deliverydetail-geometry.sql
psql $DB -f sql/migrations/102-projections-insert.sql
psql $DB -f sql/migrations/103-tasking-request.sql
psql $DB -f sql/migrations/200-heatmap-reporting.sql
psql $DB -f sql/migrations/200-placetype.sql
psql $DB -f sql/migrations/201-heatmap-bootstrap.sql
psql $DB -f sql/migrations/202-report-query-by-country.sql
python manage.py runscript --pythonpath=scripts -v 2 load_world_borders
psql $DB -f sql/migrations/203-worldborders-data-sanitization.sql
psql $DB -f sql/migrations/300-sensors-dictionaries-refactoring-before.sql
python manage.py runscript -s -v 2 --pythonpath=./sql/migrations 301-sensors-dictionaries-refactoring-import.py
psql $DB -f sql/migrations/302-sensors-dictionaries-refactoring-after.sql
python manage.py runscript -s -v 2 --pythonpath=./sql/migrations 303-sensors-dictionaries-add-spot-modes.py
python manage.py runscript -v 2 --pythonpath=./sql/migrations post_migration.py
psql $DB -f sql/migrations/304-additional-indexes.sql
psql $DB -f sql/migrations/305-taskable-sensors.sql
psql $DB -f sql/migrations/306-order-market-sector.sql
psql $DB -f sql/migrations/307-permissions.sql
# Next adds teh catalogue.ProductLink model
python manage.py syncdb
python manage.py reverse-engineer-product-ids -v 2
