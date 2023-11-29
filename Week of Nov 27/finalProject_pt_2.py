#!/usr/bin/env python3

import requests
import json
import urllib3

#suppress certificate warning
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


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


#receives an IP address of an NX-OS device
#makes call to the device at that IP for a session cookie
#returns the cookie
"""ONLY NX-OS DEVICES"""
def getCookie(address) :
    #Get Session Cookie
    url = "https://"+ address +"/api/aaaLogin.json"

    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    
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
    response = requests.request("GET", url, verify = False, headers=headers, data=json.dumps(payload))
    response = response.json()["imdata"]

    return response


#receives mgmt IP address (of an NX-OS device), VLAN number, VLAN name and an auth cookie
#makes a "POST" request to the specified device address to create a new VLAN of the specified number and name
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
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


#receives mgmt IP address (of an NX-OS device), VLAN number, VLAN SVI address and mask (CIDR notation) and an auth cookie
#sends a "POST" request to the specified device address to create a VLAN SVI for the specified VLAN number and assigns the specified IP address/mask
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
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


#receives mgmt IP address, VLAN number, HSRP group, HSRP address and an auth cookie
#sends a "POST" request to the specified device address to configure the specified VLAN's SVI for Hot Standby Routing with the specified HSRP information
#returns the API response from the device
"""ONLY NX-OS DEVICES"""
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
"""ONLY NX-OS DEVICES"""
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



def main():

    devices = [
        {
            "hostname": "dist-sw01",
            "type": "NX-OS",
            "mgmtIP": "10.10.20.177"
        },
        {
            "hostname": "dist-sw02",
            "type": "NX-OS",
            "mgmtIP": "10.10.20.178"
        },
        {
            "hostname": "dist-rtr01",
            "type": "IOS-XE",
            "mgmtIP": "10.10.20.175"
        },
        {
            "hostname": "dist-rtr02",
            "type": "IOS-XE",
            "mgmtIP": "10.10.20.176"
        }
        ]
    

    for device in devices:

        if device['type'] == "NX-OS":

            address = device['mgmtIP']
            
            get_cookie(address)

            #reconfigure addresses
                #get dictionary of interfaces with addresses using API call
                #iterate the dictionary of interfaces
                    #use add_val() to increment the second octet of the address (needs to be x.31.x.x)
                    #use another API call to change the address on the interface

            #reconfigure HSRP on VLAN SVIs (using new addresses with the same group that was previously configured)

            #reconfigure OSPF on VLAN SVIs (OSPF process 1, area 0.0.0.0)


        elif device['type'] == "IOS-XE":

            address = device['mgmtIP']

            #reconfigure addresses
                #get dictionary of interfaces with addresses using API call
                #iterate the dictionary of interfaces
                    #use add_val() to increment the second octet of the address (needs to be x.31.x.x)
                    #use another API call to change the address on the interface

            #reconfigure OSPF (this is only for bonus points -- can be done manually for this assignment)
            

        else:
            print("Invalid JSON object in file")

        
