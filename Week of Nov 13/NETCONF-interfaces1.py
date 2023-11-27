#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-7-2023

Purpose: show a user interfaces on a given device and ask which interface on which they would like to change the IP address
"""

import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict


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


def get_interfaces(ip_addr):
    
    router = {"host": ip_addr, "port" : "830",
              "username":"developer","password":"C1sco12345"}


    netconf_filter = """
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface></interface>
        </interfaces>
    """

    with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:

        netconf_reply = m.get_config(source = 'running', filter = ("subtree", netconf_filter))

    #Parse returned XML to Dictionary
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

    #Create List of Interfaces
    interfaces = netconf_data["interfaces"]["interface"]

    return(interfaces)


def print_interfaces(intf_list):

    print(f"{'Interface':20}", f"{'IP Address':20}", f"{'Subnet Mask':20}", 'Description', '\n' + "-"*70)

    for interface in intf_list:
        
        name = interface['name']

        if "address" in interface['ipv4'].keys():
            ip_addr = interface['ipv4']['address']['ip']
            netmask = interface['ipv4']['address']['netmask']
        else:
            ip_addr = "Unassigned"
            netmask = "Unassigned"

        if "description" in interface.keys():
            description = interface['description']
        else:
            description = ""

        print(f"{name:20}", f"{ip_addr:20}", f"{netmask:20}", description)

    return(None)


def main():

    interfaces = get_interfaces("10.10.20.48")

    print_interfaces(interfaces)

    #while loop for getting user input for interface name
    valid_intf = False
    while valid_intf == False:
        intf_name = input("Enter the interface name you want to modify (see above list): ")
        if intf_name in str(interfaces):
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

    #while loop for getting user input for interface description
    valid_desc = False
    while valid_desc == False:
        new_desc = input("Enter a description for the interface: ")
        if new_desc.isalnum() != False:
            valid_desc = True
            print("\n")
        else:
            print("Invalid description - try again \n")


    for interface in interfaces:

        if intf_name == interface["name"]:

            if "address" in interface['ipv4'].keys():
                interface['ipv4']['address']['ip'] = new_addr
                interface['ipv4']['address']['netmask'] = new_netmask
            else:
                interface['ipv4']["address"] = {'ip':new_addr, 'netmask':new_netmask}

            interface['description'] = new_desc

    print_interfaces(interfaces)
    
    return(None)


main()
