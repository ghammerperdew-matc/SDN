#!/usr/bin/env python3

"""
Author: Gavin Hammer-Perdew
Date created: 11-20-2023

Purpose: print an interface name, type, IP address, and netmask from an ordered dictionary
"""

from collections import OrderedDict

interface = OrderedDict([('name', 'GigabitEthernet1'),
                         ('description', 'to port6.sandbox-backend'),
                         ('type',OrderedDict([
                             ('@xmlns:ianaift', 'urn:ietf:params:xml:ns:yang:iana-if-type'),
                             ('#text', 'ianaift:ethernetCsmacd')
                             ])
                          ),
                         ('enabled', 'true'),
                         ('ipv4', OrderedDict([
                             ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip'),
                             ('address', OrderedDict([
                                 ('ip', '10.10.20.175'),
                                 ('netmask', '255.255.255.0')
                                 ])
                              )]
                                              )
                          ),
                         ('ipv6', OrderedDict([
                             ('@xmlns', 'urn:ietf:params:xml:ns:yang:ietf-ip')]
                                              )
                          )
                         ])

print(f"{'Interface Name':19}" + f"{'Interface Type':17}" + f"{'IP Address':15}" + 'Subnet Mask')
print("-"*70)
print(
      f"{interface['name']:19}" +
      f"{interface['type']['#text'][8:]:17}" +
      f"{interface['ipv4']['address']['ip']:15}" +
      interface['ipv4']['address']['netmask']
      )

