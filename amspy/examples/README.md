### AES WORKFLOW (From MP4)

# Upload, validate, protect (dinamically with AES Envelope encryption), and stream your MP4 Videos.
This example does the complete aes workflow from uploading an already encode MP4 file,
validate it with the Azure Media Packager; protecting the asset with aes encryption (content key
configuration, authorization policies, and etc), as well as configuring the HLS delivery policy.  
```
export PYTHONDONTWRITEBYTECODE=1; python3 aes_workflow_from_mp4.py
```

### AES WORKFLOW (From RAW)

# Upload, encode, protect (dinamically with AES Envelope encryption), and stream your Raw Video.
This example does the complete aes workflow from uploading an mezzanine video file,
encode it with the Azure Encoder; protecting the asset with aes encryption (content key
configuration, authorization policies, and etc), as well as configuring the HLS delivery policy.  
```
export PYTHONDONTWRITEBYTECODE=1; python3 aes_workflow_from_raw.py
```
