#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 9-8-2023

Purpose: display a specific value of several nested dictionaries
"""

#dictionary of devices with nested dictionaries of device attributes
devices = {
    "R1": {
        "type": "router",
        "hostname": "R1",
        "mgmtIP": "10.0.0.1"
        },
    "R2": {
        "type": "router",
        "hostname": "R2",
        "mgmtIP": "10.0.0.2"
        },
    "S1": {
        "type": "switch",
        "hostname": "S1",
        "mgmtIP": "10.0.0.3"
        },
    "S2": {
        "type": "switch",
        "hostname": "S2",
        "mgmtIP": "10.0.0.4"
        }
}


#iterate through nested dictionaries that represent individual devices
for device in devices.keys():
    #print the management IP address with "ping" behind it
    print("ping", devices[device]["mgmtIP"])
