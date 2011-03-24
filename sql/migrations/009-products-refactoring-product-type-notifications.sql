-- ######################################################################
--
-- Migration script for the new OrderNotificationRecipients product type
--
--
-- ######################################################################


BEGIN;

  CREATE TABLE "catalogue_ordernotificationrecipients_classes" (
      "id" serial NOT NULL PRIMARY KEY,
      "ordernotificationrecipients_id" integer NOT NULL,
      "contenttype_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED,
      UNIQUE ("ordernotificationrecipients_id", "contenttype_id")
  );

  ALTER TABLE "catalogue_ordernotificationrecipients_classes" ADD CONSTRAINT "ordernotificationrecipients_id_refs_id_2af58da6" FOREIGN KEY ("ordernotificationrecipients_id") REFERENCES "catalogue_ordernotificationrecipients" ("id") DEFERRABLE INITIALLY DEFERRED;



COMMIT;