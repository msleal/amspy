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

#Initialization...
print ("\n-----------------------= AMS Py =----------------------");
print ("Simple Python Library for Azure Media Services REST API");
print ("-------------------------------------------------------\n");

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

#Some global vars...
NAME = "movie"
VIDEO_NAME = "movie.mp4"
ISM_NAME = "movie.ism"
VIDEO_PATH = "/home/architect/Movie/Start-2009/movie.mp4"
ISM_PATH = "/home/architect/Movie/Start-2009/movie.ism"
PROCESSOR_NAME = "Windows Azure Media Packager"

### PRE-REQ We need to have a Content key to use for AES Encription
# Hee you can download a sample to create it for you:
# https://github.com/msleal/create_ams_aeskey
print ("000 >>> Checking the AES Content Key")
response = amspy.list_content_key(access_token)
if (response.status_code == 200):
	resjson = response.json()
	count = len(resjson['d']['results']);
	if (count > 0):
		protectionkey_id = str(resjson['d']['results'][0]['ProtectionKeyId'])
		print("GET Status..............................: " + str(response.status_code))
		print("AES Protection Key Id...................: " + protectionkey_id)
		print("AES Content Key Checksum................: " + str(resjson['d']['results'][0]['Checksum']))
	else:
		print("ERROR: AES Content Key Not Found. ")
		print("Please create an AES Content Key and execute the script again. ")
		print("Sample script to create one: https://github.com/msleal/create_ams_aeskey\n")
		exit(1);
		
else:
	print("GET Status.............................: " + str(response.status_code) + " - AES Content Key Listing ERROR." + str(response.content))
	exit(1);

### create an asset
print ("\n001 >>> Creating a Media Asset")
response = amspy.create_media_asset(access_token, NAME)
if (response.status_code == 201):
	resjson = response.json()
	asset_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Media Asset Name........................: " + NAME)
	print("Media Asset Id..........................: " + asset_id)
else:
	print("POST Status.............................: " + str(response.status_code) + " - Media Asset: '" + NAME + "' Creation ERROR." + str(response.content))

### list an asset
print ("\n002 >>> Listing a Media Asset")
response = amspy.list_media_asset(access_token, asset_id)
if (response.status_code == 200):
	resjson = response.json()
	asset_uri = str(resjson['d']['Uri'])
	print("GET Status..............................: " + str(response.status_code))
	print("Media Asset Name........................: " + str(resjson['d']['Name']))
	print("Media Asset Storage Account Name........: " + str(resjson['d']['StorageAccountName']))
	print("Media Asset Uri.........................: " + asset_uri)
else:
	print("GET Status..............................: " + str(response.status_code) + " - Media Asset: '" + asset_id + "' Listing ERROR." + str(response.content))

### create an assetfile
print ("\n003 >>> Creating a Media Assetfile (for the video file)")
response = amspy.create_media_assetfile(access_token, asset_id, VIDEO_NAME, "false", "false")
if (response.status_code == 201):
	resjson = response.json()
	video_assetfile_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Media Assetfile Name....................: " + str(resjson['d']['Name']))
	print("Media Assetfile Id......................: " + video_assetfile_id)
	print("Media Assetfile IsPrimary...............: " + str(resjson['d']['IsPrimary']))
else:
	print("POST Status: " + str(response.status_code) + " - Media Assetfile: '" + VIDEO_NAME + "' Creation ERROR." + str(response.content))

### create an assetfile
print ("\n004 >>> Creating a Media Assetfile (for the manifest file)")
response = amspy.create_media_assetfile(access_token, asset_id, ISM_NAME, "false", "true")
if (response.status_code == 201):
	resjson = response.json()
	ism_assetfile_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Media Assetfile Name....................: " + str(resjson['d']['Name']))
	print("Media Assetfile Id......................: " + ism_assetfile_id)
	print("Media Assetfile IsPrimary...............: " + str(resjson['d']['IsPrimary']))
