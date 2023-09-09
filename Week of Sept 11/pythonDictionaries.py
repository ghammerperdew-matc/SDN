#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-8-2023

Purpose: display the contents of nested dictionaries
"""

router1 = {
    "hostname": "R1",
    "brand": "Cisco",
    "mgmtIP": "10.0.0.1",
    "interfaces": {"G0/0": "10.1.1.1", "G0/1": "10.1.2.1"}
    }

#print keys of router1
print(router1.keys())

#print keys of interfaces (dict within router1)
print(router1["interfaces"].keys())

#print values of router1
print(router1.values())

#print values of interfaces (dict within router1)
print(router1["interfaces"].values())

#print router1 items (as tuples)
print(router1.items())

#print interfaces items (as tuples)
print(router1["interfaces"].items())
