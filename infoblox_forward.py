#!/usr/bin/env python

# Script to export all forward zones from Infoblox, and
# output a bind9 readable configuration file.

from __future__ import print_function
from pyinfoblox import InfobloxWAPI
from IPy import IP
import requests
requests.packages.urllib3.disable_warnings()

file = 'named.forward.zones'
f = open(file, 'w')

ib = InfobloxWAPI(
    username = "",
    password = "",
    wapi = "https://infoblox/wapi/v1.7/"
)

zones = ib.zone_forward.get()

for i in zones:
    # Init list of forwarders
    forwarders = []

    # Get all forwarders for current zone
    for j in i['forward_to']:
        forwarders.append(j['address'])

    # Set zone name depending on forward or reverse zone
    try:
        zone = str(IP(i['fqdn']).reverseNames()[0])[:-1]
    except ValueError, AttributeError:
        zone = str(i['fqdn'])

    # Write zone to file
    f.write("zone \"%s\" IN {\n" % zone)
    f.write ("\ttype forward;\n")
    f.write ("\tforwarders {%s;};\n" % '; '.join(forwarders))
    f.write ("};\n\n")

f.close()
