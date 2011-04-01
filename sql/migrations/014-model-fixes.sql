-- ######################################################################
--
-- Migration script for various fixes
--
--
-- ######################################################################

BEGIN;

  -- Postgresql handles foreign keys in internal triggers. Settings all these triggers for
  -- immediate execution avoid pending triggers errors
  SET CONSTRAINTS ALL IMMEDIATE;


  -- add unique constraint to Search.guid
  ALTER TABLE "catalogue_search" ADD UNIQUE("guid");
  ALTER TABLE "catalogue_search" ADD "record_count" INTEGER;

  -- add indexes to improve search performances
  CREATE INDEX "catalogue_genericsensorproduct_geometric_accuracy_mean" ON "catalogue_genericsensorproduct" ("geometric_accuracy_mean");
  CREATE INDEX "catalogue_genericsensorproduct_path" ON "catalogue_genericsensorproduct" ("path");
  CREATE INDEX "catalogue_genericsensorproduct_row" ON "catalogue_genericsensorproduct" ("row");

--ROLLBACK;
COMMIT;

