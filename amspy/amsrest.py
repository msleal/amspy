"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Rest Python library
License: MIT (see LICENSE.txt file for details)
"""

# amsrest.py - azurerm functions for the AMS Rest Interface

import urllib
import requests
from .restfns import do_auth, do_get, do_post, do_put, do_delete, do_patch, do_sto_put, do_get_url
from .settings import ams_rest_endpoint, ams_auth_endpoint

# get_access_token(accountname, accountkey)
# get access token with ams
def get_access_token(accountname, accountkey):
    accountkey_encoded = urllib.parse.quote(accountkey, safe='')
    body = "grant_type=client_credentials&client_id=" + accountname + "&client_secret=" + accountkey_encoded + " &scope=urn%3aWindowsAzureMediaServices"
    return do_auth(ams_auth_endpoint, body)

# get_url(access_token)
# get an specific url
def get_url(access_token, endpoint=ams_rest_endpoint, flag=True):
    return do_get_url(endpoint, access_token, flag)

# list_media_asset(access_token, oid)
# list a media asset(s)
def list_media_asset(access_token, oid=""):
    path = '/Assets'
    return helper_list(access_token, oid, path)

# list_content_keys(access_token, oid)
# list the content key(s)
def list_content_key(access_token, oid=""):
    path = '/ContentKeys'
    return helper_list(access_token, oid, path)

# list_media_processor(access_token, oid)
# list the media processor(s)
def list_media_processor(access_token, oid=""):
    path = '/MediaProcessors'
    return helper_list(access_token, oid, path)

# list_asset_accesspolicy(access_token, oid)
# list a asset access policy(ies)
def list_asset_accesspolicy(access_token, oid=""):
    path = '/AccessPolicies'
    return helper_list(access_token, oid, path)

# list_sas_locator(access_token, oid)
# list a sas locator(s)
def list_sas_locator(access_token, oid=""):
    path = '/Locators'
    return helper_list(access_token, oid, path)

# list_media_job(access_token, oid)
# list a media job(s)
def list_media_job(access_token, oid=""):
    path = '/Jobs'
    return helper_list(access_token, oid, path)

# delete_asset_accesspolicy(access_token, oid)
# delete a asset access policy
def delete_asset_accesspolicy(access_token, oid):
    path = '/AccessPolicies'
    return helper_delete(access_token, oid, path)

# delete_sas_locator(access_token, oid)
# delete a sas locator
def delete_sas_locator(access_token, oid):
    path = '/Locators'
    return helper_delete(access_token, oid, path)

# delete_content_key(access_token, oid)
# delete a content key
def delete_content_key(access_token, oid):
    path = '/ContentKeys'
    return helper_delete(access_token, oid, path)

# delete_media_asset(access_token, oid)
# delete a media asset
def delete_media_asset(access_token, oid):
    path = '/Assets'
    return helper_delete(access_token, oid, path)

# create_media_asset(access_token, name, options="0")
# create a media asset
def create_media_asset(access_token, name, options="0"):
    path = '/Assets'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{"Name": "' + name + '", "Options": "' + str(options) + '"}'
    return do_post(endpoint, path, body, access_token)

# create_media_assetfile(access_token, parent_asset_id, name, is_primary="false", is_encrypted="false", encryption_scheme="None", encryptionkey_id="None")
# create a media assetfile
def create_media_assetfile(access_token, parent_asset_id, name, is_primary="false", is_encrypted="false", encryption_scheme="None", encryptionkey_id="None"):
    path = '/Files'
    endpoint = ''.join([ams_rest_endpoint, path])
    if (encryption_scheme == "StorageEncryption"):
    	body = '{"IsEncrypted": "' + is_encrypted + '", "EncryptionScheme": "' + encryption_scheme + '", "EncryptionVersion": "' + "1.0" + '", "EncryptionKeyId": "' + encryptionkey_id + '", "IsPrimary": "' + is_primary + '", "MimeType": "video/mp4", "Name": "' + name + '", "ParentAssetId": "' + parent_asset_id + '"}'
    else:
    	body = '{"IsPrimary": "' + is_primary + '", "MimeType": "video/mp4", "Name": "' + name + '", "ParentAssetId": "' + parent_asset_id + '"}'
    return do_post(endpoint, path, body, access_token)

# create_sas_locator(access_token, asset_id, accesspolicy_id)
# create a sas locator
def create_sas_locator(access_token, asset_id, accesspolicy_id):
    path = '/Locators'
    endpoint = ''.join([ams_rest_endpoint, path])
    #body = '{"AccessPolicyId":"' + accesspolicy_id + '", "AssetId":"' + asset_id + '", "StartTime":"' + starttime + '", "Type":1 }'
    body = '{"AccessPolicyId":"' + accesspolicy_id + '", "AssetId":"' + asset_id + '", "Type":1 }'
    return do_post(endpoint, path, body, access_token)

# create_media_task(access_token, processor_id, asset_id, content)
# create a media task
def create_media_task(access_token, processor_id, asset_id, content):
    path = '/Tasks'
    endpoint = ''.join([ams_rest_endpoint, path])

    body = content
    return do_post(endpoint, path, body, access_token)

# create_media_job(access_token, processor_id, asset_id, content)
# create a media job
def create_media_job(access_token, processor_id, asset_id, content):
    path = '/Jobs'
    endpoint = ''.join([ams_rest_endpoint, path])

    body = content
    return do_post(endpoint, path, body, access_token)

# link_content_key(access_token, asset_id, encryptionkey_id)
# link a content key with an asset
def link_content_key(access_token, asset_id, encryptionkey_id, ams_redirected_rest_endpoint):
    path = '/Assets'
    full_path = ''.join([path, "('", asset_id, "')", "/$links/ContentKeys"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    uri = ''.join([ams_redirected_rest_endpoint, 'ContentKeys', "('", encryptionkey_id, "')"])

    body = '{"uri": "' + uri + '"}'
    return do_post(endpoint, full_path_encoded, body, access_token)

# update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name)
# update a media assetfile
def update_media_assetfile(access_token, parent_asset_id, asset_id, content_length, name):
    path = '/Files'
    full_path = ''.join([path, "('", asset_id, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    body = '{"ContentFileSize": "' + str(content_length) + '", "Id": "' + asset_id + '", "MimeType": "video/mp4", "Name": "' + name + '", "ParentAssetId": "' + parent_asset_id + '"}'
    return do_patch(endpoint, full_path_encoded, body, access_token)

# set_asset_accesspolicy(access_token, duration)
# set a asset access policy
def set_asset_accesspolicy(access_token, duration):
    path = '/AccessPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{"Name": "NewUploadPolicy", "DurationInMinutes": "' + duration + '", "Permissions": "2"}'
    return do_post(endpoint, path, body, access_token)

### Helpers...
# Generic functions not intended for "external" use... 
def helper_list(access_token, oid, path):
    if(oid != ""):
    	path = ''.join([path, "('", oid, "')"])
    endpoint = ''.join([ams_rest_endpoint, path])
    return do_get(endpoint, path, access_token)

def helper_delete(access_token, oid, path):
    full_path = ''.join([path, "('", oid, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    return do_delete(endpoint, full_path_encoded, access_token)

### Aux Funcions...
# These are functions that are intended for "external" use, but are not AMS REST API's...
# Translate the numeric options/encryption of the Asset
def translate_asset_options(nr):
    if (nr == "0"): 
    	return "None"
    if (nr == "1"): 
    	return "StorageEncrypted"
    if (nr == "2"): 
    	return "CommonEncryptionProtected"
    if (nr == "4"): 
    	return "EnvelopeEncryptionProtected"

# Translate the numeric state of the Jobs
def translate_job_state(nr):
    if (nr == "0"): 
    	return "Queued"
    if (nr == "1"): 
    	return "Scheduled"
    if (nr == "2"): 
    	return "Processing"
    if (nr == "3"): 
    	return "Finished"
    if (nr == "4"): 
    	return "Error"
    if (nr == "5"): 
    	return "Canceled"
    if (nr == "6"): 
    	return "Canceling"
# Get specific url
def retrieve_url_content(url):
    return do_get(endpoint, path, access_token)

### Exceptions...
# These, I think, should not be here... ;-)
# upload_block_blob(access_token, endpoint, content, content_length)
# upload a block blob
def upload_block_blob(access_token, endpoint, content, content_length):
    return do_sto_put(endpoint, content, content_length, access_token)

# validate_mp4_asset(access_token, processor_id, asset_id, output_assetname)
# validate a mp4 asset
def validate_mp4_asset(access_token, processor_id, asset_id, output_assetname):
    path = '/Jobs'
    endpoint = ''.join([ams_rest_endpoint, path])

    assets_path = ''.join(["/Assets", "('", asset_id, "')"])
    assets_path_encoded = urllib.parse.quote(assets_path, safe='')
    endpoint_assets = ''.join([ams_rest_endpoint, assets_path_encoded])

    body = '{ \
    		"Name":"ValidateEncodedMP4", \
   		"InputMediaAssets":[{ \
       	  		"__metadata":{ \
       	     			"uri":"' + endpoint_assets + '" \
       	  		} \
     	 	}], \
   		"Tasks":[{ \
       	  		"Configuration":"<?xml version=\\"1.0\\" encoding=\\"utf-8\\"?><taskDefinition xmlns=\\"http://schemas.microsoft.com/iis/media/v4/TM/TaskDefinition#\\"><name>MP4 Preprocessor</name><id>859515BF-9BA3-4BDD-A3B6-400CEF07F870</id><description xml:lang=\\"en\\" /><inputFolder /><properties namespace=\\"http://schemas.microsoft.com/iis/media/V4/TM/MP4Preprocessor#\\" prefix=\\"mp4p\\"><property name=\\"SmoothRequired\\" value=\\"false\\" /><property name=\\"HLSRequired\\" value=\\"true\\" /></properties><taskCode><type>Microsoft.Web.Media.TransformManager.MP4PreProcessor.MP4Preprocessor_Task, Microsoft.Web.Media.TransformManager.MP4Preprocessor, Version=1.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35</type></taskCode></taskDefinition>", \
       	  		"MediaProcessorId":"' + processor_id + '", \
       	  		"TaskBody":"<?xml version=\\"1.0\\" encoding=\\"utf-16\\"?><taskBody><inputAsset>JobInputAsset(0)</inputAsset><outputAsset assetCreationOptions=\\"1\\" assetName=\\"' + output_assetname + '\\">JobOutputAsset(0)</outputAsset></taskBody>" \
      		}] \
	}'

    return do_post(endpoint, path, body, access_token)

