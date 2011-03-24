--
-- RUN THIS SCRIPT ONLY AFTER POPULATING catalogue_worldborders TABLE
--
-- see sql/migrations/202-script...
BEGIN;

-- world borders data sanitization, needed for PISA PDF report encoding
UPDATE catalogue_worldborders set name = replace(name,'''','');
UPDATE catalogue_worldborders set name = replace(name,' (',', ');
UPDATE catalogue_worldborders set name = replace(name,')','');

COMMIT;