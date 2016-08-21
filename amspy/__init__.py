"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""

# amspy - library for easy Azure Media Services calls from Python

from .amsrest import get_access_token, create_media_asset, list_media_asset, create_media_assetfile, \
	set_asset_accesspolicy, list_asset_accesspolicy, create_sas_locator, list_sas_locator, \
	upload_block_blob, update_media_assetfile, delete_sas_locator, delete_asset_accesspolicy
