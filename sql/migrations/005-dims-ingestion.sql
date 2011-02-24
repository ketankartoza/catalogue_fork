-- ######################################################################
--
-- Migration script for the DIMS ingestion
--
-- mainly DROP NOT NULL for missing fields in metadata
--
-- ######################################################################


BEGIN;

  -- drop "L"  from processing level
  update catalogue_processinglevel set abbreviation = regexp_replace(abbreviation, '^L', '') where true;


COMMIT;