#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-29-2023

Purpose: print a few relevant attributes of the interfaces of a specific NXOS switch.
"""


import requests
import json


###The following 19 lines after this comment were provided to work with a specific device in a Cisco DevNet Sandbox instance.
###They contain certain parameters for requesting configuration information from a specific NXOS switch.
###The final line of the 19 is the actual API request.
switchuser='cisco'
switchpassword='cisco'

url='https://10.10.20.177/ins'
myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show ip interface brief",
      "version": 1
    },
    "id": 1
  }
]

#api request to an NXOS switch (dist-sw01) -- note: "verify=False" is to accept an untrusted certificate from the responding server.
response = requests.post(url, data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser,switchpassword)).json()


"""
New code starts here
"""
###function that receives the list of interfaces contained within the JSON object returned by the API in response to "show ip interface brief"
###and prints the interface name, protocol/link statuses, and the IP address (without the subnet mask)
def print_interfaces(intf_list):

    #print the list header with even spacing
    print(f"{'Name':10}", f"{'Proto':10}", f"{'Link':10}", "Address" )

    #using a for loop to iterate through the list of dictionaries that contain attributes of the interfaces and print them with even spacing
    for intf in intf_list:
        print(f"{intf['intf-name']:10}", f"{intf['proto-state']:10}", f"{intf['link-state']:10}", f"{intf['prefix']:10}")

    return None

#'ROW_intf' is a key in a nested dictionary that is associated with a list object that contains several interface dictionaries
interfaces = response["result"]["body"]["TABLE_intf"]["ROW_intf"]

#main
print_interfaces(interfaces)
    


