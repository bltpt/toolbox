#!/usr/bin/env python3

# findcidr.py: StdInString --> StdOutString
# Purpose: to accept an IP address as String, and print its smallest
#          registered CIDR block as a String to StdOut

import sys
import os
import dns.resolver

server = 'origin.asn.cymru.com'

addresses = ['231.12.45.178', '82.23.116.5', '4.237.38.65', '9.12.28.87']

myResolver = dns.resolver.Resolver()

myAnswers = []

for address in addresses:
    octet1, octet2, octet3, octet4 = address.split(".", maxsplit=4)
    addressFlip = octet4 + "." + octet3 + "." + octet2 + "." + octet1
    query = addressFlip+"."+server
    try:
        result = myResolver.query(query, "TXT")
        for answer in result:
            print("%s: %s" % (address, answer))
    except:
        print("%s: no data. Is the address routable?")
