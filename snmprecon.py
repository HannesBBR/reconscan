#!/usr/bin/env python
import subprocess
import sys

if len(sys.argv) != 3:
    print "Usage: snmprecon.py <ip address> <output folder>"
    sys.exit(0)

snmpdetect = 0
ip_address = sys.argv[1]
folder = sys.argv[2]

ONESIXONESCAN = "onesixtyone %s" % (ip_address)
results = subprocess.check_output(ONESIXONESCAN, shell=True).strip()

if results != "":
    if "Windows" in results:
        results = results.split("Software: ")[1]
        snmpdetect = 1
    elif "Linux" in results:
        results = results.split("[public] ")[1]
        snmpdetect = 1
    if snmpdetect == 1:
        print "[*] SNMP running on " + ip_address + "; OS Detect: " + results
        SNMPWALK = "snmpwalk -c public -v1 %s 1 > {folder}{ip_address}_snmpwalk.txt".format(ip_address = ip_address, folder = folder)
        results = subprocess.check_output(SNMPWALK, shell=True)

NMAPSCAN = "nmap -vv -sV -sU -Pn -p 161,162 --script=snmp-netstat,snmp-processes %s" % (ip_address)
results = subprocess.check_output(NMAPSCAN, shell=True)
resultsfile = folder + ip_address + "_snmprecon.txt"
f = open(resultsfile, "w")
f.write(results)
f.close

