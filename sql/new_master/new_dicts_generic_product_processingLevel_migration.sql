alter table catalogue_genericproduct drop column processing_level_id;
alter table catalogue_genericproduct add column processing_level_id int null
    references dictionaries_processinglevel(id);
update catalogue_genericproduct SET processing_level_id = 1;

-- Linda to update dicts with proper base processing level on InstrumentType
-- Then all products should be updated to have their processing level set
-- to the product profile base processing level.
