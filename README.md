## Simple Python Library for Azure Media Services REST API
The amspy is a library to provide a simple Azure Media Services REST interface for python. This is a personal project and NOT an official implementation of the Azure Media Services SDK for python. The only purpose of this library is for educational purposes, so people can have an easy way to understand how to interact with cloud REST apis, and learn from the examples provided in this module as well as the debug information available in the logs. Any feedback, comments or bugs, please send directly to the module owner, and go to https://azure.microsoft.com if you are looking for official Microsoft Azure SDKs.

### Using AMSPy
A detailed set of **amspy** programming examples can be found here: <a href="https://github.com/msleal/amspy/tree/master/amspy/examples">AMSPy Python library programming examples</a>.

#### Listing Media Assets:
```
import os
import json
import amspy

# Load Azure app defaults
try:
        with open('config.json') as configFile:
                configData = json.load(configFile)
except FileNotFoundError:
        print("ERROR: Expecting config.json in current folder")
        sys.exit()

account_name = configData['accountName']
account_key = configData['accountKey']

# Get the access token...
response = amspy.get_access_token(account_name, account_key)
resjson = response.json()
access_token = resjson["access_token"]

### list media assets
response = amspy.list_media_asset(access_token)
if (response.status_code == 200):
        resjson = response.json()
        print("POST Status.............................: " + str(response.status_code))
        for ma in resjson['d']['results']:
                print("Media Asset Name........................: " + ma['Id'])
                print("Media Asset Id..........................: " + ma['Name'])
else:
        print("GET Status: " + str(response.status_code) + " ERROR:" + str(response.content))
```
### Azure Media Analytics Usage Sample Scripts
A set of scripts that show how to use Azure Media Analytics is available in the amspy/examples/Analytics folder. 
In this folder you will find examples of the following analytics tools:

- Face Detection
- Face Redaction
- Hyperlapse
- Indexer v1
- Indexer v2 (Preview)
- Motion Detection
- OCR
- Video Thumbnail

Each of the samples includes a single Python script and configuration file for the processor.
Simply execute the python script to process a source file. 
To modify the source file used, edit the global variable and change the 
VIDEO_PATH to point to your source file. 

The script will execute and download the output results of the Media Analytics job into the "output" folder in the example.
You can modify the settings files for each processor to adjust the output results.

For additional documentation about Azure Media Analytics, plese refer to the page http://aka.ms/mediaanalytics

Please contact us on Twitter -  @MSFTAzureMedia - if you have any questions.

### AMSPy Library Functions:
```
add_authorization_policy(access_token, ck_id, oid) - add authorization policy to key
create_asset_accesspolicy(access_token, name, duration, permission="1") - create an asset access policy
create_asset_delivery_policy(access_token, ams_account) - create asset delivery policy
create_contentkey_authorization_policy(access_token, content) - create contenty key authorization policy
create_contentkey_authorization_policy_options(access_token, key_delivery_type="2", name="HLS Open Authorization Policy", key_restriction_type="0") - create content key authorization policy options
create_media_asset(access_token, name, options="0") - create a media asset
create_media_assetfile(access_token, parent_asset_id, name, is_primary="false", is_encrypted="false", encryption_scheme="None", encryptionkey_id="None") - create a media assetfile
create_media_job(access_token, name, job_definition, processor_id, asset_id, task_body) -create a job
create_media_task(access_token, name, processor_id, asset_id, content) - create a media task
create_ondemand_streaming_locator(access_token, encoded_asset_id, pid, starttime=None) - create on-demand streaming locator
create_sas_locator(access_token, asset_id, accesspolicy_id) - create a sas url locator
create_streaming_endpoint(access_token, name, description="New Streaming Endpoint", scale_units="1") - create a streaming endpoint
delete_asset_accesspolicy(access_token, oid) - delete an asset acess policy
delete_asset_delivery_policy(access_token, oid) - delete media asset delivery policy
delete_content_key(access_token, oid) - delete an asset acess policy
delete_contentkey_authorization_policy(access_token, oid) - delete content key authorization policy
delete_contentkey_authorization_policy_options(access_token, oid) - delete content key authorization policy options
delete_media_asset(access_token, oid) - delete an asset
delete_sas_locator(access_token, oid) - delete a sas locator
delete_streaming_endpoint(access_token, oid) - delete a streaming endpoint
encode_mezzanine_asset(access_token, processor_id, asset_id, output_assetname, json_profile) - encode a mezzanine (raw video) file into multi-bitrate MP4 video asset
get_access_token(accountname, accountkey) - get the access token/authenticate
get_delivery_url(access_token, ck_id, key_type) - get the key delivery url
get_url(access_token, endpoint=ams_rest_endpoint, flag=True) - get a specific url
link_asset_content_key(access_token, asset_id, encryptionkey_id, ams_redirected_rest_endpoint) - link a content key with a media asset
link_asset_delivery_policy(access_token, asset_id, adp_id, ams_redirected_rest_endpoint) - link asset to delivery policy
link_contentkey_authorization_policy(access_token, ckap_id, options_id, ams_redirected_rest_endpoint) - link content key authorization policy
list_asset_accesspolicy(access_token, oid="") - list asset access policy
list_asset_delivery_policy(access_token, oid="") - list media asset delivery policy(ies)
list_content_key(access_token, oid="") - list content key(s)
list_contentkey_authorization_policy(access_token, oid="") - list content key authorization policy(ies)
list_contentkey_authorization_policy_options(access_token, oid="") - list content key authorization policy options
list_media_asset(access_token, oid="") - list media asset(s)
list_media_job(access_token, oid="") - list media job(s)
list_media_processor(access_token, oid="") - list media processor(s)
list_sas_locator(access_token, oid="") - list sas locator(s)
list_streaming_endpoint(access_token, oid="") - list streaming endpoint(s)
retrieve_url_content(url) - get a specific url
scale_streaming_endpoint(access_token, streaming_endpoint_id, scale_units) - scale a streaming endpoint
translate_asset_options(nr) - translate the numeric configuration options of the asset to a human readable form
translate_job_state(nr) - translate the numeric job state to a human readable form
update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name) - update assetfile content length
upload_block_blob(access_token, endpoint, content, content_length) - upload a file as a block blob
validate_mp4_asset(access_token, processor_id, asset_id, output_assetname) - validade an encoded multi-bitrate MP4 asset
```
