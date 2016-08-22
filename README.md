#### Simple Python Library for Azure Media Services REST API
```
get_access_token(account_name, account_key) - get the access token/authenticate
create_media_asset(access_token, name) - create a media asset
list_media_asset(access_token, asset_id) - list a media asset
create_media_assetfile(access_token, asset_id, name, is_encrypted, is_primary) - create a media assetfile
set_asset_accesspolicy(access_token, duration) - set the asset access policy
list_asset_accesspolicy(access_token) - list an asset access policy
create_sas_locator(access_token, asset_id, accesspolicy_id) - create a sas url locator for upload
list_sas_locator(access_token) - list a sas locator
upload_block_blob(access_token, endpoint, content, content_length) - upload a file as a block blob 
update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name) - update assetfile content length
delete_sas_locator(access_token, saslocator_id) - delete a sas locator
delete_asset_accesspolicy(access_token, accesspolicy_id) - delete an asset access policy
```
