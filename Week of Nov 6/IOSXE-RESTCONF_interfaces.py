#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-1-2023

Purpose: Request interface information from a given device two different ways and combine it into one printable list
"""

import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#receives a device IP address
#makes RESTCONF call for device interface information
#extracts a list of dictionaries containing interface info and creates a new list of dictionaries containing only intf name and IP address
#interfaces without addresses are not added to the new list of dictionaries
#returns the new list of dictionaries containing device information
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

    #new list to which to add new device dictionaries
    mod_intf_list = []

    #iterate the list of dictionaries and select info from only interfaces with an IP address to append to new list
    #new dictionaries only include intf name and IP address
    for intf in intf_list:
        if len(intf['ietf-ip:ipv4']) != 0:
            mod_intf_list.append({'name':intf['name'], 'IP_addr':intf['ietf-ip:ipv4']['address'][0]['ip']})

    return(mod_intf_list)


#receives a device IP address
#makes RESTCONF call for device interface information
#extracts a list of dictionaries containing interface info and creates a new list of dictionaries containing only intf name and MAC address
#returns the new list of dictionaries containing device information
def get_int_rest_MAC(device_IP):
    url = "https://" + device_IP + ":443/restconf/data/interfaces-state"

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
    intf_list = response["ietf-interfaces:interfaces-state"]["interface"]

    #new list to which to add new device dictionaries
    mod_intf_list = []

    #iterate the list of dictionaries and select the interface name and MAC address from all interfaces to append to new list
    for intf in intf_list:
            mod_intf_list.append({'name':intf['name'], 'MAC_addr':intf['phys-address']})

    return(mod_intf_list)


#receives two lists: one with dictionaries containing interface names and their IP addresses, the other with interfaces and their MAC addresses
#matches interfaces in the IP address list with interfaces in the MAC address list and makes a new list of the matching interfaces
#the new list includes the intf name, IP address and MAC address
#returns the combined list of dictionaries
def combine_int_lists(int_IP_list, int_MAC_list):

    combined_list = []

    #iterate interface+IP list
    for intf in int_IP_list:

        #variables to make appending to new dictionary easier
        name = intf["name"]
        address = intf["IP_addr"]

        #for each device in the intf+MAC list, see if it matches the intf in the intf+IP list
        for int_MAC in int_MAC_list:

            #if there is a match, creates a new dictionary with the relevant info and appends it to the list of dictionaries
            if name == int_MAC["name"]:
                MAC_address = int_MAC["MAC_addr"]
                combined_list.append({"name": name, "IP_addr": address, "MAC_addr": MAC_address})

    return(combined_list)


#receives list of dictionaries containing interface names, IP addresses and MAC addresses
#prints that information in a formatted list
#returns nothing
def print_combined_list(combined_list):

    print(f"{'Interface':21}", f"{'IP Address':15}", "MAC Address")
    print("-"*49)

    for intf in combined_list:

        print(f"{intf['name']:21}", f"{intf['IP_addr']:15}", intf['MAC_addr'])

    return(None)


#receives nothing
#gets original intf lists (IP and MAC lists), combines lists with matching interfaces, prints combined list 
#returns nothing
def main():

    device_IP = "10.10.20.48"

    intf_list = get_int_rest(device_IP)

    intf_state_list = get_int_rest_MAC(device_IP)

    combined_list = combine_int_lists(intf_list, intf_state_list)

    print_combined_list(combined_list)


main()
