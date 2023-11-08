import requests
import json

def getCookie(device_addr) :

#NX REST API Authen See REST API Reference for format of payload below

    url = "https://"+ device_addr + "/api/aaaLogin.json"
 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    #print(response.json())
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]


def change_address(device_addr, cookie, interface, intf_newAddr)
    url = "https://" + device_addr + "/api/node/mo/sys/ipv4/inst/dom-default/if-[" + interface + "].json?query-target=children"

    payload = {
        "ipv4Addr": {
            "attributes": {
                "addr": intf_newAddr, #should be entered in CIDR notation
                "type": "primary"
                }
            }
        }

    headers = {
        'Content-Type:': 'application/json',
        'Cookie': 'APIC-cookie=' + cookie
        }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload)).json()

    return(response)


def main():
    #Get Session Cookie for NX switch. Change address below as needed

    address = '10.10.20.177'

    #Use the cookie below to pass in request. Cookie is good for 600 seconds

    cookie = getCookie(address)

    change_address(address, cookie, "vlan101", "172.16.101.5/24")
