BEGIN;

ALTER TABLE catalogue_projection RENAME TO dictionaries_projection;
ALTER TABLE catalogue_institution RENAME TO dictionaries_institution;

COMMIT;
