"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python Library
License: MIT (see LICENSE.txt for details)
"""

# settings.py - place to store constants for azurerm

#Endpoints...
ams_auth_endpoint = 'https://wamsprodglobal001acs.accesscontrol.windows.net/v2/OAuth2-13'
ams_rest_endpoint = 'https://media.windows.net/API'

#Headers...
json_acceptformat = "application/json;odata=verbose"
xml_acceptformat = "application/atom+xml"
batch_acceptformat = "multipart/mixed" 
xmsversion = "2.13"
dsversion = "3.0;NetFx"
mdsversion = "3.0;NetFx"
charset = "UTF-8"
