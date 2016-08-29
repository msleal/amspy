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

###########################################################################################
##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER #####
###########################################################################################

# ALL CODE IN THIS DIRECTOY (INCLUDING THIS FILE) ARE EXAMPLE CODES THAT  WILL  ACT ON YOUR 
# AMS ACCOUNT.  IT ASSUMES THAT THE AMS ACCOUNT IS CLEAN (e.g.: BRAND NEW), WITH NO DATA OR 
# PRODUCTION CODE ON IT.  DO NOT, AGAIN: DO NOT RUN ANY EXAMPLE CODE AGAINST PRODUCTION AMS
# ACCOUNT!  IF YOU RUN ANY EXAMPLE CODE AGAINST YOUR PRODUCTION  AMS ACCOUNT,  YOU CAN LOSE 
# DATA, AND/OR PUT YOUR AMS SERVICES IN A DEGRADED OR UNAVAILABLE STATE. BE WARNED!

###########################################################################################
##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER ##### ##### DISCLAIMER #####
###########################################################################################

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
ENCRYPTION = "1" # 0=None, StorageEncrypted=1, CommonEncryptionProtected=2, EnvelopeEncryptionProtected=4
ENCRYPTION_SCHEME = "StorageEncryption" # StorageEncryption or CommonEncryption.
VIDEO_NAME = "movie.mp4"
ISM_NAME = "movie.ism"
VIDEO_PATH = "assets/movie.mp4"
ISM_PATH = "assets/movie.ism"
PROCESSOR_NAME = "Windows Azure Media Packager"
AUTH_POLICY = '{"Name":"Open Authorization Policy"}'
KEY_DELIVERY_TYPE = "2" # 1=PlayReady, 2=AES Envelope Encryption
SCALE_UNIT = "1" # This will set the Scale Unit of the Streaming Unit to 1 (Each SU = 200mbs)

### get ams redirected url
response = amspy.get_url(access_token)
if (response.status_code == 200):
        ams_redirected_rest_endpoint = str(response.url)
else:
        print("GET Status: " + str(response.status_code) + " - Getting Redirected URL ERROR." + str(response.content))
        exit(1);

### PRE-REQ We need to have a Content key to use for AES Encription and
# at least 1 ("one") scale unit at the streaming endpoint (e.g.: default).
# Here you can download a sample to create the Content Key for you:
# https://github.com/msleal/create_ams_aeskey
# The streaming endpoint will be scaled for you (to "1" scale unit).
print ("000 >>> Checking the AES Content Key and Setting Streaming Endpoint Scale Unit")
response = amspy.list_content_key(access_token)
if (response.status_code == 200):
	resjson = response.json()
	count = len(resjson['d']['results']);
	if (count > 0):
		contentkey_id = str(resjson['d']['results'][0]['Id'])
		protectionkey_id = str(resjson['d']['results'][0]['ProtectionKeyId'])
		print("GET Status..............................: " + str(response.status_code))
		print("AES Content Key Id......................: " + contentkey_id)
		print("AES Content Key Name....................: " + str(resjson['d']['results'][0]['Name']))
		print("AES Content Protection Key Id...........: " + protectionkey_id)
		print("AES Content Key Checksum................: " + str(resjson['d']['results'][0]['Checksum']))
	else:
		print("ERROR: AES Content Key Not Found. ")
		print("Please create an AES Content Key and execute the script again. ")
		print("Sample script to create one: https://github.com/msleal/create_ams_aeskey\n")
		exit(1);
		
else:
	print("GET Status.............................: " + str(response.status_code) + " - AES Content Key Listing ERROR." + str(response.content))
	exit(1);

# list and get the id of the default streaming endpoint
response = amspy.list_streaming_endpoint(access_token)
if (response.status_code == 200):
	resjson = response.json()
	for ea in resjson['d']['results']:
		print("POST Status.............................: " + str(response.status_code))
		print("Streaming Endpoint Id...................: " + ea['Id'])
		print("Streaming Endpoint Name.................: " + ea['Name'])
		print("Streaming Endpoint Description..........: " + ea['Description'])
		if (ea['Name'] == 'default'):
			streaming_endpoint_id = ea['Id'];
else:
        print("POST Status.............................: " + str(response.status_code) + " - Streaming Endpoint Creation ERROR." + str(response.content))

# scale the default streaming endpoint
response = amspy.scale_streaming_endpoint(access_token, streaming_endpoint_id, SCALE_UNIT)
if (response.status_code == 202):
	print("POST Status.............................: " + str(response.status_code))
	print("Streaming Endpoint SU Configured to.....: " + SCALE_UNIT)
else:
	print("GET Status.............................: " + str(response.status_code) + " - Streaming Endpoint Scaling ERROR." + str(response.content))
	exit(1);

######################### PHASE 1: UPLOAD and VALIDATE #########################
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
	print("Media Asset Encryption..................: " + str(amspy.translate_asset_options(resjson['d']['Options'])))
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
response = amspy.create_media_assetfile(access_token, asset_id, ISM_NAME, "true", "false")
if (response.status_code == 201):
	resjson = response.json()
	ism_assetfile_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Media Assetfile Name....................: " + str(resjson['d']['Name']))
	print("Media Assetfile Id......................: " + ism_assetfile_id)
	print("Media Assetfile IsPrimary...............: " + str(resjson['d']['IsPrimary']))
