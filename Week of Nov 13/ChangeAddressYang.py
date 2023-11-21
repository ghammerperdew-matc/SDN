import requests
import json


url = "https://10.10.20.175:443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"
username = 'cisco'
password = 'cisco'
payload={"ietf-interfaces:interface": {
                    "name": "GigabitEthernet2",
                    "description": "Configured by RESTCONF",
                    "type": "iana-if-type:ethernetCsmacd",
                    "enabled": "true",
                                     "ietf-ip:ipv4": {
                                                            "address": [{
                                                                "ip": "172.16.252.21",
                                                                "netmask": "255.255.255.252"
                                                                
                                                                        }   ]
                                                        }
                                        }
         }

headers = {
  'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
  'Accept': 'application/yang-data+json',
  'Content-Type': 'application/yang-data+json'
}

response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload)
)
print(response.text)
