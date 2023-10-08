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


#receives and IP address
#adds two to the value of the third octet (ex: 192.168.1.1 --> 192.168.3.1)
#returns modified address
def add_two(IP_address):

    IP_address = IP_address.split(".")
    
    IP_address[2] = str(int(IP_address[2]) + 2)

    new_IP_address = ".".join(IP_address)

    return new_IP_address


#receives nothing and returns nothing
#asks user to input address
def main():

    address = input("Please enter valid IP address: ")

    if check_address(address) == False:
        print("That is an invalid IP address, and this is why we can't have nice things.")
    else:
        address = add_two(address)
        print("The modified address is:", address)

    return None


main()