else:
	print("POST Status: " + str(response.status_code) + " - Media Assetfile: '" + ISM_NAME + "' Creation ERROR." + str(response.content))

### set an asset access policy
print ("\n005 >>> Setting an Asset Access Policy")
duration = "440"
response = amspy.set_asset_accesspolicy(access_token, duration)
if (response.status_code == 201):
	resjson = response.json()
	accesspolicy_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Asset Access Policy Id..................: " + accesspolicy_id)
	print("Asset Access Policy Duration/min........: " + str(resjson['d']['DurationInMinutes']))
else:
	print("POST Status: " + str(response.status_code) + " - Asset Access Policy Creation ERROR." + str(response.content))

### list an asset access policies
print ("\n006 >>> Listing a Asset Access Policies")
response = amspy.list_asset_accesspolicy(access_token)
if (response.status_code == 200):
	resjson = response.json()
	print("GET Status..............................: " + str(response.status_code))
	for ap in resjson['d']['results']:
		print("Asset Access Policie Id.................: " + str(ap['Id']))
else:
	print("GET Status: " + str(response.status_code) + " - Asset Access Policy List ERROR." + str(response.content))

### create a sas locator
print ("\n007 >>> Creating a SAS Locator")
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
	print("POST Status.............................: " + str(response.status_code))
	print("SAS URL Locator StartTime...............: " + str(resjson['d']['StartTime']))
	print("SAS URL Locator Id......................: " + saslocator_id)
	print("SAS URL Locator Base URI................: " + saslocator_baseuri)
	print("SAS URL Locator Content Access Component: " + saslocator_cac)
else:
	print("POST Status: " + str(response.status_code) + " - SAS URL Locator Creation ERROR." + str(response.content))

### list the sas locator
print ("\n008 >>> Listing a SAS Locator")
response = amspy.list_sas_locator(access_token)
if (response.status_code == 200):
	resjson = response.json()
	print("GET Status..............................: " + str(response.status_code))
	for sl in resjson['d']['results']:
		print("SAS Locator Id..........................: " + str(sl['Id']))
else:
	print("GET Status..............................: " + str(response.status_code) + " - SAS Locator List ERROR." + str(response.content))

### upload the video file
print ("\n009 >>> Uploading the Video File")
#datetime = datetime.datetime.now(pytz.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
saslocator_video_url = ''.join([saslocator_baseuri, '/', VIDEO_NAME, saslocator_cac])
with open(VIDEO_PATH, mode='rb') as file:
	video_content = file.read()
	video_content_length = len(video_content)
response = amspy.upload_block_blob(access_token, saslocator_video_url, video_content, video_content_length)
if (response.status_code == 201):
	print("POST Status.............................: " + str(response.status_code))
	#print("SAS Complete Upload URL.........: " + saslocator_video_url)
	print("Video File Uploaded.....................: OK")
else:
	print("POST Status.............................: " + str(response.status_code) + " - Video File: '" + VIDEO_NAME + "' Upload ERROR." + str(response.content))

### upload the manifest file
print ("\n010 >>> Uploading the Manifest File")
saslocator_ism_url = ''.join([saslocator_baseuri, '/', ISM_NAME, saslocator_cac])
with open(ISM_PATH, mode='rb') as file:
	ism_content = file.read()
	ism_content_length = len(ism_content)
response = amspy.upload_block_blob(access_token, saslocator_ism_url, ism_content, ism_content_length)
if (response.status_code == 201):
	print("POST Status.............................: " + str(response.status_code))
	#print("SAS Complete Upload URL.................: " + saslocator_ism_url)
	print("Manifest File Uploaded..................: OK")
else:
	print("POST Status: " + str(response.status_code) + " - Video File: '" + ISM_NAME + "' Upload ERROR." + str(response.content))

### update the assetfile
print ("\n011 >>> Updating the Video Assetfile")
response = amspy.update_media_assetfile(access_token, asset_id, video_assetfile_id, video_content_length, VIDEO_NAME)
if (response.status_code == 204):
	print("MERGE Status............................: " + str(response.status_code))
	print("Assetfile Content Length Updated........: " + str(video_content_length))
