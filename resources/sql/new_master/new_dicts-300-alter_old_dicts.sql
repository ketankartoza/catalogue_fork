BEGIN;

ALTER TABLE catalogue_projection RENAME TO dictionaries_projection;
ALTER TABLE catalogue_institution RENAME TO dictionaries_institution;
ALTER TABLE catalogue_license RENAME to dictionaries_license;
ALTER TABLE catalogue_quality RENAME to dictionaries_quality;
ALTER TABLE catalogue_topic RENAME TO dictionaries_topic;

COMMIT;
