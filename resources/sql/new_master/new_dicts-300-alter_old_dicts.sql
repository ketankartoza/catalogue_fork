BEGIN;

ALTER TABLE catalogue_projection RENAME TO dictionaries_projection;
ALTER TABLE catalogue_institution RENAME TO dictionaries_institution;
alter TABLE catalogue_license RENAME to dictionaries_license;

COMMIT;
