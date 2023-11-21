
###Code from youtube.com/watch?v=kESU4Y8DJ2A

import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager

router = {"host": "10.10.20.175", "port" : "830",
          "username":"cisco","password":"cisco"}

with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
    ip_schema = m.get_schema('ietf-interfaces')
    root=ET.fromstring(ip_schema.xml)
    yang_tree = list(root)[0].text
    f = open('ietf-interfaces.yang','w')
    f.write(yang_tree)
    f.close()
