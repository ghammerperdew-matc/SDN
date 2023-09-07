router1 = {
    "brand": "Cisco",
    "model": "2901",
    "mgmtIP": "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.1.3.1 /24",
    "hostname": "r1"
    }

def print_router(dictionary):
    for key in dictionary.keys():
        print(f"{key:10}", end="")

    print("\n" + "-" * 70)
    
    for value in dictionary.values():
        output = value.split()
        print(f"{output[0]:10}", end="")

    return(None)

print_router(router1)

while(True):

    print("Would you like to change the mgmtIP address?")
    userInput = str(input("Enter Y or N: "))

    if userInput.lower() is "y":
        while(True):
            #enter address
            newAddress = input("Enter a valid IPv4 address without a subnet mask or N to cancel: ")

            #check escape (cancel) value
            if newAddress.lower() is "n":
                return(False)

            #split IP address into individual octets
            address = newAddress.split(".")

            #validate number of octets
            if len(address) == 4:
                #validate each octet
                while(True):
                    for listItem in address:
                        if listItem.isdigit():

                        else:
                            print("Invalid input. Enter the address in the format of x.x.x.x where x is an integer from 0-255.")
                            return(False)
                            

                        #if int(listItem) >= 0 and int(listItem) <= 255:


                #if address is valid, change the address in the dictionary and display the new dictionary

            else:
                #if not valid, display the requirements for a valid address
                print("Invalid input. Enter the address in the format of x.x.x.x where x is an integer from 0-255.")

        #exits main loop        
        return(False)

    elif userInput.lower() is "n":
        #end script by returning false for while loop
        return(False)

    else:
        print("Invalid input - try again.")
