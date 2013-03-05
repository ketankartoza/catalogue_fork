BEGIN;

-- insert instrument types

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 1 FROM search_search_sensors WHERE missionsensor_id=2;

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 2 FROM search_search_sensors WHERE missionsensor_id=13;

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT DISTINCT search_id, 3 FROM search_search_sensors WHERE missionsensor_id IN (17,18,19,20);

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 4 FROM search_search_sensors WHERE missionsensor_id=16;

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 5 FROM search_search_sensors WHERE missionsensor_id=5;

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT DISTINCT search_id, 6 FROM search_search_sensors WHERE missionsensor_id IN (21,22,23);

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 7 FROM search_search_sensors WHERE missionsensor_id=24;

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 8 FROM search_search_sensors WHERE missionsensor_id=10;

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 9 FROM search_search_sensors WHERE missionsensor_id=14;

INSERT INTO "search_search_instrumenttype" (search_id, instrumenttype_id)
    SELECT search_id, 10 FROM search_search_sensors WHERE missionsensor_id=15;

-- update satellite (was mission)

UPDATE search_search SET satellite_id = 1
WHERE mission_id= 19;

UPDATE search_search SET satellite_id = 2
WHERE mission_id= 23;

UPDATE search_search SET satellite_id = 3
WHERE mission_id= 12;

UPDATE search_search SET satellite_id = 4
WHERE mission_id= 13;

UPDATE search_search SET satellite_id = 5
WHERE mission_id= 14;

UPDATE search_search SET satellite_id = 6
WHERE mission_id= 10;

UPDATE search_search SET satellite_id = 7
WHERE mission_id= 11;

UPDATE search_search SET satellite_id = 8
WHERE mission_id= 17;

UPDATE search_search SET satellite_id = 9
WHERE mission_id= 15;

UPDATE search_search SET satellite_id = 10
WHERE mission_id= 22;

UPDATE search_search SET satellite_id = 11
WHERE mission_id= 16;

UPDATE search_search SET satellite_id = 12
WHERE mission_id= 18;

UPDATE search_search SET satellite_id = 13
WHERE mission_id= 20;

UPDATE search_search SET satellite_id = 14
WHERE mission_id= 21;

UPDATE search_search SET satellite_id = 15
WHERE mission_id= 9;



-- update spectralmode (was sensor_type)

UPDATE search_search SET spectral_mode_id = 25
WHERE sensor_type_id = 6;

UPDATE search_search SET spectral_mode_id = 31
WHERE sensor_type_id = 8;

UPDATE search_search SET spectral_mode_id = 20
WHERE sensor_type_id IN (26,29,32);

UPDATE search_search SET spectral_mode_id = 17
WHERE sensor_type_id = 36;

UPDATE search_search SET spectral_mode_id = 14
WHERE sensor_type_id = 40;

UPDATE search_search SET spectral_mode_id = 15
WHERE sensor_type_id = 41;

UPDATE search_search SET spectral_mode_id = 16
WHERE sensor_type_id = 42;

UPDATE search_search SET spectral_mode_id = 13
WHERE sensor_type_id = 44;

UPDATE search_search SET spectral_mode_id = 6
WHERE sensor_type_id IN (174, 175, 176, 177);

UPDATE search_search SET spectral_mode_id = 4
WHERE sensor_type_id = 178;

UPDATE search_search SET spectral_mode_id = 1
WHERE sensor_type_id = 179;

UPDATE search_search SET spectral_mode_id = 19
WHERE sensor_type_id IN (182, 184, 187);

UPDATE search_search SET spectral_mode_id = 18
WHERE sensor_type_id = 185;

COMMIT;