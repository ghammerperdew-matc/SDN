#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 10-3-2023

Purpose: make API calls to two distribution switches and print the OSPF neighbors and the link statuses of each neighbor connection
"""

import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_OSPF_neighbors(mgmt_IP_address):
##  Receives the management IP address of an NX-OS switch
##  Makes an API call to that switch for OSPF neighbors
##  Returns the response from the API as a JSON object
    

    #device credentials for the specific NX-OS switch that is being targeted
    switchuser='cisco'
    switchpassword='cisco'
    
    #variables used to form an HTTPS request to the switch API
    url='https://' + mgmt_IP_address + '/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "show ip ospf neighbor", #actual command to be entered on the switch's CLI
        "version": 1
        },
        "id": 1
      }
    ]

    #verify=False is included to get around not being able to verify the site's certificate
    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()

    return(response)


def print_OSPF_neighbors(OSPF_neighbor_dict):
##  Receives a JSON object containing OSPF neighbor information
##  Prints the router ID, neighbor IP address, and connected interface for each neighbor relationship
##  Returns nothing

    neighbor_table_list = OSPF_neighbor_dict["result"]["body"]["TABLE_ctx"]["ROW_ctx"]["TABLE_nbr"]["ROW_nbr"]

    print(f"{'Router-ID':15}", f"{'Neighbor IP':15}", "Int\n" + "-"*38)
    
    for neighbor in neighbor_table_list:
        print(f"{neighbor['rid']:15}", f"{neighbor['addr']:15}", neighbor['intf'])

    return None


def main():
##  Main function receives nothing and returns nothing
##  Iterates through a dictionary to make API calls and print specific OSPF neighbor information from API responses

    #List of dictionaries containing basic device information
    devices = [
        {
        "hostname": "dist-sw01",
        "deviceType": "switch",
        "mgmtIP": "10.10.20.177"
        },
        {
        "hostname": "dist-sw02",
        "deviceType": "switch",
        "mgmtIP": "10.10.20.178"
            }
        ]

    #iterate through the device dictionaries and use the IP addresses to make API calls and print information in a readable format
    for device in devices:

        mgmtIP = device["mgmtIP"]

        print(device["hostname"], "OSPF Neighbors\n" + "-"*38)
        
        OSPF_neighbors = get_OSPF_neighbors(mgmtIP)
        print_OSPF_neighbors(OSPF_neighbors)

        print("\n")

    return None


#execute main function
main()
