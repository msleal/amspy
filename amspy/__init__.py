"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""

# amspy - library for easy Azure Media Services calls from Python

from .amsrest import get_access_token, create_media_asset, list_media_asset, create_media_assetfile, \
	list_content_keys, list_asset_accesspolicy, set_asset_accesspolicy, create_sas_locator, \
	list_sas_locator, upload_block_blob, update_media_assetfile, delete_sas_locator, \
	delete_asset_accesspolicy, delete_content_key, create_media_job, list_media_processor
