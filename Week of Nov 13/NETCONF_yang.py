#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-15-2023

Purpose: print the keys and values of an ordered dictionary in the following format:
(each pair on their own line)

Key = (key)   Value = (value)
"""


from collections import OrderedDict


#receives an ordered dictionary
#lists the key/value pairs
#returns nothing
def list_keys_values(ordered_dict):

    #.items() returns a list of tuples
    #so two variables can be used to represent the key and value in the tuple
    for key, value in ordered_dict.items():
        print("Key = " + f"{key:10}", "Value = " + value)

    return None


#receives nothing
#create ordered dict, print key/value pairs using "list_keys_values" function
#returns nothing
def main():
    
    router1 = OrderedDict([
        ("brand", "Cisco"),
        ("model", "1941"),
        ("mgmtIP", "10.0.0.1"),
        ("G0/0", "10.0.1.1"),
        ("G0/1", "10.0.2.1"),
        ("G0/2", "10.1.0.1")
        ])

    list_keys_values(router1)

    return None


main()