else:
	print("MERGE Status............................: " + str(response.status_code) + " - Assetfile: '" + VIDEO_NAME + "' Update ERROR." + str(response.content))

### update the assetfile
print ("\n012 >>> Updating the Manifest Assetfile")
response = amspy.update_media_assetfile(access_token, asset_id, ism_assetfile_id, ism_content_length, ISM_NAME)
if (response.status_code == 204):
	print("MERGE Status............................: " + str(response.status_code))
	print("Assetfile Content Length Updated........: " + str(ism_content_length))
else:
	print("MERGE Status............................: " + str(response.status_code) + " - Assetfile: '" + ISM_NAME + "' Update ERROR." + str(response.content))

### delete the locator
print ("\n013 >>> Deleting the Locator")
response = amspy.delete_sas_locator(access_token, saslocator_id)
if (response.status_code == 204):
	print("DELETE Status...........................: " + str(response.status_code))
	print("SAS URL Locator Deleted.................: " + saslocator_id)
else:
	print("DELETE Status...........................: " + str(response.status_code) + " - SAS URL Locator: '" + saslocator_id + "' Delete ERROR." + str(response.content))

### delete the asset access policy
print ("\n014 >>> Deleting the Acess Policy")
response = amspy.delete_asset_accesspolicy(access_token, accesspolicy_id)
if (response.status_code == 204):
	print("DELETE Status...........................: " + str(response.status_code))
	print("Asset Access Policy Deleted.............: " + accesspolicy_id)
else:
	print("DELETE Status...........................: " + str(response.status_code) + " - Asset Access Policy: '" + accesspolicy_id + "' Delete ERROR." + str(response.content))

### get the media processor
print ("\n015 >>> Getting the Media Processor")
response = amspy.list_media_processor(access_token)
if (response.status_code == 200):
        resjson = response.json()
        print("GET Status..............................: " + str(response.status_code))
        for mp in resjson['d']['results']:
                if(str(mp['Name']) == PROCESSOR_NAME):
                        processor_id = str(mp['Id'])
                        print("MEDIA Processor Id......................: " + processor_id)
                        print("MEDIA Processor Name....................: " + PROCESSOR_NAME)
else:
        print("GET Status: " + str(response.status_code) + " - Media Processors Listing ERROR." + str(response.content))

## create a media validation job
print ("\n016 >>> Creating a Specific Media Job to validate the mp4")
response = amspy.validate_mp4_asset(access_token, processor_id, asset_id, "mp4validated")
if (response.status_code == 201):
	resjson = response.json()
	job_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Media Job Id............................: " + job_id)
else:
	print("POST Status.............................: " + str(response.status_code) + " - Media Job Creation ERROR." + str(response.content))

### list a media job
print ("\n017 >>> Listing a Media Job")
flag = 1
while (flag):
	response = amspy.list_media_job(access_token, job_id)
	if (response.status_code == 200):
		resjson = response.json()
		job_state = str(resjson['d']['State'])
		if (resjson['d']['EndTime'] != None):
			flag = 0;
		print("GET Status..............................: " + str(response.status_code))
		print("Media Job Status........................: " + amspy.translate_job_state(job_state))
	else:
		print("GET Status..............................: " + str(response.status_code) + " - Media Job: '" + asset_id + "' Listing ERROR." + str(response.content))
	time.sleep(5);

### delete an asset
if (amspy.translate_job_state(job_state) == 'Finished'):
	print ("\n018 >>> Deleting the Original Asset")
	response = amspy.delete_media_asset(access_token, asset_id)
	if (response.status_code == 204):
		print("DELETE Status...........................: " + str(response.status_code))
		print("Asset Deleted...........................: " + asset_id)
	else:
		print("DELETE Status...........................: " + str(response.status_code) + " - Asset: '" + asset_id + "' Delete ERROR." + str(response.content))
print ("\n We got here? Cool!")
