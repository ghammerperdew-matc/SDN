#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-5-2023

This script contains a dictionary of information from a Cisco router.
The purpose is to display the information contained in the dictionary in a list format that is easy to read.
"""

#dictionary of router information
router1 = {
    "brand": "Cisco",
    "model": "2901",
    "mgmtIP": "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.1.3.1 /24",
    "hostname": "r1"
    }

#Loop through the tuples generated by .items() and assign them to the tuple of variables (key, value)
for key, value in router1.items():

    #Print the tuples as a two-column list of keys on one side and values on the other
    #"Key" and "Value" provided for clarity when reading
    print("Key = " + key + "\t" + "Value = " + value)
