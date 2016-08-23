#### Simple Python Library for Azure Media Services REST API
```
get_access_token(accountname, accountkey) - get the access token/authenticate
list_media_asset(access_token, oid) - list media asset
list_media_processor(access_token, oid) - list media processor
list_asset_accesspolicy(access_token, oid) - list asset acess policy
list_sas_locator(access_token, oid) - list sas locator
create_media_asset(access_token, name) - create a media asset
create_media_assetfile(access_token, parent_asset_id, name, is_encrypted, is_primary) - create a media assetfile
create_sas_locator(access_token, asset_id, accesspolicy_id) - create a sas url locator
create_media_job(access_token, name, job_definition, processor_id, asset_id, task_body) -create a job
update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name) - update assetfile content length
set_asset_accesspolicy(access_token, duration) - set the asset access policy
delete_asset_accesspolicy(access_token, accesspolicy_id) - delete an asset acess policy
delete_sas_locator(access_token, saslocator_id) - delete a sas locator
upload_block_blob(access_token, endpoint, content, content_length) - upload a file as a block blob
```
