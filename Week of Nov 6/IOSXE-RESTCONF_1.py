#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 10-31-2023

Purpose: make a RESTCONF api call to a device to get interface information and then print it in a readable format
"""

import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#receives an IP address of a device to which to make an API call (RESTCONF)
#calls for list of interfaces and associated information
#returns list of dictionaries containing interface information
def get_Ints(device_IP):
    url = "https://" + device_IP + ":443/restconf/data/ietf-interfaces:interfaces"

    username = 'developer'
    password = 'C1sco12345'
    payload={}
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    #requests nested dictionary/list of dictionaries of interfaces and makes it a json (dict) object
    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload).json()

    #selects only the list of interface dictionaries from the nested structure
    intf_list = response["ietf-interfaces:interfaces"]["interface"]

    return(intf_list)


#receives a list of dictionaries containing interface information
#iterates the list and prints the address and status of each interface (or notes lack of address)
#returns nothing
def print_Int(intf_list):
    
    for intf in intf_list:

        name = intf["name"]

        #get the status of the interface
        if intf["enabled"] == True:
            status = "UP"
        else:
            status = "DOWN"

        #if the IPv4 nested dictionary is not empty, it assigns that info to variable to be printed
        #otherwise a statement is printed saying there is no address along with the other info
        if len(intf["ietf-ip:ipv4"]) != 0:
            
            address = intf["ietf-ip:ipv4"]["address"][0]["ip"]
            netmask = intf["ietf-ip:ipv4"]["address"][0]["netmask"]

            print(f"{name:20}", f"{status:8}", f"{address:17}", netmask)

        else:
            print(f"{name:20}", f"{status:8}", f"{'No IP Address':17}", "No Netmask")

    return(None)


#main -- receives nothing, returns nothing
def main():

    device_IP = "10.10.20.48"

    intf_list = get_Ints(device_IP)

    print_Int(intf_list)



main()
