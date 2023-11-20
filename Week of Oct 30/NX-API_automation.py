#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-17-2023

Purpose: Create a new VLAN and VLAN SVI, then configure that SVI (including HSRP and OSPF configuration)
"""

import requests
import json
import urllib3


#suppress certificate warning
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


#receives a management IP address of a device
#makes POST request to get an auth cookie
#returns the cookie
def getCookie(addr) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]


#receives mgmt IP address, VLAN number, VLAN name and an auth cookie
#makes a "POST" request to the specified device address to create a new VLAN of the specified number and name
#returns the API response from the device
def create_VLAN(IP_addr, vlan_num, vlan_name, cookie):
    
    url = "https://" + IP_addr + "/api/mo/sys/bd.json"

    payload = {
        "bdEntity": {
          "children": [
            {
              "l2BD": {
                "attributes": {
                  "fabEncap": "vlan-" + vlan_num,
                  "name": vlan_name,
                  "pcTag": "1" #this attribute is not necessary -- it is "the default classId for the unknown Unicast traffic terminating on the L2 bridge-domain"
        }}}]}}

    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()

    return response


#receives mgmt IP address, VLAN number, VLAN SVI address and mask (CIDR notation) and an auth cookie
#sends a "POST" request to the specified device address to create a VLAN SVI for the specified VLAN number and assigns the specified IP address/mask
#returns the API response from the device
def create_VLAN_SVI(device_addr, vlan_num, vlan_svi_CIDR_addr, cookie):
    #vlan_svi_CIDR_address must have the full IP address with the mask in this format: x.x.x.x/mm
    
    url = "https://" + device_addr + "/api/mo/sys.json"

    payload = {
        "topSystem": {
          "children": [
            {
              "interfaceEntity": {
                "children": [
                  {
                    "sviIf": {
                      "attributes": {
                        "id": "vlan" + vlan_num,
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
                                    "id": "vlan" + vlan_num
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


#receives mgmt IP address, VLAN number, HSRP group, HSRP address and an auth cookie
#sends a "POST" request to the specified device address to configure the specified VLAN's SVI for Hot Standby Routing with the specified HSRP information
#returns the API response from the device
def VLAN_SVI_HSRP(device_addr, vlan_num, HSRP_group, HSRP_addr, cookie):
    
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
                              "id": "vlan" + vlan_num
                            },
                            "children": [
                              {
                                "hsrpGroup": {
                                  "attributes": {
                                    "af": "ipv4",
                                    "id": HSRP_group,
                                    "ip": HSRP_addr,
                                    "ipObtainMode": "admin"
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
                        "id": "vlan" + vlan_num
                      }
                    }
                  }
                ]
              }
            },
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


#receives mgmt IP address, VLAN number, OSPF process ID, OSPF area and an auth cookie
#sends a "POST" request to the specified device address to configure the specified VLAN's SVI for Open-Shortest-Path-First routing with the specified OSPF info
#returns the API response from the device
def VLAN_SVI_OSPF(device_addr, vlan_num, OSPF_process, OSPF_area, cookie):

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
                        "name": OSPF_process
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
                                    "area": OSPF_area,
                                    "id": "vlan" + vlan_num
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
                        "id": "vlan" + vlan_num
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


#receives nothing
#iterates a dictionary of devices and uses the information to make API requests to the devices,
#which create a new VLAN and configure a VLAN SVI with specified settings (including HSRP and OSPF)
#returns nothing
def main():

    devices = [
        {
            "hostname": "dist-sw01",
            "mgmtIP": "10.10.20.177"
        },
        {
            "hostname": "dist-sw02",
            "mgmtIP": "10.10.20.178"
        }
        ]

    #device_count variable is used for the 'offset' parameter in the add_val() function for incrementing IP addresses for device interfaces
    #it is incremented at the end of the for loop that iterates the 'devices' dictionary
    device_count = 1

    for device in devices:
        
        address = device['mgmtIP']

        cookie = getCookie(address)

        new_VLAN_num = "110"
        new_VLAN_name = "testNXOS"
        
        #take the base address of the VLAN and increment it with the device count to get the proper value in the 4th octet
        VLAN_SVI_address = add_val("172.16.110.1", 4, device_count)
        #netmask for IP address in CIDR format (/xx)
        VLAN_SVI_netmask = "/24"
        #combine the address and netmask for a full address in CIDR format
        VLAN_SVI_CIDR_address = VLAN_SVI_address + VLAN_SVI_netmask

        VLAN_HSRP_group = "10"
        VLAN_HSRP_address = "172.16.110.1"

        VLAN_OSPF_process = "1"
        VLAN_OSPF_area = "0.0.0.0" #or just 'area 0' would work too
        
        #print the hostname of the device that is being configured
        print("*"*12)
        print(device['hostname'])
        print("*"*12)

        #response from the API for the following functions should be {'imdata': []} if they are successful
        #success is determined by checking the length of the list associated with 'imdata' in the returned dictionary
        #if any of the responses contains actual information, it is printed out
        new_vlan_response = create_VLAN(address, new_VLAN_num, new_VLAN_name, cookie)
        if len(new_vlan_response['imdata']) == 0:
            print("Created new VLAN:", "VLAN" + new_VLAN_num, new_VLAN_name)
        else:
            print("ERROR\n", new_vlan_response)

        vlan_svi_response = create_VLAN_SVI(address, new_VLAN_num, VLAN_SVI_CIDR_address, cookie)
        if len(vlan_svi_response['imdata']) == 0:
            print("Created VLAN " + new_VLAN_num + " SVI with IP address of " + VLAN_SVI_CIDR_address)
        else:
            print("ERROR\n", vlan_svi_response)

        vlan_hsrp_response = VLAN_SVI_HSRP(address, new_VLAN_num, VLAN_HSRP_group, VLAN_HSRP_address, cookie)
        if len(vlan_hsrp_response['imdata']) == 0:
            print("VLAN " + new_VLAN_num + " SVI configured in HSRP group " + VLAN_HSRP_group + " with HSRP address of " + VLAN_HSRP_address)
        else:
            print("ERROR\n", vlan_hsrp_response)

        vlan_ospf_response = VLAN_SVI_OSPF(address, new_VLAN_num, VLAN_OSPF_process, VLAN_OSPF_area, cookie)
        if len(vlan_ospf_response['imdata']) == 0:
            print("VLAN " + new_VLAN_num + " SVI configured in OSPF process " + VLAN_OSPF_process + " in OSPF area " + VLAN_OSPF_area, "\n")
        else:
            print("ERROR\n", vlan_ospf_response, "\n")

        device_count += 1

    return None


main()
