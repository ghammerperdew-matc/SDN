#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-5-2023

This script contains a dictionary of information from a Cisco router.
The purpose is to display the information contained in the dictionary in a list format,
and then ask the user if they would like to change the management IP address (mgmtIP).
If the user enters a valid address, it is changed in the dictionary.
This process loops until broken by the user.
"""

#dictionary of router info
router1 = {
    "brand": "Cisco",
    "model": "2901",
    "mgmtIP": "10.0.0.1", 
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.1.3.1 /24",
    "hostname": "r1"
    }


#function for printing the router dictionary in a specific format, returns None
#prints keys and their values on separate lines with a dotted line between
def print_router(dictionary):
    #print keys on first line
    for key in dictionary.keys():
        print(f"{key:20}", end="")

    #print dotted line
    print("\n" + "-" * 128)

    #print values on second line
    for value in dictionary.values():

        #some of the IP addresses are in CIDR notation
        #need to split the subnet masks from the addresses
        output = value.split()

        #prints only first item in list generate by .values()
        #thus not printing subnet mask
        print(f"{output[0]:20}", end="")

    return(None)


#function for validating the IP address, returns True or False
def check_address(IP_address):
        #split IP address into individual octets -- returns a list
        address = IP_address.split(".")

        #validate number of octets in the list
        if len(address) == 4:
                
            #validate each octet
            for listItem in address:
                    
                #check if there are letters in the octet
                if listItem.isdigit():
                        
                    #if no letters, convert to integer and continue
                    listItem = int(listItem)
                        
                    #check if integer range is valid
                    if listItem >= 0 and listItem <= 255:
                            
                        #variable for boolean decision later
                        status = True
                            
                    #if range is invalid, set status and prompt to re-enter address
                    else:
                        status = False
                        break
                
                #if there are letters, prompt to re-enter address
                else:
                    status = False
                    break
                
            #return the value of the status variable for the function
            return(status)


#main function, returns None
def main():
    #print dictionary content (formatted for readability)
    print_router(router1)

    #begin main loop
    while(True):

        #prompt to change mgmtIP address or quit
        print("\nWould you like to change the mgmtIP address?")
        userInput = str(input("Enter Y or N: "))

        #check user input
        if userInput.lower() == "y":
            while(True):
                #enter address
                newAddress = input("Enter a valid IPv4 address without a subnet mask or N to cancel: ")

                #check escape (cancel) value
                if newAddress.lower() == "n":
                    break

                #ensure address is within valid parameters, change the address in the dictionary and display the new dictionary
                if check_address(newAddress):
                    router1["mgmtIP"] = newAddress
                    print_router(router1)
                    break

                else:
                    #if not valid, display the requirements for a valid address
                    print("Invalid input. Enter the address in the format of x.x.x.x where x is an integer from 0-255.")


        elif userInput.lower() == "n":
            #break loop
            break

        else:
            print("Invalid input - try again.")

    return(None)


#Call main function
main()

#Once main loop is broken, main() returns None, and the script closes with quit()
quit()
