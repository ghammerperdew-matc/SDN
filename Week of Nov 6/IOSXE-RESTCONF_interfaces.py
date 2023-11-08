import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def get_int_rest(device_IP):
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

    mod_intf_list = []

    for intf in intf_list:
        if len(intf['ietf-ip:ipv4']) != 0:
            mod_intf_list.append({'name':intf['name'], 'IP_addr':intf['ietf-ip:ipv4']['address'][0]['ip']})

    return(mod_intf_list)


def get_int_rest_MAC(device_IP):
    url = "https://" + device_IP + ":443/restconf/data/interfaces-state"

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
    intf_list = response["ietf-interfaces:interfaces-state"]["interface"]

    mod_intf_list = []

    for intf in intf_list:
            mod_intf_list.append({'name':intf['name'], 'MAC_addr':intf['phys-address']})

    return(mod_intf_list)


def combine_int_lists(int_IP_list, int_MAC_list):

    combined_list = []

    for intf in int_IP_list:

        name = intf["name"]
        address = intf["IP_addr"]

        for int_MAC in int_MAC_list:

            if name == int_MAC["name"]:
                MAC_address = int_MAC["MAC_addr"]
                combined_list.append({"name": name, "IP_addr": address, "MAC_addr": MAC_address})

    return(combined_list)


def print_combined_list(combined_list):

    print(f"{'Interface':21}", f"{'IP Address':15}", "MAC Address")
    print("-"*49)

    for intf in combined_list:

        print(f"{intf['name']:21}", f"{intf['IP_addr']:15}", intf['MAC_addr'])


def main():

    device_IP = "10.10.20.48"

    intf_list = get_int_rest(device_IP)

    intf_state_list = get_int_rest_MAC(device_IP)

    combined_list = combine_int_lists(intf_list, intf_state_list)

    print_combined_list(combined_list)


main()