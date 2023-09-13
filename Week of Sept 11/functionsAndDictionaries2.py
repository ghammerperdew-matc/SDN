#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-12-2023

Purpose: display a dictionary of device information and add devices and their attributes to the dictionary when prompted
"""

#Receives a dictionary of devices and prepends ping to the mgmtIP address of each device
#Prints that prepended address and returns nothing
def ping_prep(device_dict):  
    for device in device_dict:
        print("ping", device_dict[device]["mgmtIP"])
    print("\n")


#Receives a dictionary of devices and prints the device and its attributes
#returns None
def print_devices(device_dict):
    for device in device_dict.keys():
        print(device)
        for key, value in device_dict[device].items():
            print("\t", f"{key:10}", value)
        print("\n")

    return(None)


#verifies that inputs for values aside from IP addresses are alphanumeric and not null/
#return False if input is null or is not alphanumeric, otherwise return True
def check_null(value): 
    if value.isalnum() == False:
        valid_input = False
    else:
        valid_input = True
        
    return valid_input


#verifies that IP addresses are valid (not accounting for subnet masks)
def check_IP(IP_address):
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
    return(status) 


#Receives nothing, gets information from user regarding new device, returns device info as a dictionary
def get_device():   

    not_null = False
    #loop until condition is met (input is validated)
    while not_null == False:
        
        #Prompt user to enter a hostname
        hostname = input("Enter a valid device hostname: ")

        #verify hostname is not null and is alphanumeric
        not_null = check_null(hostname)
        
        #restart loop if input is not valid
        if not_null == False:
            print("Hostname cannot be null and must be alphanumeric - try again\n")

    
    not_null = False
    #loop until condition is met (input is validated)
    while not_null == False:

        #Prompt user to enter a device type
        dtype = input("Enter a valid device type: ")
        
        #verify type is not null and is alphanumeric
        not_null = check_null(dtype)

        #restart loop if input is not valid
        if not_null == False:
            print("Type cannot be null and must be alphanumeric - try again\n")

    
    not_null = False
    #loop until condition is met (input is validated)
    while not_null == False:

        #Prompt user to enter a device brand
        brand = input("Enter a valid device brand: ")
        
        #verify brand is not null and is alphanumeric
        not_null = check_null(brand)

        #restart loop if input is not valid
        if not_null == False:
            print("Brand cannot be null and must be alphanumeric - try again\n")

    
    valid_IP = False

    while valid_IP == False:

        #Prompt user to enter a valid IP address
        mgmtIP = input("Enter a valid IP address: ")
        
        #verify IP is not null and is valid
        valid_IP = check_IP(mgmtIP)

        #restart loop if input is not valid
        if valid_IP == False:
            print("Invalid input. Enter the address in the format of x.x.x.x where x is an integer from 0-255.\n")


    #build device dictionary
    device = {
        "hostname": hostname,
        "type": dtype,
        "brand": brand,
        "mgmtIP": mgmtIP
        }
    
    #return device dictionary
    return device


#adds new device that has been verified to the current dictionary
def add_new_device(new_device, device_dict):
    new_key = new_device["hostname"]
    devices[new_key] = new_device
    
    
#main function
def main():
    
    ping_prep(devices)

    print_devices(devices)

    add_device = True
    while add_device == True:
        #prompt for adding a new device
        new_device_prompt = input("Would you like to add a new device? Enter Y or N: ")

        if new_device_prompt.lower() == "y":
            #prompt for and validate information of new device
            new_device = get_device()

            #add new device to devices dictionary
            add_new_device(new_device, devices)
            
            #print the new list of devices and their attributes
            print_devices(devices)

        elif new_device_prompt.lower() == "n":
            #if user denies the prompt, break the loop
            add_device = False

        else:
            #restart loop if input
            print("Invalid input -- enter Y or N\n")

        
        
#dictionary of devices with nested dictionaries of device attributes
devices = {
    "R1": {
        "hostname": "R1",
        "type": "router",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.1"
        },
    "R2": {
        "hostname": "R2",
        "type": "router",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.2"
        },
    "S1": {
        "hostname": "S1",
        "type": "switch",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.3"
        },
    "S2": {
        "hostname": "S2",
        "type": "switch",
        "brand": "Cisco",
        "mgmtIP": "10.0.0.4"
        }
}

main()
