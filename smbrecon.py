#!/usr/bin/python
import sys
import subprocess

if len(sys.argv) != 3:
    print "Usage: smbrecon.py <ip address> <output folder>"
    sys.exit(0)

ip = sys.argv[1]
NBTSCAN = "./samrdump.py %s" % (ip) # TODO: add this script
nbtresults = subprocess.check_output(NBTSCAN, shell=True)
if ("Connection refused" not in nbtresults) and ("Connect error" not in nbtresults) and ("Connection reset" not in nbtresults):
	print "[*] SAMRDUMP User accounts/domains found on " + ip
	lines = nbtresults.split("\n")
	for line in lines:
		if ("Found" in line) or (" . " in line):
			print "   [+] " + line
				

 