else:
	print("POST Status: " + str(response.status_code) + " - Media Assetfile: '" + ISM_NAME + "' Creation ERROR." + str(response.content))

### create an asset access policy
print ("\n005 >>> Creating an Asset Access Policy")
duration = "440"
response = amspy.create_asset_accesspolicy(access_token, "NewUploadPolicy", duration, "2")
if (response.status_code == 201):
	resjson = response.json()
	write_accesspolicy_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Asset Access Policy Id..................: " + write_accesspolicy_id)
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
#response = amspy.create_sas_locator(access_token, asset_id, write_accesspolicy_id, starttime)
response = amspy.create_sas_locator(access_token, asset_id, write_accesspolicy_id)
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
response = amspy.delete_asset_accesspolicy(access_token, write_accesspolicy_id)
if (response.status_code == 204):
	print("DELETE Status...........................: " + str(response.status_code))
	print("Asset Access Policy Deleted.............: " + write_accesspolicy_id)
else:
	print("DELETE Status...........................: " + str(response.status_code) + " - Asset Access Policy: '" + write_accesspolicy_id + "' Delete ERROR." + str(response.content))

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
print ("\n016 >>> Creating a Media Job to validate the mp4")
response = amspy.validate_mp4_asset(access_token, processor_id, asset_id, "mp4validated")
if (response.status_code == 201):
	resjson = response.json()
	job_id = str(resjson['d']['Id']);
	print("POST Status.............................: " + str(response.status_code))
	print("Media Job Id............................: " + job_id)
else:
	print("POST Status.............................: " + str(response.status_code) + " - Media Job Creation ERROR." + str(response.content))

### list a media job
print ("\n017 >>> Getting the Media Job Status")
flag = 1
while (flag):
	response = amspy.list_media_job(access_token, job_id)
	if (response.status_code == 200):
		resjson = response.json()
		job_state = str(resjson['d']['State'])
		if (resjson['d']['EndTime'] != None):
			joboutputassets_uri = resjson['d']['OutputMediaAssets']['__deferred']['uri']
			flag = 0;
		print("GET Status..............................: " + str(response.status_code))
		print("Media Job Status........................: " + amspy.translate_job_state(job_state))
	else:
		print("GET Status..............................: " + str(response.status_code) + " - Media Job: '" + asset_id + "' Listing ERROR." + str(response.content))
	time.sleep(5);

