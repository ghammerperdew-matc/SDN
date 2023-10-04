import requests
import json
import urllib3

urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


def get_OSPF_neighbors(mgmt_IP_address):
    
    switchuser='cisco'
    switchpassword='cisco'

    url='https://' + mgmt_IP_address + '/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
        "cmd": "show ip ospf neighbor",
        "version": 1
        },
        "id": 1
      }
    ]

    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()

    return(response)


def print_OSPF_neighbors(OSPF_neighbor_dict):

    neighbor_table_list = OSPF_neighbor_dict["result"]["body"]["TABLE_ctx"]["ROW_ctx"]["TABLE_nbr"]["ROW_nbr"]

    print(f"{'Router-ID':15}", f"{'Neighbor IP':15}", "Int\n" + "-"*38)
    
    for neighbor in neighbor_table_list:
        print(f"{neighbor['rid']:15}", f"{neighbor['addr']:15}", neighbor['intf'])

    return None


def main():
    devices = [
        {
        "hostname": "dist-sw01",
        "deviceType": "switch",
        "mgmtIP": "10.10.20.177"
        },
        {
        "hostname": "dist-sw02",
        "deviceType": "switch",
        "mgmtIP": "10.10.20.178"
            }
        ]

    for device in devices:

        mgmtIP = device["mgmtIP"]

        print(device["hostname"], "OSPF Neighbors\n" + "-"*38)
        
        OSPF_neighbors = get_OSPF_neighbors(mgmtIP)
        print_OSPF_neighbors(OSPF_neighbors)

        print("\n")

    return None


#execute main function
main()
