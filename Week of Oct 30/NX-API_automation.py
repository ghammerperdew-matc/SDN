#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-17-2023

Purpose: 
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
                        "autostate": "no",
                        "name": vlan_name
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
      }}}]}}]}}]}}]}
    
    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()

    return response



def main():
    
    address = "10.10.20.177"

    cookie = getCookie(address)

    VLAN_num = "110"
    VLAN_name = "testNXOS"
    VLAN_SVI_CIDR_addr = "172.16.110.2/24"

    #response should be {'imdata': []} if it is successful
    new_vlan_response = create_VLAN(address, VLAN_num, VLAN_name, cookie)
    print(new_vlan_response)

    vlan_svi_response = create_VLAN_SVI(address, VLAN_num, VLAN_SVI_CIDR_addr, cookie)
    print(vlan_svi_response)
