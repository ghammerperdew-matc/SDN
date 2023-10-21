#!/usr/bin/env python3


"""
Author: Gavin Hammer-Perdew
Date created: 10-21-2023

Purpose: make API calls to two distribution switches to modify the addresses on the VLAN interfaces
as a proof of concept for performing this function on many devices in a large network.
"""


import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

#receives a management IP address for a device
#sends an API request to that device with the "show ip interface brief" command
#returns the dictionary containing the interface interfaces
def show_IP_interface_brief(mgmt_address):

    switchuser='cisco'
    switchpassword='cisco'
    url='https://' + mgmt_address + '/ins'
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

    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()

    #ROW_intf is a dictionary key with a value of the list of dictionaries containing the interface information
    interfaces = response["result"]["body"]["TABLE_intf"]["ROW_intf"]

    return interfaces


#receives a list of dictionaries containing interface information
#compiles a new list of dictionaries for only VLAN interfaces
#returns that list
def select_vlan_interfaces(interface_list):

    #creates empty list to which to append interface dictionaries
    vlan_interfaces = []

    #iterates through the interface dictionaries and appends those which have a name that contains "vlan" to the vlan_interfaces list
    #.lower() used to negate case differences between devices
    for interface in interface_list:
        if "vlan" in interface["intf-name"].lower():
            vlan_interfaces.append(interface)

    return vlan_interfaces


#function that receives the list of interfaces contained within the JSON object returned by the API in response to "show ip interface brief"
#and prints the interface name, protocol/link statuses, and the IP address (without the subnet mask)
def print_interfaces(intf_list):

    #print the list header with even spacing
    print(f"{'Name':10}", f"{'Proto':10}", f"{'Link':10}", "Address" )

    #using a for loop to iterate through the list of dictionaries that contain attributes of the interfaces and print them with even spacing
    for intf in intf_list:
        print(f"{intf['intf-name']:10}", f"{intf['proto-state']:10}", f"{intf['link-state']:10}", f"{intf['prefix']:10}")

    print("\n")

    return None


###receives and IP address, octet to modify (1-4) and offset (how much to change it by)
###checks validity of octet number and offset
###if both valid, adds the specified amount to the value of specified octet (ex: 192.168.1.1 --> 192.168.3.1)
###returns modified address or "-1" for invalid octet anbd "-2" for invalid offset
def add_val(IP_address, octet, offset):

    if octet <= 4 and octet > 0:
        octet = octet-1

        IP_address = IP_address.split(".")

        if (int(IP_address[octet]) + offset) < 0 or (int(IP_address[octet]) + offset) > 255:
            new_IP_address = "-2"
        else:
            IP_address[octet] = str(int(IP_address[octet]) + offset)
            new_IP_address = ".".join(IP_address)
        
    else:
        new_IP_address = "-1"

    return new_IP_address


#receives a management IP address, interface name, new address and subnet mask to be assigned to the received interface
#makes an API call to the device at the recieve management address to change the IP address on the received interface
####this assumes that the management address, interface, new address and subnet mask have been verified####
#returns the response from the device -- if everything worked, it will contain almost nothing, but any errors that occur will be returned otherwise
def change_interface_address(mgmt_address, int_name, new_address, subnet_mask):

    switchuser='cisco'
    switchpassword='cisco'
    url='https://' + mgmt_address + '/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "configure terminal",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "interface " + int_name,
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip address " + new_address + " " + subnet_mask,
          "version": 1
        },
        "id": 3
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "exit",
          "version": 1
        },
        "id": 4
      }
    ]

    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()
    
    return response


#receives nothing, returns nothing
#iterates through dictionary of devices and increments the 4th octet of the VLAN iterface IP addresses on all devices by 5
def main():

    devices = {
        "dist-sw01":"10.10.20.177",
        "dist-sw02":"10.10.20.178"
        }

    for key in devices:

        mgmt_address = devices[key]
        
        print("*" * 15)
        print("**", key, "**")
        print("*" * 15 + "\n")
    
        #get "show ip interface brief" output
        full_IP_intf_list = show_IP_interface_brief(mgmt_address)
        
        #select only VLAN interfaces and append them to new list
        #(easier to work with lists when you don't have to exclude items)
        vlan_IP_intf_list = select_vlan_interfaces(full_IP_intf_list)
        
        #print the full list of ints in a nice format
        print("Current interface IP addresses: \n")
        print_interfaces(full_IP_intf_list)

        #iterate through list of VLAN int dictionaries to modify the addresses and update the dictionaries with the new addresses
        for intf in vlan_IP_intf_list:
            new_IP_address = add_val(intf['prefix'], 4, 5)

            #checks add_val return for error codes and either changes the address in the dictionary or prints a custom error message
            if new_IP_address != "-1" and new_IP_address != "-2":
                intf['prefix'] = new_IP_address
            elif new_IP_address == "-1":
                print("Error: invalid octet range for:", intf['intf-name'])
            else:
                print("Error: invalid offset for:", intf['intf-name'], "-- new octet value would be out of range")

        #iterate through the updated list of dictionaries and make API calls to the switch to change the addresses on the VLAN interfaces
        for intf in vlan_IP_intf_list:
            api_response = change_interface_address(mgmt_address, intf['intf-name'], intf['prefix'], '255.255.255.0')

        #get "show IP interface brief" output (again) to show new addresses on the interfaces
        full_IP_intf_list = show_IP_interface_brief(mgmt_address)
        
        #print the list of VLAN ints in a nice format (again)
        print("Updated interface IP addresses: \n")
        print_interfaces(full_IP_intf_list)



main()
