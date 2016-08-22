"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""
import os
import json
import amspy
import time
#import pytz
import logging
import datetime

# Load Azure app defaults
try:
	with open('config.json') as configFile:
		configData = json.load(configFile)
except FileNotFoundError:
	print("ERROR: Expecting config.json in current folder")
	sys.exit()

subscription_id = configData['subscriptionId']
rg_name = configData['rgName']
account_name = configData['accountName']
account_key = configData['accountKey']
log_name = configData['logName']
log_level = configData['logLevel']
purge_log = configData['purgeLog']
time_zone = configData['timeZone']
region = configData['region']

#Remove old log file if requested (default behavior)...
if (purge_log.lower() == "yes"):
        if (os.path.isfile(log_name)):
                os.remove(log_name);

#Basic Logging...
logging.basicConfig(format='%(asctime)s - %(levelname)s:%(message)s', level=log_level, filename=log_name)

# Get the access token...
response = amspy.get_access_token(account_name, account_key)
resjson = response.json()
access_token = resjson["access_token"]

#Initialization...
print ("\n----------------= AMS Py =-----------------");
print ("Simple Azure Media Services  Python Library");
print ("-------------------------------------------\n");

#Some global vars...
name = "movie"
video_name = "movie.mp4"
ism_name = "movie.ism"
video_path = "/home/architect/Movie/Start-2009/movie.mp4"
ism_path = "/home/architect/Movie/Start-2009/movie.ism"

### create an asset
print ("001 - Creating a Media Asset...")
response = amspy.create_media_asset(access_token, name)
if (response.status_code == 201):
	resjson = response.json()
	asset_id = str(resjson['d']['Id']);
	print("POST Status: " + str(response.status_code))
	print("Media Asset Name: " + name)
	print("Media Asset Id: " + asset_id)
else:
	print("POST Status: " + str(response.status_code) + " - Media Asset: '" + name + "' Creation ERROR." + str(response.content))

### list an asset
print ("\n002 - Listing a Media Asset...")
response = amspy.list_media_asset(access_token, asset_id)
if (response.status_code == 200):
	resjson = response.json()
	print("GET Status: " + str(response.status_code))
	print("Media Asset Name: " + str(resjson['d']['Name']))
	print("Media Asset Storage Account Name: " + str(resjson['d']['StorageAccountName']))
	print("Media Asset Uri: " + str(resjson['d']['Uri']))
else:
	print("GET Status: " + str(response.status_code) + " - Media Asset: '" + name + "' Listing ERROR." + str(response.content))

### create an assetfile
print ("\n003 - Creating a Media Assetfile (for the video file)...")
response = amspy.create_media_assetfile(access_token, asset_id, video_name, "false", "false")
if (response.status_code == 201):
	resjson = response.json()
	video_assetfile_id = str(resjson['d']['Id']);
	print("POST Status: " + str(response.status_code))
	print("Media Assetfile Name: " + str(resjson['d']['Name']))
	print("Media Assetfile Id: " + video_assetfile_id)
	print("Media Assetfile IsPrimary: " + str(resjson['d']['IsPrimary']))
else:
	print("POST Status: " + str(response.status_code) + " - Media Assetfile: '" + video_name + "' Creation ERROR." + str(response.content))

### create an assetfile
print ("\n004 - Creating a Media Assetfile (for the manifest file)...")
response = amspy.create_media_assetfile(access_token, asset_id, ism_name, "false", "true")
if (response.status_code == 201):
	resjson = response.json()
	ism_assetfile_id = str(resjson['d']['Id']);
	print("POST Status: " + str(response.status_code))
	print("Media Assetfile Name: " + str(resjson['d']['Name']))
	print("Media Assetfile Id: " + ism_assetfile_id)
	print("Media Assetfile IsPrimary: " + str(resjson['d']['IsPrimary']))
else:
	print("POST Status: " + str(response.status_code) + " - Media Assetfile: '" + ism_name + "' Creation ERROR." + str(response.content))

### set an asset access policy
print ("\n005 - Setting an Asset Access Policy...")
duration = "440"
response = amspy.set_asset_accesspolicy(access_token, duration)
if (response.status_code == 201):
	resjson = response.json()
	accesspolicy_id = str(resjson['d']['Id']);
	print("POST Status: " + str(response.status_code))
	print("Asset Access Policy Id: " + accesspolicy_id)
	print("Asset Access Policy Duration in Minutes: " + str(resjson['d']['DurationInMinutes']))
else:
	print("POST Status: " + str(response.status_code) + " - Asset Access Policy: '" + name + "' Creation ERROR." + str(response.content))

### list an asset access policies
print ("\n006 - Listing a Asset Access Policies...")
response = amspy.list_asset_accesspolicy(access_token)
if (response.status_code == 200):
	resjson = response.json()
	print("GET Status: " + str(response.status_code))
	for ap in resjson['d']['results']:
		print("Asset Access Policie Id: " + str(ap['Id']))
else:
	print("GET Status: " + str(response.status_code) + " - Asset Access Policy: '" + name + "' List ERROR." + str(response.content))

