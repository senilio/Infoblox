#!/usr/bin/env python

# Script to export all authoritative zones from Infoblox, and
# output a bind9 readable configuration file.

from __future__ import print_function
from pyinfoblox import InfobloxWAPI
from IPy import IP
import requests
requests.packages.urllib3.disable_warnings()

master = '192.168.25.10'
file = 'named.authoritative.zones'

ib = InfobloxWAPI(
    username = "",
    password = "",
    wapi = "https://infoblox/wapi/v1.7/"
)

zones = ib.zone_auth.get()
f = open(file, 'w')

for i in zones:
    if i['view'] == 'Default':
        # Decide zone name
        try:
            zone = str(IP(i['fqdn']).reverseNames()[0])[:-1]
        except ValueError, AttributeError:
            zone = str(i['fqdn'])

        # Decide file name
        try:
            zonefile = str(IP(i['fqdn']).reverseNames()[0])[:-1]
        except ValueError, AttributeError:
            zonefile = str(i['fqdn'])

        # Write config to disk
        f.write ("zone \"%s\" IN {\n" % zone)
        f.write ("\ttype slave;\n")
        f.write ("\tfile \"data/%s.zone\";\n" % zonefile)
        f.write ("\tmasters { %s; };\n" % master )
        f.write ("};\n\n")

f.close()
