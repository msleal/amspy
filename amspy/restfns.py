"""
Copyright (c) 2016, Marcelo Leal
Description: Simple Azure Media Services Python library
License: MIT (see LICENSE.txt file for details)
"""

# restfns - REST functions for amspy

import requests
import json
from .settings import acceptformat, charset, dsversion, mdsversion, xmsversion

# do_auth(endpoint, body, access_token)
# do an HTTP POST request for authentication (acquire an access token) and return JSON
def do_auth(endpoint, body):
    headers = {"content-type": "application/x-www-form-urlencoded",
                "Expect" : "100-continue",
                "Accept": acceptformat}
    return requests.post(endpoint, data=body, headers=headers)

# do_get(endpoint, access_token)
# do an HTTP GET request and return JSON
def do_get(endpoint, path, access_token):
    headers = {"Content-Type": acceptformat,
		"DataServiceVersion": dsversion,
		"MaxDataServiceVersion": mdsversion,
		"Accept": acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    body = ''
    response = requests.get(endpoint, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.get(redirected_url, data=body, headers=headers)
    return response

# do_put(endpoint, body, access_token)
# do an HTTP PUT request and return JSON
def do_put(endpoint, body, access_token):
    headers = {"content-type": acceptformat,
		"Accept": acceptformat,
		"DataServiceVersion": dsversion,
		"MaxDataServiceVersion": mdsversion,
		"Accept-Charset" : charset,
		"x-ms-version" : xmsversion,
		"Expect": "100-continue",
		"Authorization": "Bearer " + access_token}
    return requests.put(endpoint, data=body, headers=headers)

# do_post(endpoint, body, access_token)
# do an HTTP POST request and return JSON
def do_post(endpoint, path, body, access_token):
    headers = {"Content-Type": acceptformat, 
		"DataServiceVersion": dsversion,
		"MaxDataServiceVersion": mdsversion,
		"Accept": acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    response = requests.post(endpoint, data=body, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.post(redirected_url, data=body, headers=headers)
    return response

# do_patch(endpoint, path, body, access_token)
# do an HTTP PATCH request and return JSON
def do_patch(endpoint, path, body, access_token):
    headers = {"Content-Type": acceptformat, 
		"DataServiceVersion": dsversion,
		"MaxDataServiceVersion": mdsversion,
		"Accept": acceptformat,
		"Accept-Charset" : charset,
		"Authorization": "Bearer " + access_token,
		"x-ms-version" : xmsversion}
    response = requests.patch(endpoint, data=body, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.patch(redirected_url, data=body, headers=headers)
    return response

# do_delete(endpoint, access_token)
# do an HTTP DELETE request and return JSON
def do_delete(endpoint, path, access_token):
    headers = {"DataServiceVersion": dsversion,
		"MaxDataServiceVersion": mdsversion,
		"Accept": acceptformat,
		"Accept-Charset" : charset,
		"Authorization": 'Bearer ' + access_token,
		"x-ms-version" : xmsversion}
    response = requests.delete(endpoint, headers=headers, allow_redirects=False)
    # AMS response to the first call can be a redirect, 
    # so we handle it here to make it transparent for the caller...
    if (response.status_code == 301):
         redirected_url = ''.join([response.headers['location'], path])
         response = requests.delete(redirected_url, headers=headers)
    return response

# do_sto_put(endpoint, body, access_token)
# do an HTTP PUT request to the azure storage api and return JSON
def do_sto_put(endpoint, body, content_length, access_token):
    headers = {"Accept": acceptformat,
		"Accept-Charset" : charset,
		"x-ms-blob-type" : "BlockBlob",
		"x-ms-meta-m1": "v1",
		"x-ms-meta-m2": "v2",
		"x-ms-version" : "2015-02-21",
		"Content-Length" : content_length}
    return requests.put(endpoint, data=body, headers=headers)
