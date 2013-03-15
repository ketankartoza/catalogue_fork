BEGIN;

ALTER TABLE "catalogue_taskingrequest" ADD
    "satellite_id" integer REFERENCES "dictionaries_satellite" ("id") DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE "catalogue_taskingrequest" ADD
    "instrument_type_id" integer REFERENCES "dictionaries_instrumenttype" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;



BEGIN;

UPDATE "catalogue_taskingrequest" SET satellite_id=15, instrument_type_id=1
    WHERE mission_sensor_id = 2;

UPDATE "catalogue_taskingrequest" SET satellite_id=7, instrument_type_id=5
    WHERE mission_sensor_id = 5;

UPDATE "catalogue_taskingrequest" SET satellite_id=12, instrument_type_id=8
    WHERE mission_sensor_id = 10;

UPDATE "catalogue_taskingrequest" SET satellite_id=1, instrument_type_id=2
    WHERE mission_sensor_id = 13;

UPDATE "catalogue_taskingrequest" SET satellite_id=13, instrument_type_id=9
    WHERE mission_sensor_id = 14;

UPDATE "catalogue_taskingrequest" SET satellite_id=14, instrument_type_id=10
    WHERE mission_sensor_id = 15;

UPDATE "catalogue_taskingrequest" SET satellite_id=6, instrument_type_id=4
    WHERE mission_sensor_id = 16;

UPDATE "catalogue_taskingrequest" SET satellite_id=3, instrument_type_id=3
    WHERE mission_sensor_id = 17;

UPDATE "catalogue_taskingrequest" SET satellite_id=4, instrument_type_id=3
    WHERE mission_sensor_id = 18;

UPDATE "catalogue_taskingrequest" SET satellite_id=5, instrument_type_id=3
    WHERE mission_sensor_id = 19;

UPDATE "catalogue_taskingrequest" SET satellite_id=6, instrument_type_id=3
    WHERE mission_sensor_id = 20;

UPDATE "catalogue_taskingrequest" SET satellite_id=8, instrument_type_id=6
    WHERE mission_sensor_id = 21;

UPDATE "catalogue_taskingrequest" SET satellite_id=9, instrument_type_id=6
    WHERE mission_sensor_id = 22;

UPDATE "catalogue_taskingrequest" SET satellite_id=10, instrument_type_id=6
    WHERE mission_sensor_id = 23;

UPDATE "catalogue_taskingrequest" SET satellite_id=11, instrument_type_id=7
    WHERE mission_sensor_id = 24;

COMMIT;


BEGIN;
ALTER TABLE "catalogue_taskingrequest"
    ALTER "satellite_id" SET NOT NULL;

ALTER TABLE "catalogue_taskingrequest"
    ALTER "instrument_type_id" SET NOT NULL;

COMMIT;
