"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""
import os
import json
import amspy
import time
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
print ("\n-----------------------= AMS Py =----------------------");
print ("Simple Python Library for Azure Media Services REST API");
print ("-------------------------------------------------------\n");

### list streaming endpoints
print ("\n001 >>> Listing Streaming Endpoints")
response = amspy.list_streaming_endpoint(access_token)
if (response.status_code == 200):
	resjson = response.json()
	for ea in resjson['d']['results']:
		print("POST Status.............................: " + str(response.status_code))
		print("Streaming Endpoint Id...................: " + ea['Id'])
		print("Streaming Endpoint Name.................: " + ea['Name'])
		print("Streaming Endpoint Description..........: " + ea['Description'])
else:
	print("POST Status.............................: " + str(response.status_code) + " - Streaming Endpoint Creation ERROR." + str(response.content))

