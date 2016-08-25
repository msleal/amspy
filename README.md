#### Simple Python Library for Azure Media Services REST API
The amspy is a library to provide a simple Azure Media Services REST interface for python. This is a personal project and NOT an official implementation of the Azure Media Services SDK for python. The only purpose of this library is for educational purposes, so people can have an easy way to understand how to interact with cloud REST apis, and learn from the examples provided in this module as well as the debug information available in the logs. Any feedback, comments or bugs, please send directly to the module owner, and go to https://azure.microsoft.com if you are looking for official Microsoft Azure SDKs.

```
get_access_token(accountname, accountkey) - get the access token/authenticate
list_media_asset(access_token, oid) - list media asset
list_content_key(access_token, oid) - list sas locator
list_media_processor(access_token, oid) - list media processor
list_asset_accesspolicy(access_token, oid) - list asset acess policy
list_sas_locator(access_token, oid) - list sas locator
delete_asset_accesspolicy(access_token, oid) - delete an asset acess policy
delete_sas_locator(access_token, oid) - delete a sas locator
delete_content_key(access_token, oid) - delete an asset acess policy
delete_media_asset(access_token, oid) - delete an asset
create_media_asset(access_token, name) - create a media asset
create_media_assetfile(access_token, parent_asset_id, name, is_encrypted, is_primary) - create a media assetfile
create_sas_locator(access_token, asset_id, accesspolicy_id) - create a sas url locator
create_media_task(access_token, name, processor_id, asset_id, content) - create a media task
create_media_job(access_token, name, job_definition, processor_id, asset_id, task_body) -create a job
update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name) - update assetfile content length
set_asset_accesspolicy(access_token, duration) - set the asset access policy
upload_block_blob(access_token, endpoint, content, content_length) - upload a file as a block blob
validate_mp4_asset(access_token, processor_id, asset_id, output_assetname) - validade an encoded MP4 asset
```
