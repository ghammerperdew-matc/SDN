#!/usr/bin/env python3

import requests
import json
import urllib3

#suppress certificate warning
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


###receives and IP address (in CIDR form), octet to modify (1-4) and offset (how much to change it by)
###checks validity of octet number and offset
###if both valid, adds the specified amount to the value of specified octet (ex: 192.168.1.1 --> 192.168.3.1)
###returns modified address (with same netmask attached) or "-1" for invalid octet and "-2" for invalid offset
def increment_CIDR_address(CIDR_address, octet, offset):

    if octet <= 4 and octet > 0:
        octet = octet-1

        IP_address = CIDR_address.split("/")

        IP_address[0] = IP_address[0].split(".")

        if (int(IP_address[0][octet]) + offset) < 0 or (int(IP_address[0][octet]) + offset) > 255:
            new_IP_address = "-2"
        else:
            IP_address[0][octet] = str(int(IP_address[0][octet]) + offset)
            IP_address[0] = ".".join(IP_address[0])
            new_IP_address = "/".join(IP_address)
        
    else:
        new_IP_address = "-1"

    return new_IP_address


###receives and IP address (no netmask), octet to modify (1-4) and offset (how much to change it by)
###checks validity of octet number and offset
###if both valid, adds the specified amount to the value of specified octet (ex: 192.168.1.1 --> 192.168.3.1)
###returns modified address or "-1" for invalid octet anbd "-2" for invalid offset
def increment_address(IP_address, octet, offset):

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


#receives an IP address (assumed to be completely valid) and a value for the fourth octet
#sets the value of the fourth octet of the given address to the specified value
#returns the new IP address -- to be utilized in configuring HSRP
def calculate_HSRP_address(IP_address, fourth_octet_value):

    IP_address = IP_address.split(".")

    IP_address[3] = str(fourth_octet_value)

    IP_address = ".".join(IP_address)

    return IP_address


#receives an IP address of an NX-OS device
#makes call to the device at that IP for a session cookie
#returns the cookie
"""ONLY NX-OS DEVICES"""
def get_cookie(address) :
    #Get Session Cookie
    url = "https://"+ address +"/api/aaaLogin.json"

    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "admin",
                    "pwd" : "RG!_Yw200"}
               }
          }

    response = requests.post(url, json=payload, verify = False)

    #test = response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
    
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]


#receives a management IP address of a device and an auth cookie for said device (NX-OS devices only)
#uses address and cookie to make a GET request for interface information (IPv4 interfaces)
#returns a list of dictionaries containing interface data
"""ONLY NX-OS DEVICES"""
def get_interfaces(addr, cookie):

    url = "https://" + addr + "/api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"

    #API payload -- empty because it's a GET request
    payload = {}

    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    #send API post request
    response = requests.request("GET", url, verify = False, headers=headers, data=json.dumps(payload)).json()
    response = response["imdata"]

    return response


#receives a management IP address of a device, a list of dictionaries containing IPv4 interface info (no addr info), and an auth cookie for said device (NX-OS devices only)
###must use get_interfaces() function to retrieve list of interface dicts
#iterates the list and gets the address info for each interface (full dict of IPv4 addr information)
#returns the list of dictionaries
def get_interface_address(addr, intf_name, cookie):

    url = "https://" + addr + "/api/node/mo/sys/ipv4/inst/dom-default/if-[" + intf_name + "].json?query-target=children"

    #API payload -- empty because it's a GET request
    payload = {}

    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    #send API post request
    response = requests.request("GET", url, verify = False, headers=headers, data=json.dumps(payload)).json()

    intf_address = response["imdata"][0]["ipv4Addr"]["attributes"]["addr"]
        
    return intf_address



"""ONLY NX-OS DEVICES"""
def change_address(device_addr, cookie, interface, intf_new_addr):
    url = "https://" + device_addr + "/api/node/mo/sys/ipv4/inst/dom-default/if-[" + interface + "].json?query-target=children"

    payload = {
        "ipv4Addr": {
            "attributes": {
                "addr": intf_new_addr, #should be entered in CIDR notation
                "type": "primary"
                }
            }
        }

    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload)).json()

    return(response)