### create a sas locator
print ("\n007 - Creating a SAS Locator...")
## INFO: If you need to upload your files immediately, you should set your StartTime value to five minutes before the current time.
#This is because there may be clock skew between your client machine and Media Services.
#Also, your StartTime value must be in the following DateTime format: YYYY-MM-DDTHH:mm:ssZ (for example, "2014-05-23T17:53:50Z").
# EDITED: Not providing starttime is the best approach to be able to upload a file immediatly...
#starttime = datetime.datetime.now(pytz.timezone(time_zone)).strftime("%Y-%m-%dT%H:%M:%SZ")
#response = amspy.create_sas_locator(access_token, asset_id, accesspolicy_id, starttime)
response = amspy.create_sas_locator(access_token, asset_id, accesspolicy_id)
if (response.status_code == 201):
	resjson = response.json()
	saslocator_id = str(resjson['d']['Id']);
	saslocator_baseuri = str(resjson['d']['BaseUri']);
	saslocator_cac = str(resjson['d']['ContentAccessComponent']);
	print("POST Status: " + str(response.status_code))
	print("SAS URL Locator StartTime: " + str(resjson['d']['StartTime']))
	print("SAS URL Locator Id: " + saslocator_id)
	print("SAS URL Locator Base URI: " + saslocator_baseuri)
	print("SAS URL Locator Content Access Component: " + saslocator_cac)
else:
	print("POST Status: " + str(response.status_code) + " - SAS URL Locator: '" + name + "' Creation ERROR." + str(response.content))

### list the sas locator
print ("\n008 - Listing a SAS Locator...")
response = amspy.list_sas_locator(access_token)
if (response.status_code == 200):
	resjson = response.json()
	print("GET Status: " + str(response.status_code))
	for sl in resjson['d']['results']:
		print("SAS Locator Id: " + str(sl['Id']))
else:
	print("GET Status: " + str(response.status_code) + " - SAS Locator: '" + name + "' List ERROR." + str(response.content))

### upload the video file
print ("\n009 - Uploading the Video File...")
#datetime = datetime.datetime.now(pytz.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
saslocator_video_url = ''.join([saslocator_baseuri, '/', video_name, saslocator_cac])
with open(video_path, mode='rb') as file:
	video_content = file.read()
	video_content_length = len(video_content)
response = amspy.upload_block_blob(access_token, saslocator_video_url, video_content, video_content_length)
if (response.status_code == 201):
	print("POST Status: " + str(response.status_code))
	print("SAS Complete Upload URL: " + saslocator_video_url)
	print("Video File Uploaded.")
else:
	print("POST Status: " + str(response.status_code) + " - Video File: '" + video_name + "' Upload ERROR." + str(response.content))

### upload the manifest file
print ("\n010 - Uploading the Manifest File...")
saslocator_ism_url = ''.join([saslocator_baseuri, '/', ism_name, saslocator_cac])
with open(ism_path, mode='rb') as file:
	ism_content = file.read()
	ism_content_length = len(ism_content)
response = amspy.upload_block_blob(access_token, saslocator_ism_url, ism_content, ism_content_length)
if (response.status_code == 201):
	print("POST Status: " + str(response.status_code))
	print("SAS Complete Upload URL: " + saslocator_ism_url)
	print("Manifest File Uploaded.")
else:
	print("POST Status: " + str(response.status_code) + " - Video File: '" + ism_name + "' Upload ERROR." + str(response.content))

### update the assetfile
print ("\n011 - Updating the Video Assetfile...")
response = amspy.update_media_assetfile(access_token, asset_id, video_assetfile_id, video_content_length, video_name)
if (response.status_code == 204):
	print("MERGE Status: " + str(response.status_code))
	print("Assetfile Content Length Updated: " + str(video_content_length))
else:
	print("MERGE Status: " + str(response.status_code) + " - Assetfile: '" + video_name + "' Update ERROR." + str(response.content))

### update the assetfile
print ("\n012 - Updating the Manifest Assetfile...")
response = amspy.update_media_assetfile(access_token, asset_id, ism_assetfile_id, ism_content_length, ism_name)
if (response.status_code == 204):
	print("MERGE Status: " + str(response.status_code))
	print("Assetfile Content Length Updated: " + str(ism_content_length))
else:
	print("MERGE Status: " + str(response.status_code) + " - Assetfile: '" + ism_name + "' Update ERROR." + str(response.content))

### delete the locator
print ("\n013 - Deleting the Locator...")
response = amspy.delete_sas_locator(access_token, saslocator_id)
if (response.status_code == 204):
	print("DELETE Status: " + str(response.status_code))
	print("SAS URL Locator Deleted: " + saslocator_id)
else:
	print("DELETE Status: " + str(response.status_code) + " - SAS URL Locator: '" + saslocator_id + "' Delete ERROR." + str(response.content))

### delete the asset access policy
print ("\n014 - Deleting the Acess Policy...")
response = amspy.delete_asset_accesspolicy(access_token, accesspolicy_id)
if (response.status_code == 204):
	print("DELETE Status: " + str(response.status_code))
	print("Asset Access Policy Deleted: " + accesspolicy_id)
else:
	print("DELETE Status: " + str(response.status_code) + " - Asset Access Policy: '" + accesspolicy_id + "' Delete ERROR." + str(response.content))
