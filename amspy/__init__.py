"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""

# amspy - library for easy Azure Media Services calls from Python

from .amsrest import get_access_token, create_media_asset, list_media_asset, create_media_assetfile, \
	list_content_key, list_asset_accesspolicy, set_asset_accesspolicy, create_sas_locator, \
	list_sas_locator, list_media_job, list_media_processor, upload_block_blob, update_media_assetfile, \
	delete_sas_locator, delete_asset_accesspolicy, delete_content_key, create_media_job, \
	delete_media_asset, validate_mp4_asset, translate_job_state, translate_asset_options, link_content_key, \
	get_redirected_url
