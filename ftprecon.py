#!/usr/bin/env python
import subprocess
import sys
import os

if len(sys.argv) != 4:
    print "Usage: ftprecon.py <ip address> <port> <output folder>"
    sys.exit(0)

ip_address = sys.argv[1].strip()
port = sys.argv[2].strip()
folder = sys.argv[3]
print "INFO: Performing nmap FTP script scan for " + ip_address + ":" + port
FTPSCAN = "nmap -sV -Pn -vv -p {port} --script=ftp-anon,ftp-bounce,ftp-libopie,ftp-proftpd-backdoor,ftp-vsftpd-backdoor,ftp-vuln-cve2010-4221 -oN '{folder}{ip_address}_ftp.nmap' {ip_address}".format(port = port, ip_address = ip_address, folder = folder)
results = subprocess.check_output(FTPSCAN, shell=True)
outfile = folder + ip_address + "_ftprecon.txt"
f = open(outfile, "w")
f.write(results)
f.close

print "INFO: Performing hydra ftp scan against " + ip_address 
HYDRA = "hydra -L wordlists/userlist -P wordlists/offsecpass -f -o {folder}{ip_address}_ftphydra.txt -u {ip_address} -s {port} ftp".format(ip_address = ip_address, port = port, folder = folder)
results = subprocess.check_output(HYDRA, shell=True)
resultarr = results.split("\n")
for result in resultarr:
    if "login:" in result:
		print "[*] Valid ftp credentials found: " + result 
