import requests
import json

def change_intf_address(device_addr, intf_name, new_addr, new_netmask):

    #print(intf_name, new_addr, new_netmask)
    url = "https://10.10.20.48:443/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet2"
    print(url)
    username = 'developer'
    password = 'C1sco12345'
    payload = {"ietf-interfaces:interface": {
                            "name": "GigabitEthernet2",
                            "description": "Configured by RESTCONF",
                            "type": "iana-if-type:ethernetCsmacd",
                            "enabled": "true",
                            "ietf-ip:ipv4": {
                                "address": [
                                    {
                                        "ip": "172.16.252.26",
                                        "netmask": "255.255.255.0"
                                    }
                                ]
                            }
                        }
                    }
    
    headers = {
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload))
    response = response.json

    return(response)


change_address = change_intf_address("10.10.20.48", "GigabitEthernet2", "172.32.20.10", "255.255.255.0")
print(change_address)