######################### PHASE 2: PROTECT and STREAM #########################
### delete an asset
if (amspy.translate_job_state(job_state) == 'Finished'):
	### delete an asset
	print ("\n018 >>> Deleting the Original Asset")
	response = amspy.delete_media_asset(access_token, asset_id)
	if (response.status_code == 204):
		print("DELETE Status...........................: " + str(response.status_code))
		print("Asset Deleted...........................: " + asset_id)
	else:
		print("DELETE Status...........................: " + str(response.status_code) + " - Asset: '" + asset_id + "' Delete ERROR." + str(response.content))

	## getting the encoded asset id
	print ("\n019 >>> Getting the Encoded Media Asset Id")
	response = amspy.get_url(access_token, joboutputassets_uri, False)
	if (response.status_code == 200):
		resjson = response.json()
		encoded_asset_id = resjson['d']['results'][0]['Id']
		print("GET Status..............................: " + str(response.status_code))
		print("Encoded Media Asset Id..................: " + encoded_asset_id)
	else:
		print("GET Status..............................: " + str(response.status_code) + " - Media Job Output Asset: '" + job_id + "' Getting ERROR." + str(response.content))

	### link a content key
	print ("\n020 >>> Linking the Content Key to the Encoded Asset")
	response = amspy.link_asset_content_key(access_token, encoded_asset_id, contentkey_id, ams_redirected_rest_endpoint)
	if (response.status_code == 204):
		print("GET Status..............................: " + str(response.status_code))
		print("Media Content Key Linked................: OK")
	else:
		print("GET Status..............................: " + str(response.status_code) + " - Media Asset: '" + encoded_asset_id + "' Content Key Linking ERROR." + str(response.content))

	### configure content key authorization policy
	print ("\n021 >>> Creating the Content Key Authorization Policy")
	response = amspy.create_contentkey_authorization_policy(access_token, AUTH_POLICY)
	if (response.status_code == 201):
		resjson = response.json()
		authorization_policy_id = str(resjson['d']['Id']);
		print("POST Status.............................: " + str(response.status_code))
		print("CK Authorization Policy Id..............: " + authorization_policy_id)
	else:
		print("POST Status.............................: " + str(response.status_code) + " - Content Key Authorization Policy Creation ERROR." + str(response.content))

	### configure asset delivery policy
	print ("\n022 >>> Creating the Content Key Authorization Policy Options")
	response = amspy.create_contentkey_authorization_policy_options(access_token)
	if (response.status_code == 201):
		resjson = response.json()
		authorization_policy_options_id = str(resjson['d']['Id']);
		print("POST Status.............................: " + str(response.status_code))
		print("CK Authorization Policy Options Id......: " + authorization_policy_options_id)
	else:
		print("POST Status.............................: " + str(response.status_code) + " - Content Key Authorization Policy Options Creation ERROR." + str(response.content))

	### link a contentkey authorization policies with options
	print ("\n023 >>> Linking the Content Key Authorization Policy with Options")
	response = amspy.link_contentkey_authorization_policy(access_token, authorization_policy_id, authorization_policy_options_id, ams_redirected_rest_endpoint)
	if (response.status_code == 204):
		print("GET Status..............................: " + str(response.status_code))
		print("CK Authorization Policy Linked..........: OK")
	else:
		print("GET Status..............................: " + str(response.status_code) + " - Content Key Authorization Policy '" + authorization_policy_id + "' Linking ERROR." + str(response.content))

	### link a contentkey authorization policies with options
	print ("\n024 >>> Add the Authorization Policy to the Content Key")
	response = amspy.add_authorization_policy(access_token, contentkey_id, authorization_policy_id)
	if (response.status_code == 204):
		print("GET Status..............................: " + str(response.status_code))
		print("Authorization Policy Added..............: OK")
	else:
		print("GET Status..............................: " + str(response.status_code) + " - Authorization Policy: '" + authorization_policy_id + "' Adding ERROR." + str(response.content))

	### get the delivery url
	print ("\n025 >>> Getting the Key Delivery URL")
	response = amspy.get_delivery_url(access_token, contentkey_id, KEY_DELIVERY_TYPE)
	if (response.status_code == 200):
		resjson = response.json()
		keydelivery_url = str(resjson['d']['GetKeyDeliveryUrl']);
		print("POST Status.............................: " + str(response.status_code))
		print("Key Delivery URL........................: " + keydelivery_url)
	else:
		print("POST Status.............................: " + str(response.status_code) + " - Key Delivery: '" + contentkey_id + "' URL Getting ERROR." + str(response.content))

	### create asset delivery policy
	print ("\n026 >>> Creating Asset Delivery Policy")
	response = amspy.create_asset_delivery_policy(access_token, account_name)
	if (response.status_code == 201):
		resjson = response.json()
		assetdeliverypolicy_id = str(resjson['d']['Id']);
		print("POST Status.............................: " + str(response.status_code))
		print("Asset Delivery Policy Id................: " + assetdeliverypolicy_id)
	else:
		print("POST Status.............................: " + str(response.status_code) + " - Asset Delivery Policy Creating ERROR." + str(response.content))

	### link the asset with the asset delivery policy
	print ("\n027 >>> Linking the Asset with the Asset Delivery Policy")
	response = amspy.link_asset_delivery_policy(access_token, encoded_asset_id, assetdeliverypolicy_id, ams_redirected_rest_endpoint)
	if (response.status_code == 204):
		print("GET Status..............................: " + str(response.status_code))
		print("Asset Delivery Policy Linked............: OK")
	else:
		print("GET Status..............................: " + str(response.status_code) + " - Asset: '" + encoded_asset_id + "' Delivery Policy Linking ERROR." + str(response.content))

	### create an asset access policy
	print ("\n028 >>> Creating an Asset Access Policy")
	duration = "43200"
	response = amspy.create_asset_accesspolicy(access_token, "NewViewAccessPolicy", duration)
	if (response.status_code == 201):
		resjson = response.json()
		view_accesspolicy_id = str(resjson['d']['Id']);
		print("POST Status.............................: " + str(response.status_code))
		print("Asset Access Policy Id..................: " + view_accesspolicy_id)
		print("Asset Access Policy Duration/min........: " + str(resjson['d']['DurationInMinutes']))
	else:
		print("POST Status: " + str(response.status_code) + " - Asset Access Policy Creation ERROR." + str(response.content))

	### create an ondemand streaming locator
	print ("\n029 >>> Create an OnDemand Streaming Locator")
	#starttime = datetime.datetime.now(pytz.timezone(time_zone)).strftime("%Y-%m-%dT%H:%M:%SZ")
	#response = amspy.create_ondemand_streaming_locator(access_token, encoded_asset_id, view_accesspolicy_id, starttime)
	response = amspy.create_ondemand_streaming_locator(access_token, encoded_asset_id, view_accesspolicy_id)
	if (response.status_code == 201):
		resjson = response.json()
		ondemandlocator_id = str(resjson['d']['Id']);
		print("GET Status..............................: " + str(response.status_code))
		print("OnDemand Streaming Locator Id...........: " + ondemandlocator_id)
		print("OnDemand Streaming Locator Path.........: " + str(resjson['d']['Path']))
		print("HLS + AES URL...........................: " + str(resjson['d']['Path']) + ISM_NAME + "/manifest(format=m3u8-aapl)")
		print ("\n -> We got here? Cool! Now you just need the popcorn...")
	else:
		print("GET Status..............................: " + str(response.status_code) + " - OnDemand Streaming Locator Creating ERROR." + str(response.content))
else:
	print ("\n Something went wrong... we could not validate the MP4 Asset!")
