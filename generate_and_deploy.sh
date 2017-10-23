#!/bin/bash

error=0

echo -n "Will download zone config from Infoblox. Enter to continue."
read

### Download authoritative zones
 echo "Generating authoritative zone config"
 python infoblox_authoritative.py 2>/dev/null
 test $? -eq 0 || { error=1; }

### Download forward zones
 echo "Generating forward zone config"
 python infoblox_forward.py 2>/dev/null
 test $? -eq 0 || { error=1; }

### Verify syntax of authoritative zones
 echo "Verifying named.authoritative.zones "
 named-checkconf named.authoritative.zones
 test $? -eq 0 || { error=1; } 

### Verify syntax of forward zones
 echo "Verifying named.forward.zones "
 named-checkconf named.forward.zones
 test $? -eq 0 || { error=1; } 

### Verify syntax of named.conf
 echo "Verifying named.conf"
 named-checkconf
 test $? -eq 0 || { error=1; } 

### Count number of zones before deploy
 before_auth_count=`cat /etc/named.authoritative.zones | grep ^zone | wc -l`
 before_fwd_count=`cat /etc/named.forward.zones | grep ^zone | wc -l`

### Count number of zones in new files
 after_auth_count=`cat named.authoritative.zones | grep ^zone | wc -l`
 after_fwd_count=`cat named.forward.zones | grep ^zone | wc -l`

echo
echo "Review these numbers before proceeding!"
echo "---"
echo "Auth zones in running config : $before_auth_count"
echo "Fwd zones in running config  : $before_fwd_count"
echo "---"
echo "Auth zones in new config : $after_auth_count"
echo "Fwd zones in new config  : $after_fwd_count"
echo "---"
echo -en "Ctrl+C to abort. Enter to deploy new config." ; read

test $error -eq 0 && {
   echo "Moving zone config to /etc"
   mv -f named.*.zones /etc
   echo "Reloading named config"
   rndc reconfig
} || { echo "Something went wrong." ; }
