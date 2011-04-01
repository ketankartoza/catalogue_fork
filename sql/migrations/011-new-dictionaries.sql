CREATE TABLE "catalogue_topic" (
    "id" serial NOT NULL PRIMARY KEY,
    "abbreviation" varchar(10) NOT NULL UNIQUE,
    "name" varchar(255) NOT NULL UNIQUE
)
;
CREATE TABLE "catalogue_placetype" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL UNIQUE
)
;
CREATE TABLE "catalogue_place" (
    "id" serial NOT NULL PRIMARY KEY,
    "name" varchar(255) NOT NULL,
    "place_type_id" integer NOT NULL REFERENCES "catalogue_placetype" ("id") DEFERRABLE INITIALLY DEFERRED
)
;
CREATE TABLE "catalogue_unit" (
    "id" serial NOT NULL PRIMARY KEY,
    "abbreviation" varchar(10) NOT NULL UNIQUE,
    "name" varchar(255) NOT NULL UNIQUE
)
;
