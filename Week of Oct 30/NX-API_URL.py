#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-14-2023

Purpose: send an API request for information regarding interfaces on a device and
print the domain name and interface name of each interface from returned data
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


#receives a management IP address of a device and an auth cookie for said device
#uses address and cookie to make a GET request for interface information (IPv4 interfaces)
#returns a list of dictionaries containing interface data
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


#receives nothing
#gets auth cookie from device at given address and uses it to get interface information from device at given address
#prints the interface URL location and the interface names
#returns nothing
def main():

    address = '10.10.20.177'

    #get a cookie from the device at the given address
    cookie = getCookie(address)
    
    #list of dictionaries containing interface data
    intf_list = get_interfaces(address, cookie)
    
    #iterates list and prints interface URL and name
    for intf in intf_list:
        print(f"{intf['ipv4If']['attributes']['dn']:40}", intf["ipv4If"]["attributes"]["id"])
    


main()

