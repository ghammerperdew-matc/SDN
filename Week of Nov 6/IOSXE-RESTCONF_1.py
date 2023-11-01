import requests
import json

def get_Ints(device_IP):
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


def print_Int(intf_list):
    
    for intf in intf_list:

        name = intf["name"]

        if intf["enabled"] == True:
            status = "UP"
        else:
            status = "DOWN"

        if len(intf["ietf-ip:ipv4"]) != 0:
            
            address = intf["ietf-ip:ipv4"]["address"][0]["ip"]
            netmask = intf["ietf-ip:ipv4"]["address"][0]["netmask"]

            print(f"{name:20}", f"{status:8}", f"{address:17}", netmask)

        else:
            print(f"{name:20}", f"{status:8}", f"{'No IP Address':17}", "No Netmask")

    return(None)


def main():

    device_IP = "10.10.20.48"

    intf_list = get_Ints(device_IP)

    print_Int(intf_list)



main()