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


"""
This function shouldn't be used when checking user input in loops because it will just break the loops.
It is best to use this one in scripts where function parameters are statically written or
are taken from API responses (to double-check proper communication/handling of API calls/responses)
"""
#receives an IP address
#validates the IP address
#raises exceptions/errors (with explanations) if the address is invalid
#returns True or False
def validate_address(IP_address):
    
    IP_address = IP_address.split(".")

    if len(IP_address) != 4:
        raise Exception("Invalid number of octets -- IP address should have 4 octets")

    for octet_value in IP_address:
        if octet_value.isdigit() != True:
            raise ValueError("Invalid octet integer value -- IP address must not contain letters, empty space or be a null value")
        if int(octet_value) < 0 or int(octet_value) > 255:
            raise ValueError("Invalid octet value -- each octet must be an integer value in range of 0-255")
        
    valid_address = True

    return valid_address



sketchy_address = "192.168.1.1"
validity = validate_address(sketchy_address)
print(validity)
