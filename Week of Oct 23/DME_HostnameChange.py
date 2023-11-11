#!/usr/bin/env

"""
Date created: 11-7-2023
Created by Ryan Jacob, Abdullah Altameemi, Solomon, and Gavin Hammer-Perdew

Purpose: this script utilizes several functions to validate user-defined IP addresses and hostnames.
It then generates a new cookie for that device's IP address for authentication
and configures the device's hostname to the user's specifications, so long as it's a valid name (read: does not have spaces).

We used an internet search to find a new method of checking if names have spaces and settled on using Method #2
(Using 'in' operator) found on this site: https://www.geeksforgeeks.org/python-check-for-spaces-in-string
"""

import requests
import json
import urllib3

#suppress certificate warning
urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)


#receives an IP address
#makes call to the device at taht IP for a session cookie
#returns the cookie
def getCookie(address) :
    #Get Session Cookie
    url = "https://"+ address +"/api/aaaLogin.json"

    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]


#receives an IP address
#checks validity of address
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


#receives hostname
#ensures there are no spaces in the hostname
#returns True or False
def check_hostname(hostname):

    valid_name = True #set valid_name flag to True by default
    
    #if there are spaces in the name set to False
    if " " in hostname:
        valid_name = False

    #Returns valid_name flag
    return valid_name


#receives device IP address, new hostname for the device and a cookie for API connection
#sends API request to change the hostname
#returns response from the device
def configure_hostname(IP_addr, hostname, cookie):

    #URI to device
    url = "https://"+ IP_addr +"/api/mo/sys.json"

    #API payload
    payload = {
      "topSystem": {
        "attributes": {
          "name": hostname
        }
      }
    }

    #attach cookie to header
    headers = {
      'Content-Type': 'application/json',
      'Cookie': 'APIC-cookie=' + cookie
    }

    #send API post request
    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload))

    return response


#receives nothing
#asks user for input within while loops (with quit option)
#input includes the device address, and a new hostname for the device
#uses user input to change the hostname on the specified device
#returns nothing
def main():

    _quit_ = "n"

    while _quit_ != "y": #while the _quit_ flag is not "y", run
        valid_address = False
        while valid_address == False: #does not break until a valid address is given
            addr = input("Please enter the IP address of the device you wish to configure\n> ")

            if addr.lower() == "q":
                _quit_ = "y"
                valid_address = True

            if _quit_ != "y":
                if check_address(addr) == False:
                    print("Invalid address - try again or enter 'Q' to quit.")
                else:
                    valid_address = True
                    print("\n")

        if _quit_ != "y": #nested loop to allow hostname validation
            valid_hostname = False
            while valid_hostname == False: #does not break until a valid hostname is given
                name = input("Please enter a new hostname for the device\n> ")

                if name.lower() == "q":
                    _quit_ = "y"
                    valid_hostname = True

                if _quit_ != "y":
                    if check_hostname(name) == False:
                        print("Invalid hostname - try again or enter 'Q' to quit.")
                    else:
                        valid_hostname = True
                        print("\n")

        if _quit_ != "y": #runs all functions, notify's user of hostname change, then exits
            my_cookie = getCookie(addr)
            configure_hostname(addr, name, my_cookie)
            print("Hostname configured. Exiting...\n")
            break

    return(None)

        
##MAIN##
main()
