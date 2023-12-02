def increment_CIDR_address(CIDR_address, octet, offset):

    if octet <= 4 and octet > 0:
        octet = octet-1

        IP_address = CIDR_address.split("/")

        IP_address[0] = IP_address[0].split(".")

        if (int(IP_address[0][octet]) + offset) < 0 or (int(IP_address[0][octet]) + offset) > 255:
            new_IP_address = "-2"
        else:
            IP_address[0][octet] = str(int(IP_address[0][octet]) + offset)
            IP_address[0] = ".".join(IP_address[0])
            new_IP_address = "/".join(IP_address)
        
    else:
        new_IP_address = "-1"

    return new_IP_address


cidr_IP_address = "192.168.1.1/24"
octet = 4
offset = 1

mod_address = increment_CIDR_address
(cidr_IP_address, octet, offset)
print(mod_address)
