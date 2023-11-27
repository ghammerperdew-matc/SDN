import xml.etree.ElementTree as ET
import xmltodict
import xml.dom.minidom
from lxml import etree
from ncclient import manager

router = {"host": "10.10.20.48", "port" : "830",
          "username":"developer","password":"C1sco12345"}

with manager.connect(host=router['host'],port=router['port'],username=router['username'],password=router['password'],hostkey_verify=False) as m:
    ip_schema = m.get_schema('ietf-inet-types')
    root=ET.fromstring(ip_schema.xml)
    yang_tree = list(root)[0].text
    f = open('ietf-inet-types.yang','w')
    f.write(yang_tree)
    f.close()
