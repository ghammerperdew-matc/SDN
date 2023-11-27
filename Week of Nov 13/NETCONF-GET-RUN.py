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

print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())

print("#" * 40)

    #Parse returned XML to Dictionary

netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

print(netconf_data)

print("d" *40)

    #Create List of Interfaces

interfaces = netconf_data["interfaces"]["interface"]

print(interfaces)

print("I" * 40)

for interface in interfaces:
    print(interface)
          
