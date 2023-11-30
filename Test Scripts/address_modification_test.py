"""
Old function
"""
###receives an IP address, octet to modify (1-4) and offset (how much to change it by)
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


"""
New function
"""
###receives an IP address (string), octet number (int), method of changing octet value (string), value to set or increment octet value
###change methods --> "set" or "increment"
###validates all parameters and raises an exception/error (with explanation) if any parameter is invalid
###modifies the specified octet of an IP address using the specified method and value
def modify_IPv4(IP_address, octet, change_method, change_value):

    IP_address = IP_address.split(".")

    for octet_value in IP_address:
        if octet_value.isdigit() != True:
            raise ValueError("Invalid octet integer value -- IP address must not contain letters, empty space or be a null value")
        if int(octet_value) < 0 or int(octet_value) > 255:
            raise ValueError("Invalid octet value -- each octet must be an integer value in range of 0-255")

    if len(IP_address) != 4:
        raise Exception("Invalid number of octets -- IP address should have 4 octets")

    if int(octet) > 4 or int(octet) < 1:
        raise ValueError("Invalid octet range -- use octet values 1-4 (1.2.3.4)")

    octet = octet-1
    
    if change_method != "set" and change_method != "increment":
        raise ValueError("Invalid string value -- change_method parameter must be a string and must be either 'set' or 'increment'")

    if change_method == "set_to":
        if change_value < 0 or change_value > 255:
            raise ValueError("Invalid octet value range -- change_value must be a value from 0-255 when using 'set' for change_method parameter")

        IP_address[octet] = str(change_value)
        new_IP_address = ".".join(IP_address)
    
    else:
        if (int(IP_address[octet]) + change_value) < 0 or (int(IP_address[octet]) + change_value) > 255:
            raise ValueError("Invalid increment value: change_value must not cause the octet to be incremented outside of values 0-255")
        
        IP_address[octet] = str(int(IP_address[octet]) + change_value)
        new_IP_address = ".".join(IP_address)
        
    return new_IP_address



address = "192.168.1.25"
new_address = modify_IPv4(address, 4, "increment", 10)
print(new_address)
