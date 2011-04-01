-- ######################################################################
--
-- Migration script for new search record fields related to DIMS OS4Eo
--
--
-- ######################################################################

BEGIN;

  -- Postgresql handles foreign keys in internal triggers. Settings all these triggers for
  -- immediate execution avoid pending triggers errors
  SET CONSTRAINTS ALL IMMEDIATE;

  ALTER TABLE "catalogue_searchrecord" ADD "product_ready" boolean;
  ALTER TABLE "catalogue_searchrecord" ADD "internal_order_id" INTEGER;

  UPDATE "catalogue_searchrecord" SET "product_ready" = 'f' FROM "catalogue_genericproduct"
    WHERE "catalogue_genericproduct"."local_storage_path" IS NOT NULL
    AND "catalogue_genericproduct"."local_storage_path" != ''
    AND "catalogue_searchrecord"."product_id" = "catalogue_genericproduct"."id";

  UPDATE "catalogue_searchrecord" SET "product_ready" = 't' FROM "catalogue_genericproduct"
    WHERE ("catalogue_genericproduct"."local_storage_path" IS NULL
    OR "catalogue_genericproduct"."local_storage_path" = '')
    AND "catalogue_searchrecord"."product_id" = "catalogue_genericproduct"."id";

  ALTER TABLE "catalogue_searchrecord" ADD "download_path" VARCHAR(512);

  ALTER TABLE "catalogue_searchrecord" ALTER "product_ready" SET NOT NULL;

--ROLLBACK;
COMMIT;

