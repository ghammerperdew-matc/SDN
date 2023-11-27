#!/usr/bin/env python3


import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager
from collections import OrderedDict

router = {"host": "10.10.20.48", "port" : "830",
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

print(f"{'Interface':20}", f"{'IP Address':20}", f"{'Subnet Mask':20}", 'Description', '\n' + "-"*70)

for interface in interfaces:
    
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
