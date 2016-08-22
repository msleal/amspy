"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Rest Python library
License: MIT (see LICENSE.txt file for details)
"""

# amsrest.py - azurerm functions for the AMS Rest Interface

import urllib
import requests
from .restfns import do_auth, do_get, do_post, do_put, do_delete, do_patch, do_sto_put
from .settings import ams_rest_endpoint, ams_auth_endpoint


# get_access_token(accountname, accountkey)
# get access token with ams
def get_access_token(accountname, accountkey):
    accountkey_encoded = urllib.parse.quote(accountkey, safe='')
    body = "grant_type=client_credentials&client_id=" + accountname + "&client_secret=" + accountkey_encoded + " &scope=urn%3aWindowsAzureMediaServices"
    return do_auth(ams_auth_endpoint, body)

# create_media_asset(access_token, name)
# create a media asset
def create_media_asset(access_token, name):
    path = '/Assets'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{"Name": "' + name + '"}'
    return do_post(endpoint, path, body, access_token)

# list_media_asset(access_token, asset_id)
# list a media asset
def list_media_asset(access_token, asset_id):
    path = '/Assets'
    full_path = ''.join([path, "('", asset_id, "')"])
    endpoint = ''.join([ams_rest_endpoint, full_path])
    return do_get(endpoint, full_path, access_token)

# create_media_assetfile(access_token, parent_asset_id, name, is_encrypted, is_primary)
# create a media assetfile
def create_media_assetfile(access_token, parent_asset_id, name, is_encrypted, is_primary):
    path = '/Files'
    endpoint = ''.join([ams_rest_endpoint, path])
    body = '{"IsEncrypted": "' + is_encrypted + '", "IsPrimary": "' + is_primary + '", "MimeType": "video/mp4", "Name": "' + name + '", "ParentAssetId": "' + parent_asset_id + '"}'
    return do_post(endpoint, path, body, access_token)

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

# list_asset_accesspolicy(access_token, asset_id)
# list a asset access policy
def list_asset_accesspolicy(access_token):
    path = '/AccessPolicies'
    endpoint = ''.join([ams_rest_endpoint, path])
    return do_get(endpoint, path, access_token)

# delete_asset_accesspolicy(access_token, accesspolicy_id)
# delete a asset access policy
def delete_asset_accesspolicy(access_token, accesspolicy_id):
    path = '/AccessPolicies'
    full_path = ''.join([path, "('", accesspolicy_id, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    return do_delete(endpoint, full_path_encoded, access_token)

# create_sas_locator(access_token, asset_id, accesspolicy_id)
# create a sas locator
def create_sas_locator(access_token, asset_id, accesspolicy_id):
    path = '/Locators'
    endpoint = ''.join([ams_rest_endpoint, path])
    #body = '{"AccessPolicyId":"' + accesspolicy_id + '", "AssetId":"' + asset_id + '", "StartTime":"' + starttime + '", "Type":1 }'
    body = '{"AccessPolicyId":"' + accesspolicy_id + '", "AssetId":"' + asset_id + '", "Type":1 }'
    return do_post(endpoint, path, body, access_token)

# list_sas_locator(access_token, saslocator_id)
# list a sas locator
def list_sas_locator(access_token):
    path = '/Locators'
    endpoint = ''.join([ams_rest_endpoint, path])
    return do_get(endpoint, path, access_token)

# delete_sas_locator(access_token, saslocator_id)
# delete a sas locator
def delete_sas_locator(access_token, saslocator_id):
    path = '/Locators'
    full_path = ''.join([path, "('", saslocator_id, "')"])
    full_path_encoded = urllib.parse.quote(full_path, safe='')
    endpoint = ''.join([ams_rest_endpoint, full_path_encoded])
    return do_delete(endpoint, full_path_encoded, access_token)

# upload_block_blob(access_token, endpoint, content, content_length)
# upload a block blob
def upload_block_blob(access_token, endpoint, content, content_length):
    return do_sto_put(endpoint, content, content_length, access_token)
