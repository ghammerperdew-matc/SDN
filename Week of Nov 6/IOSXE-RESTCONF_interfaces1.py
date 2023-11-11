#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-7-2023

Purpose: show a user interfaces on a given device and ask which interface on which they would like to change the IP address
"""

import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#receives a device IP address
#makes RESTCONF call for device interface information
#returns list of dictionaries containing device information
def get_int_rest(device_IP):
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
#prints the info in a formatted list
#returns nothing
def print_intf_list(intf_list):
    
    for intf in intf_list:

        name = intf["name"]

        if intf["enabled"] == True:
            status = "UP"
        else:
            status = "DOWN"

        if len(intf["ietf-ip:ipv4"]) != 0:
            
            address = intf["ietf-ip:ipv4"]["address"][0]["ip"]
            netmask = intf["ietf-ip:ipv4"]["address"][0]["netmask"]

            print(f"{name:20}", f"{status:8}", f"{address:17}", netmask)

        else:
            print(f"{name:20}", f"{status:8}", f"{'No IP Address':17}", "No Netmask")

    print("\n")

    return(None)


#receives a device IP address, name of intf to modify, new address for said interface and new netmask
#makes RESTCONF call to the given device to change the IP address/netmask on the provided interface -- assumes all info is accurate/valid
#returns the response from the device (good to keep in case troubleshooting is necessary) -- response code should be 204 for success
def change_intf_address(device_addr, intf_name, new_addr, new_netmask):
    url = "https://" + device_addr + ":443/restconf/data/ietf-interfaces:interfaces/interface=" + intf_name
    username = 'developer'
    password = 'C1sco12345'
    payload={"ietf-interfaces:interface": {
                        "name": intf_name,
                        "description": "Configured by RESTCONF",
                        "type": "iana-if-type:ethernetCsmacd",
                        "enabled": "true",
                                         "ietf-ip:ipv4": {
                                                                "address": [{
                                                                    "ip": new_addr,
                                                                    "netmask": new_netmask
                                                                    
                                                                            }   ]
                                                            }
                                            }
             }

    headers = {
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload)).json

    return(response)


#receives an IP address or a subnet mask
#converts it to binary and keeps the octet '.' separation
#returns it as a string
def convert_to_binary(address):

    octet_list = address.split('.')

    binary_octet_list = []

    for octet in octet_list:
        binary_octet = f"{int(octet):08b}"
        binary_octet_list.append(binary_octet)

    binary_mask = '.'.join(binary_octet_list)

    return(binary_mask)


#receives a binary netmask (octets separated by .)
#evaluates each octet for proper binary order for subnet masks in the most basic terms (no zeros before ones)
#returns True if the subnet is technically valid (not evaluating for proper range given an IP address)
#returns False if any of the octets are invalid
def validate_netmask(bin_netmask):

    valid = True

    octet_list = bin_netmask.split(".")

    for octet in octet_list:

        if "01" in octet:
            valid = False

    return(valid)


#receives an IP address
#validates the IP address
#returns True or False
def validate_address(IP_address):
        #split IP address into individual octets -- returns a list
        octet_list = IP_address.split(".")

        #assume the address is valid, create variable for "True" status
        #Will be changed to false if any issue is found
        status = True

        #validate number of octets in the list
        if len(octet_list) != 4:

            #set status to false if there are not exactly 4 octets
            status = False
                
        #validate each octet
        for octet in octet_list:
                    
            #check if there are letters in the octet
            if octet.isdigit() == False:

                status = False
                        
            #check if integer range is valid
            elif int(octet) < 0 or int(octet) > 255:
                            
                #change address status to False if invalid range
                status = False
                
        #return the value of the status variable for the function
        return status


#receives nothing
#prints interface info for given device
#asks user for input in while loops, no additional "quit" feature on this script
#uses user input to change the IP address on the user-specified interface on the given device
#returns nothing
def main():

    device_addr = "10.10.20.48"

    intf_list = get_int_rest(device_addr)

    print_intf_list(intf_list)

    #while loop for getting user input for interface name
    valid_intf = False
    while valid_intf == False:
        intf_name = input("Enter the interface name you want to modify (see above list): ")
        if intf_name in str(intf_list):
            valid_intf = True
        else:
            print("Invalid interface name - try again \n")

    #loop for getting user input for new IP address and verifying it
    valid_IP = False
    while valid_IP == False:
        new_addr = input("Enter a new valid IP address for "+ intf_name + ": ")
        valid_IP = validate_address(new_addr)
        if valid_IP == False:
            print("Invalid IP address - try again \n")

    #loop for getting user input for getting the subnet mask for the new address (and verifying it)
    valid_netmask = False
    while valid_netmask == False:
        new_netmask = input("Enter the subnet mask for the new IP address: ")
        valid_netmask = validate_netmask(new_netmask)
        if valid_netmask == False:
            print("Invalid netmask - try again \n")
            
    #make call to device to change IP address on the given interface
    restconf_call_response = change_intf_address(device_addr, intf_name, new_addr, new_netmask)
    
    #get updated list of interfaces
    intf_list = get_int_rest(device_addr)

    #print updated list of interfaces
    print_intf_list(intf_list)

    return(None)


main()

