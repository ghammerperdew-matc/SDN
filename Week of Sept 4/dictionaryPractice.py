#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-5-2023

This script contains a dictionary of information from a Cisco router.
The purpose is to modify and then display the information as a list of keys, values and then items.
"""

#dictionary of values from a router
router1 = {
    "brand": "Cisco",
    "model": "1941",
    "mgmtIP": "10.0.0.1",
    "G0/0": "10.0.1.1 /24",
    "G0/1": "10.0.2.1 /24",
    "G0/2": "10.0.3.1 /24",
    "hostname": "r1"
    }

#modifies values of two dictionary keys
router1["G0/2"] = "10.1.3.1"
router1["model"] = "2901"

#print the list of keys, their values (again as a list),
#and then the items (keys and values as a list of tuples)
print(router1.keys())
print(router1.values())
print(router1.items())
