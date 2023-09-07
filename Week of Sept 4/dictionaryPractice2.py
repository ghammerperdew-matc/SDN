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
        print(f"{key:13}", end="")

    print("\n" + "-" * 86)
    
    for value in dictionary.values():
        output = value.split()
        print(f"{output[0]:13}", end="")

    return(None)


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
                        print("Invalid input. Enter the address in the format of x.x.x.x where x is an integer from 0-255.")
                        break
                
                #if ther are letters, prompt to re-enter address
                else:
                    status = False
                    print("Invalid input. Enter the address in the format of x.x.x.x where x is an integer from 0-255.")
                    break
                
            return(status)


def main():
    #print dictionary content (formatted for readability)
    print_router(router1)

    #begin main loop
    while(True):

        #prompt to change mgmtIP address or quit
        print("\nWould you like to change the mgmtIP address?")
        userInput = str(input("Enter Y or N: "))

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

quit()
