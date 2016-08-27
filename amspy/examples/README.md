### Upload and Valiate a MP4 Video
This example does the complete workflow from upload an already encode MP4 file,
and validate it with the Azure Media Packager. This example also link a Content key
with the Encoded Asset, so we can use AES dynamic encryption to deliver the content (e.g.: HLS).
```
response = amspy.get_redirected_url(access_token)
response = amspy.list_content_key(access_token)
response = amspy.create_media_asset(access_token, NAME)
response = amspy.list_media_asset(access_token, asset_id)
response = amspy.create_media_assetfile(access_token, asset_id, VIDEO_NAME, "false", "true")
response = amspy.create_media_assetfile(access_token, asset_id, ISM_NAME, "true", "true")
response = amspy.set_asset_accesspolicy(access_token, duration)
response = amspy.list_asset_accesspolicy(access_token)
response = amspy.create_sas_locator(access_token, asset_id, accesspolicy_id)
response = amspy.list_sas_locator(access_token)
response = amspy.upload_block_blob(access_token, saslocator_video_url, video_content, video_content_length)
response = amspy.upload_block_blob(access_token, saslocator_ism_url, ism_content, ism_content_length)
response = amspy.update_media_assetfile(access_token, asset_id, video_assetfile_id, video_content_length, VIDEO_NAME)
response = amspy.update_media_assetfile(access_token, asset_id, ism_assetfile_id, ism_content_length, ISM_NAME)
response = amspy.link_content_key(access_token, asset_id, encryptionkey_id, ams_redirected_rest_endpoint)
response = amspy.delete_sas_locator(access_token, saslocator_id)
response = amspy.delete_asset_accesspolicy(access_token, accesspolicy_id)
response = amspy.list_media_processor(access_token)
response = amspy.validate_mp4_asset(access_token, processor_id, asset_id, "mp4validated")
response = amspy.list_media_job(access_token, job_id)
response = amspy.delete_media_asset(access_token, asset_id)
```
