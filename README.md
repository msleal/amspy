#### Simple Python Library for Azure Media Services REST API
The amspy is a library to provide a simple Azure Media Services REST interface for python. This is a personal project and NOT an official implementation of the Azure Media Services SDK for python. The only purpose of this library is for educational purposes, so people can have an easy way to understand how to interact with cloud REST apis, and learn from the examples provided in this module as well as the debug information available in the logs. Any feedback, comments or bugs, please send directly to the module owner, and go to https://azure.microsoft.com if you are looking for official Microsoft Azure SDKs.

```
get_access_token(accountname, accountkey) - get the access token/authenticate
get_url(access_token, endpoint=ams_rest_endpoint, flag=True) - get a specific url
list_media_asset(access_token, oid="") - list media asset(s)
list_content_key(access_token, oid="") - list content key(s)
list_media_processor(access_token, oid="") - list media processor(s)
list_asset_accesspolicy(access_token, oid="") - list asset access policy
list_sas_locator(access_token, oid="") - list sas locator(s)
list_media_job(access_token, oid="") - list media job(s)
delete_asset_accesspolicy(access_token, oid) - delete an asset acess policy
delete_sas_locator(access_token, oid) - delete a sas locator
delete_content_key(access_token, oid) - delete an asset acess policy
delete_media_asset(access_token, oid) - delete an asset
create_media_asset(access_token, name, options="0") - create a media asset
create_media_assetfile(access_token, parent_asset_id, name, is_primary="false", is_encrypted="false", encryption_scheme="None", encryptionkey_id="None") - create a media assetfile
create_sas_locator(access_token, asset_id, accesspolicy_id) - create a sas url locator
create_asset_delivery_policy(access_token, ams_account) - create asset delivery policy
create_media_task(access_token, name, processor_id, asset_id, content) - create a media task
create_media_job(access_token, name, job_definition, processor_id, asset_id, task_body) -create a job
create_contentkey_authorization_policy(access_token, content) - create contenty key authorization policy
create_contentkey_authorization_policy_options(access_token, key_delivery_type="2", name="HLS Open Authorization Policy", key_restriction_type="0") - create content key authorization policy options
create_ondemand_streaming_locator(access_token, encoded_asset_id, pid, starttime=None) - create on-demand streaming locator
create_asset_accesspolicy(access_token, name, duration, permission="1") - create an asset access policy
link_asset_content_key(access_token, asset_id, encryptionkey_id, ams_redirected_rest_endpoint) - link a content key with a media asset
link_asset_delivery_policy(access_token, asset_id, adp_id, ams_redirected_rest_endpoint) - link asset to delivery policy
link_contentkey_authorization_policy(access_token, ckap_id, options_id, ams_redirected_rest_endpoint) - link content key authorization policy
add_authorization_policy(access_token, ck_id, oid) - add authorization policy to key
update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name) - update assetfile content length
get_delivery_url(access_token, ck_id, key_type) - get the key delivery url
upload_block_blob(access_token, endpoint, content, content_length) - upload a file as a block blob
validate_mp4_asset(access_token, processor_id, asset_id, output_assetname) - validade an encoded MP4 asset
upload_block_blob(access_token, endpoint, content, content_length) - upload file as a block blob
```
