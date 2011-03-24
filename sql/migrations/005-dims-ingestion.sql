-- ######################################################################
--
-- Migration script for the DIMS ingestion
--
-- mainly DROP NOT NULL for missing fields in metadata
--
-- ######################################################################


BEGIN;

  alter table catalogue_genericsensorproduct alter spectral_resolution drop not null;
  alter table catalogue_genericsensorproduct alter radiometric_resolution drop not null;
  alter table catalogue_genericproduct alter remote_thumbnail_url drop not null;


COMMIT;