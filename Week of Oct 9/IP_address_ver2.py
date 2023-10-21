#!/usr/bin/env/python 3

#receives an IP address
#validates the IP address
#returns True or False
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


###receives and IP address, octet to modify (1-4) and offset (how much to change it by)
###checks validity of octet number and offset
###if both valid, adds the specified amount to the value of specified octet (ex: 192.168.1.1 --> 192.168.3.1)
###returns modified address or "-1" for invalid octet anbd "-2" for invalid offset
def add_val(IP_address, octet, offset):

    if octet <= 4 and octet > 0:
        octet = octet-1

        IP_address = IP_address.split(".")

        if (int(IP_address[octet]) + offset) < 0 or (int(IP_address[octet]) + offset) > 255:
            new_IP_address = "-2"
        else:
            IP_address[octet] = str(int(IP_address[octet]) + offset)
            new_IP_address = ".".join(IP_address)
        
    else:
        new_IP_address = "-1"

    return new_IP_address


#receives nothing and returns nothing
#asks user to input address, octet and offset
def main():
    address = input("Please enter valid IP address: ")
    octet = int(input("Please specify which octet of the address should be offset (integer 1-4): "))
    offset = int(input("Please specify by what value each device should be offset: "))

    if check_address(address) == False:
        print("That is an invalid IP address, and this is why we can't have nice things.")
    else:
        address = add_val(address, octet, offset)
        if address != "-1" and address != "-2":
                print("Updated address is: ", address)
        elif address == "-1":
                print("Error: invalid octet range")
        else:
                print("Error: invalid offset -- new octet value would be out of range")
                        
    return None


main()
