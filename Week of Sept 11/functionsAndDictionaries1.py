#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-12-2023

Purpose: display a list of NTP servers and their addresses contained in a dictionary
"""

#prints keys and the associated values in two columns
def print_dict(dictionary):
    for key, value in dictionary.items():
        print(key, "\t", value)
    return(None)


#prepares a list of ping statements for the addresses in the NTP server dictionary
def ping_prep(IP_list):
    addr_list = []
    for address in IP_list.values():
        addr_list.append(address)
    for x in range(len(addr_list)):
        addr_list[x] = "Ping " + addr_list[x]
    return addr_list


#prints the list of ping statements, each on its own line
def print_pings(ping_list):
    for list_item in ping_list:
        print(list_item)


#main method, returns nothing
def main():
    print("Server Name", "\t", "Address")
    print_dict(ntpServers)
    print("\n")
    pings = ping_prep(ntpServers)
    print_pings(pings)
    return(None)


#dictionary of NTP servers and their addresses
ntpServers = {
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.191.6"
    }


main()
