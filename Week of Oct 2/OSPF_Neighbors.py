#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 10-3-2023

Purpose: iterate through nexted dictionaries of basic device information and print it with formatting
"""

devices = [
    {
    "hostname": "dist-sw01",
    "device_type": "switch",
    "mgmt_IP": "10.10.20.177"
    },
    {
    "hostname": "dist-sw02",
    "device_type": "switch",
    "mgmt_IP": "10.10.20.178"
        }
    ]

print(f"{'Host':13}", f"{'Type':10}", "Mgmt IP\n" + "-"*40)

for device in devices:

        print(f"{device['hostname']:13}", f"{device['device_type']:10}", device["mgmt_IP"])
