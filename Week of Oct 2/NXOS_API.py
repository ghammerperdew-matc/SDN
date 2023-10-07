#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 10-3-2023

Purpose: make an API call to an NXOS switch to get the hostname and some memory information, and then print that to the screen
"""

import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#device credentials for the specific NX-OS switch that is being targeted
switchuser='cisco'
switchpassword='cisco'

#variables used to form an HTTPS request to the switch API
url='https://10.10.20.177/ins'
myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
    "cmd": "show version", #actual command to be entered on the switch's CLI
    "version": 1
    },
    "id": 1
  }
]

#verify=False is included to get around not being able to verify the site's certificate
response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()

#Narrow the JSON object received to have only the "body" section of the output.
#This is the dictionary where the desired information is contained.
response = response["result"]["body"]

#Select device hostname, memory and memory type from the "body" dictionary
hostname = response["host_name"]
memory_volume = response["memory"]
memory_type = response["mem_type"]

#print the hostname and memory information to the screen with formatting
print("Hostname =", hostname, "\t", "Memory =", memory_volume, memory_type)