#receives mgmt IP address (of an NX-OS device), VLAN number, VLAN name and an auth cookie
#makes a "POST" request to the specified device address to create a new VLAN of the specified number and name
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
def create_VLAN(device_address, vlan_num, vlan_name, cookie):
    
    url = "https://" + device_address + "/api/mo/sys/bd.json"

    payload = {
        "bdEntity": {
          "children": [
            {
              "l2BD": {
                "attributes": {
                  "fabEncap": "vlan-" + str(vlan_num),
                  "name": str(vlan_name),
                  "pcTag": "1" #this attribute is not necessary -- it is "the default classId for the unknown Unicast traffic terminating on the L2 bridge-domain"
        }}}]}}

    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()

    return response


#receives mgmt IP address (of an NX-OS device), VLAN number, VLAN SVI address and mask (CIDR notation) and an auth cookie
#sends a "POST" request to the specified device address to create a VLAN SVI for the specified VLAN number and assigns the specified IP address/mask
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
def create_VLAN_SVI(device_address, vlan_num, vlan_svi_CIDR_addr, cookie):
    #vlan_svi_CIDR_address must have the full IP address with the mask in this format: x.x.x.x/mm
    
    url = "https://" + device_address + "/api/mo/sys.json"

    payload = {
        "topSystem": {
          "children": [
            {
              "interfaceEntity": {
                "children": [
                  {
                    "sviIf": {
                      "attributes": {
                        "id": "vlan" + str(vlan_num),
                        "adminSt": "up",
                        "autostate": "no"
        }}}]}},
            {
              "ipv4Entity": {
                "children": [
                  {
                    "ipv4Inst": {
                      "children": [
                        {
                          "ipv4Dom": {
                            "attributes": {
                              "name": "default"
                            },
                            "children": [
                              {
                                "ipv4If": {
                                  "attributes": {
                                    "id": "vlan" + str(vlan_num)
                                  },
                                  "children": [
                                    {
                                      "ipv4Addr": {
                                        "attributes": {
                                          "addr": vlan_svi_CIDR_addr
        }}}]}}]}}]}}]}}]}}

    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()

    return response


#receives mgmt IP address (from NX-OS device) and an auth cookie
#sends a "POST" request to the specified device address to enable the HSRP feature (just in case it's not already enabled)
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
def enable_HSRP(device_addr, cookie):
    
    url = "https://" + device_addr + "/api/mo/sys.json"

    payload = {
          "topSystem": {
            "children": [
              {
                "fmEntity": {
                  "children": [
                    {
                      "fmHsrp": {
                        "attributes": {
                          "adminSt": "enabled"
                        }
                      }
                    }
                  ]
                }
              }
            ]
          }
        }

    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()

    return response


