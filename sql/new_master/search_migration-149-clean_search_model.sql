BEGIN;

-- delete radar searches

delete from search_search_instrumenttype where search_id = (select id from search_search where  acquisition_mode_id = 2);
delete from search_searchdaterange where search_id = (select id from search_search where  acquisition_mode_id = 2);
delete from search_search where  acquisition_mode_id = 2;


-- drop unused attributes

ALTER TABLE "search_search" DROP COLUMN search_type;
ALTER TABLE "search_search" DROP COLUMN keywords;
ALTER TABLE "search_search" DROP COLUMN polarising_mode;
ALTER TABLE "search_search" DROP COLUMN mission_id CASCADE;
ALTER TABLE "search_search" DROP COLUMN sensor_type_id CASCADE;
ALTER TABLE "search_search" DROP COLUMN acquisition_mode_id CASCADE;


-- drop old unsed table

DROP TABLE search_search_sensors CASCADE;

COMMIT;