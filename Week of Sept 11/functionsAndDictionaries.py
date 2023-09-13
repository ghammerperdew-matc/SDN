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

#main method, returns nothing
def main():
    print("Server Name", "\t", "Address")
    print_dict(ntpServers)
    return(None)

#dictionary of NTP servers and their addresses
ntpServers = {
    "Server1": "221.100.250.75",
    "Server2": "201.0.113.22",
    "Server3": "58.23.191.6"
    }


main()
