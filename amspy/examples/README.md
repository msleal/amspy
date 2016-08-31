## Pre-Req to run the samples
You will need to install the python sdk for Azure and Blob Storage (we use this sdk for the upload
part of our scripts), and install the amspy python library (this is the library that implements
the AMS REST API's).

```
pip(3) install pycrypto
pip(3) install azure
pip(3) install azure-storage
pip(3) install amspy
```

## Config File
You need to add your credentials and provide informaton about your AMS environment using the config
file (config.json). Here is a description of each option:
```
{
   "subscriptionId": "<here-you-add-your-azure-subscription-id>",
   "rgName": "<here-you-your-resource-group-name>",
   "accountName": "<here-you-add-your-media-services-account-name>",
   "accountKey": "<here-you-add-your-media-services-account-secret-key>",
   "logName": "<here-you-choose-the-name-of-your-log-file>",
   "logLevel": "DEBUG",
   "purgeLog": "Yes",
   "timeZone": "<here-you-add-your-time-zone>",
   "region": "<here-you-specify-the-region-where-you-want-your-ams-deployed>"
}
```

## Examples
In this directory you have many small scripts that show how to use specific Azure Media Services API's.
You will also find two complete samples showing how to upload encode (or validate) assets, as well as
protect them and configure the streaming. You can see a description of these two scripts bellow...

## HLS+AES WORKFLOW (From MP4)

### Upload, validate, protect (dinamically with AES Envelope encryption), and stream your MP4 Videos.
This example does the complete AES workflow from uploading an already encode MP4 file,
validate it with the Azure Media Packager; protecting the asset with AES envelope encryption (content key
configuration, authorization policies, and etc), as well as configuring the HLS delivery policy.  
```
export PYTHONDONTWRITEBYTECODE=1; python3 aes_workflow_from_mp4.py
```

## HLS+AES WORKFLOW (From RAW)

### Upload, encode, protect (dinamically with AES Envelope encryption), and stream your Raw Video.
This example does the complete AES workflow from uploading an mezzanine video file,
encode it with the Azure Encoder; protecting the asset with AES envelope encryption (content key
configuration, authorization policies, and etc), as well as configuring the HLS delivery policy.  
```
export PYTHONDONTWRITEBYTECODE=1; python3 aes_workflow_from_raw.py
```
