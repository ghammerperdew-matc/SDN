import requests
import json
import urllib3

#This line keeps the certificate warning from appearing in the output when the script is run
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


#receives an IP address
#validates the IP address
#returns True or False
"""
This is also used to check that the subnet mask meets the same basic requirements.
I know this is not the correct way, but we also don't need it to be right now, and this will eventually be updated.
"""
def check_address(IP_address):
        #split IP address into individual octets -- returns a list
        octet_list = IP_address.split(".")

        #assume the address is valid, create variable for "True" status
        #Will be changed to false if any issue is found
        status = True

        #validate number of octets in the list
        if len(octet_list) != 4:

            #set status to false if there are not exactly 4 octets
            status = False
                
        #validate each octet
        for octet in octet_list:
                    
            #check if there are letters in the octet
            if octet.isdigit() == False:

                status = False
                        
            #check if integer range is valid
            elif int(octet) < 0 or int(octet) > 255:
                            
                #change address status to False if invalid range
                status = False
                
        #return the value of the status variable for the function
        return status


#function that receives the list of interfaces contained within the JSON object returned by the API in response to "show ip interface brief"
#and prints the interface name, protocol/link statuses, and the IP address (without the subnet mask)
def print_interfaces(intf_list):

    #print the list header with even spacing
    print(f"{'Name':10}", f"{'Proto':10}", f"{'Link':10}", "Address" )

    #using a for loop to iterate through the list of dictionaries that contain attributes of the interfaces and print them with even spacing
    for intf in intf_list:
        print(f"{intf['intf-name']:10}", f"{intf['proto-state']:10}", f"{intf['link-state']:10}", f"{intf['prefix']:10}")

    print("\n")

    return None


#receives a management IP address for a device
#sends an API request to that device with the "show ip interface brief" command
#returns the dictionary containing the interface interfaces
def show_IP_interface_brief(mgmt_address):

    switchuser='cisco'
    switchpassword='cisco'
    url='https://' + mgmt_address + '/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "show ip interface brief",
          "version": 1
        },
        "id": 1
      }
    ]

    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()

    #ROW_intf is a dictionary key with a value of the dictionary containing the interface information
    interfaces = response["result"]["body"]["TABLE_intf"]["ROW_intf"]

    return interfaces


#receives an interface input from a user and a dictionary of interfaces for a given device
#compares the interface from user input with the interfaces in the dictionary to see if it exists on the given device
#returns True or False (exists or not)
def interface_exists(user_input_interface, intf_list):

    exists = False

    for intf in intf_list:
        if intf["intf-name"] == user_input_interface:
            exists = True

    return exists


#receives a management IP address, interface name, new address and subnet mask to be assigned to the received interface
#makes an API call to the device at the recieve management address to change the IP address on the received interface
####this assumes that the management address, interface, new address and subnet mask have been verified####
#returns the response from the device -- if everything worked, it will contain almost nothing, but any errors that occur will be returned otherwise
def change_interface_address(mgmt_address, int_name, new_address, subnet_mask):

    switchuser='cisco'
    switchpassword='cisco'
    url='https://' + mgmt_address + '/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "configure terminal",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "interface " + int_name,
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip address " + new_address + " " + subnet_mask,
          "version": 1
        },
        "id": 3
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "exit",
          "version": 1
        },
        "id": 4
      }
    ]

    response = requests.post(url,data=json.dumps(payload), verify=False, headers=myheaders, auth=(switchuser, switchpassword)).json()
    
    return response


#receives and returns nothing
#gets input from the user and verifies it and prompts them to either quit or enter valid information if they enter invalid info to start with
#sends API calls to a device to change IP address on an interface of a specified device
def main():

    #main while loop break variable
    _quit_ = "n"

    #main while loop
    while _quit_ != "y":

        #break variable for valid_address while loop
        valid_address = False
        while valid_address == False:
            mgmt_address = input("Please enter the management IP address of the device you would like to modify: ")

            if mgmt_address.lower() == "q":
                _quit_= "y" #sets quit variable to the quit value, so when the loop is broken, the main while loop breaks too
                valid_address = True #breaks valid_address loop
                
            #if the quit value is "n", the input address is evaluated
            #if it's "y", valid_address is set to True (again just in case), so that the valid_address loop will break
            #this pattern repeats for each while loop for input
            if _quit_ != "y":
                if check_address(mgmt_address) ==  False:
                    print("Invalid address - try again or enter 'Q' to quit.")
                else:
                    valid_address = True
                    print("\n")
        
        #only continues to next loop if _quit_ is "n" -- this pattern repeats for all input loops
        if _quit_ != "y":
            #gets 'show ip interface brief' output from the device specified by management IP
            int_IP_addrs = show_IP_interface_brief(mgmt_address)
            #prints the list of interfaces with their IP addresses in a readable format
            print_interfaces(int_IP_addrs)

            #break variable for valid_interface while loop
            valid_interface = False
            while valid_interface == False:
                interface = input("Please enter the name of the interface to modify -- ensure it is the same as listed above: ")

                if interface.lower() == "q":
                    _quit_ = "y"
                    valid_interface = True

                if _quit_ != "y":

                    if interface_exists(interface, int_IP_addrs) == False:
                        print("Invalid interface - try again or enter 'Q' to quit.")
                    else:
                        valid_interface = True

        if _quit_ != "y":
            #break variable for valid_address while loop
            valid_new_address = False
            while valid_new_address == False:
                new_address = input("Please enter a new valid IP address for the interface: ")

                if new_address.lower() == "q":
                    _quit_ = "y"
                    valid_new_address = True

                if _quit_ != "y":

                    if check_address(new_address) == False:
                        print("Invalid IP address -- try again or enter 'Q' to quit.")
                    else:
                        valid_new_address = True
                    
        if _quit_ != "y":
            #break variable for valid_subnet while loop
            valid_subnet = False
            while valid_subnet == False:
                subnet_mask = input("Please enter a valid subnet mask (ex: 255.255.255.0): ")

                if subnet_mask.lower() == "q":
                    _quit_ = "y"
                    valid_subnet = True

                if _quit_ != "y":

                    if check_address(subnet_mask) == False:
                        print("Invalid subnet mask -- try again or enter 'Q' to quit.")
                    else:
                        valid_subnet = True
        
        #once all of the necessary input has been gathered, it is used to call the necessary functions
        if _quit_ != "y":
            #makes the request for changin the IP address on the given interface on the given device
            change_interface_address(mgmt_address, interface, new_address, subnet_mask)
            
            #makes a new call to get the interfaces/IP addresses
            int_IP_addrs = show_IP_interface_brief(mgmt_address)
            
            #prints the new list of ints/addresses -- the address of the specified interface should be different now
            print_interfaces(int_IP_addrs)

        return None


main()