#receives mgmt IP address, VLAN virtual interface (SVI) name (ex: 'vlan101'), HSRP group, HSRP address and an auth cookie
#sends a "POST" request to the specified device address to configure the specified VLAN's SVI for Hot Standby Routing with the specified HSRP information
#HSRP priority defaults to 100, but an optional parameter can be used to set it to something else
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
def VLAN_SVI_HSRP(device_addr, cookie, SVI_name, HSRP_group, HSRP_addr, HSRP_priority="100"):
    
    url = "https://" + device_addr + "/api/mo/sys.json"

    payload = {
        "topSystem": {
          "children": [
            {
              "hsrpEntity": {
                "children": [
                  {
                    "hsrpInst": {
                      "children": [
                        {
                          "hsrpIf": {
                            "attributes": {
                              "id": SVI_name
                            },
                            "children": [
                              {
                                "hsrpGroup": {
                                  "attributes": {
                                    "af": "ipv4",
                                    "id": str(HSRP_group),
                                    "ip": HSRP_addr,
                                    "ipObtainMode": "admin",
                                    "prio": HSRP_priority
                                  }
                                }
                              }
                            ]
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            },
            {
              "interfaceEntity": {
                "children": [
                  {
                    "sviIf": {
                      "attributes": {
                        "id": SVI_name
                      }
                    }
                  }
                ]
              }
            }
          ]
        }
      }
    
    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()

    return response


#receives mgmt IP address, VLAN virtual interface (SVI) name (ex: 'vlan101'), OSPF process ID number (int or str), OSPF area (str or int) and an auth cookie
#sends a "POST" request to the specified device address to configure the specified VLAN's SVI for Open-Shortest-Path-First routing with the specified OSPF info
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
def VLAN_SVI_OSPF(device_addr, SVI_name, OSPF_process, OSPF_area, cookie):

    url = "https://" + device_addr + "/api/mo/sys.json"

    payload = {
        "topSystem": {
          "children": [
            {
              "ospfEntity": {
                "children": [
                  {
                    "ospfInst": {
                      "attributes": {
                        "name": str(OSPF_process)
                      },
                      "children": [
                        {
                          "ospfDom": {
                            "attributes": {
                              "name": "default"
                            },
                            "children": [
                              {
                                "ospfIf": {
                                  "attributes": {
                                    "advertiseSecondaries": "yes",
                                    "area": str(OSPF_area),
                                    "id": SVI_name
                                  }
                                }
                              }
                            ]
                          }
                        }
                      ]
                    }
                  }
                ]
              }
            },
            {
              "interfaceEntity": {
                "children": [
                  {
                    "sviIf": {
                      "attributes": {
                        "id": SVI_name
                      }
                    }
                  }
                ]
              }
            }
          ]
        }
      }

    
    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()

    return response


#receives a device IP address
#makes RESTCONF call for device interface information
#returns list of dictionaries containing device information
"""ONLY IOS-XE DEVICES"""
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


#receives a device IP address, name of intf to modify, new address for said interface and new netmask
#makes RESTCONF call to the given device to change the IP address/netmask on the provided interface -- assumes all info is accurate/valid
#returns the response from the device (good to keep in case troubleshooting is necessary) -- response code should be 204 for success
"""ONLY IOS-XE DEVICES"""
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


# Function to load inventory from a JSON file and convert it to a dictionary
def load_inventory(filename):
    try:
        with open(filename, 'r') as file:
            inventory_data = json.load(file)
        return inventory_data
    except FileNotFoundError:
        return []



def main():

    """this list of dictionaries currently resides in a JSON file and is called by the load_inventory() function"""
    devices = [
        {
            "hostname": "dist-sw01",
            "type": "NX-OS",
            "mgmtIP": "10.10.20.40"
        },
        {
            "hostname": "dist-sw02",
            "type": "None",
            "mgmtIP": "10.10.20.178"
        },
        {
            "hostname": "dist-rtr01",
            "type": "None",
            "mgmtIP": "10.10.20.48"
        },
        {
            "hostname": "dist-rtr02",
            "type": "None",
            "mgmtIP": "10.10.20.176"
        }
        ]

    #devices = load_inventory("inventory.json")

    #counts how many devices a new VLAN has been created/configured on
    ##it is used to increment the IP address for the VLAN SVI
    new_vlan_device_counter = 1

    for device in devices:

        #NX-OS process
        if device['type'] == "NX-OS":

            device_address = device['mgmtIP']
            
            cookie = get_cookie(device_address)
            
            interface_list = get_interfaces(device_address, cookie)
            
            for interface in interface_list:
                #reconfigure IP addresses (increment from 172.16.x.x to 172.31.x.x)
                interface_name = interface['ipv4If']['attributes']['id']
                interface_address = get_interface_address(device_address, interface_name, cookie)
                new_interface_address = increment_CIDR_address(interface_address, 2, 15)
                change_address_response = change_address(device_address, cookie, interface_name, new_interface_address)
                if len(change_address_response['imdata']) == 0:
                    print(f"{interface_name} IP address changed to {new_interface_address}")
                else:
                    print(f"Error: {change_address_response}")
                
                if "vlan" in interface_name.lower():
                    #reconfigure HSRP on VLAN SVIs (using new addresses with the same group that was previously configured)
                    HSRP_address = calculate_HSRP_address(new_interface_address, 1)
                    HSRP_group = 10
                    VLAN_SVI_HSRP_response = VLAN_SVI_HSRP(device_address, cookie, interface_name, HSRP_group, HSRP_address)
                    if len(VLAN_SVI_HSRP_response['imdata']) == 0:
                        print(f"{interface_name} added to HSRP group {HSRP_group} with address {HSRP_address}")
                    else:
                        print(f"Error: {VLAN_SVI_HSRP_response}")

                    #reconfigure OSPF on VLAN SVIs (OSPF process 1, area 0.0.0.0)
                    OSPF_process = 1
                    OSPF_area = "0.0.0.0"
                    VLAN_SVI_OSPF_response = VLAN_SVI_OSPF(device_address, interface_name, OSPF_process, OSPF_area, cookie)
                    if len(VLAN_SVI_OSPF_response['imdata']) == 0:
                        print(f"{interface_name} added to OSPF process {OSPF_process} in OSPF area {OSPF_area}")
                    else:
                        print(f"Error: {VLAN_SVI_OSPF_response}")

            #create VLAN 120
            vlan_num = 120
            vlan_name = "script"
            vlan_default_CIDR_address = "172.31.120.1/24"
            vlan_svi_CIDR_address = increment_CIDR_address(vlan_default_CIDR_address, 4, new_vlan_device_counter)

            create_VLAN_120 = create_VLAN(device_address, vlan_num, vlan_name, cookie)
            if len(create_VLAN_120['imdata']) == 0:
                print(f"Created VLAN {vlan_num}")
            else:
                print(f"Error: {create_VLAN_120}")                

            create_VLAN_SVI_120 = create_VLAN_SVI(device_address, vlan_num, vlan_svi_CIDR_address, cookie)
            if len(create_VLAN_SVI_120['imdata']) == 0:
                print(f"Created VLAN {vlan_num} SVI")
            else:
                print(f"Error: {create_VLAN_SVI_120}")  

            #VLAN 120 HSRP
            HSRP_address = vlan_default_CIDR_address
            HSRP_group = 10
            interface_name = "Vlan120"
            VLAN_SVI_HSRP_response = VLAN_SVI_HSRP(device_address, cookie, interface_name, HSRP_group, HSRP_address)
            if len(VLAN_SVI_HSRP_response['imdata']) == 0:
                print(f"{interface_name} added to HSRP group {HSRP_group} with address {HSRP_address}")
            else:
                print(f"Error: {VLAN_SVI_HSRP_response}")

            #VLAN 120 OSPF
            OSPF_process = 1
            OSPF_area = "0.0.0.0"
            VLAN_SVI_OSPF_response = VLAN_SVI_OSPF(device_address, interface_name, OSPF_process, OSPF_area, cookie)
            if len(VLAN_SVI_OSPF_response['imdata']) == 0:
                print(f"{interface_name} added to OSPF process {OSPF_process} in OSPF area {OSPF_area}")
            else:
                print(f"Error: {VLAN_SVI_OSPF_response}")

            new_vlan_device_counter += 1
            
        #IOS-XE process
        if device['type'] == "IOS-XE":

            #use the value of mgmtIP to connect to IOS-XE management addresses
            get_iosxe_address = device['mgmtIP']

            #make API call to obtain list of interfaces
            iosxe_interface_list = get_int_rest(get_iosxe_address)

            #iterate through each interface on IOS-XE devices
            for interface in iosxe_interface_list:
               #print(interface)
                
                #set interface name to interface being configured
                interface_name = interface['name']
                
                #if interface_name chooses the management port or loopback0, ignore it
                if interface_name in ["GigabitEthernet1", "VirtualPortGroup0"]:
                    #continues to end of loop, skipping following code
                    continue
                


                if interface["type"] == "iana-if-type:ethernetCsmacd":
                    if len(interface['ietf-ip:ipv4']) != 0:
                        #get IP address
                        current_addr = interface['ietf-ip:ipv4']['address'][0]['ip']
                        #get netmask
                        netmask = interface['ietf-ip:ipv4']['address'][0]['netmask']
                        print("Current: ", interface_name, current_addr, netmask)
                                  
                        #modify the current address from 172.16.x.x to 172.31.x.x
                        new_addr = increment_address(current_addr, 2, -15)

                        #notice user of changes underway
                        #print(f"Updated {interface_name} IP address to {new_addr}")
                        print("New: ", interface_name, new_addr, netmask)
                        
                        #make API call to change address on the interface
                        new_interface_specs = change_intf_address(device["mgmtIP"], interface_name, new_addr, netmask)
                        print("API call status: ", new_interface_specs)



main()
