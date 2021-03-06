#!/usr/bin/env python

###############################################################################################################
## [Title]: reconscan.py -- a recon/enumeration script
## [Author]: Mike Czumak (T_v3rn1x) -- @SecuritySift
##-------------------------------------------------------------------------------------------------------------
## [Details]: 
## This script is intended to be executed remotely against a list of IPs to enumerate discovered services such 
## as smb, smtp, snmp, ftp and other. 
##-------------------------------------------------------------------------------------------------------------
## [Warning]:
## This script comes as-is with no promise of functionality or accuracy.  I strictly wrote it for personal use
## I have no plans to maintain updates, I did not write it to be efficient and in some cases you may find the 
## functions may not produce the desired results so use at your own risk/discretion. I wrote this script to 
## target machines in a lab environment so please only use it against systems for which you have permission!!  
##-------------------------------------------------------------------------------------------------------------   
## [Modification, Distribution, and Attribution]:
## You are free to modify and/or distribute this script as you wish.  I only ask that you maintain original
## author attribution and not attempt to sell it or incorporate it into any commercial offering (as if it's 
## worth anything anyway :)
###############################################################################################################

import subprocess
import multiprocessing
from multiprocessing import Process, Queue
import os
import time 

def multProc(targetin, scanip, port, folder):
	jobs = []
	p = multiprocessing.Process(target=targetin, args=(scanip,port,folder))
	jobs.append(p)
	p.start()
	return


def dnsEnum(ip_address, port, folder):
	print "INFO: Detected DNS on " + ip_address + ":" + port
	if port.strip() == "53":
	   SCRIPT = "./dnsrecon.py %s" % (ip_address, folder)# execute the python script         
	   subprocess.call(SCRIPT, shell=True)
	return

def httpEnum(ip_address, port, folder):
	print "INFO: Detected http on " + ip_address + ":" + port
	print "INFO: Performing nmap web script scan for " + ip_address + ":" + port    
	HTTPSCAN = "nmap -sV -Pn -vv -p {port} --script=http-vhosts,http-userdir-enum,http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-email-harvest,http-methods,http-method-tamper,http-passwd,http-robots.txt -oN {folder}{ip_address}_http.nmap {ip_address}".format(port = port, folder = folder, ip_address = ip_address)
	results = subprocess.check_output(HTTPSCAN, shell=True)
	DIRBUST = "./dirbust.py http://%s:%s %s" % (ip_address, port, ip_address) # execute the python script
	subprocess.call(DIRBUST, shell=True)
	#NIKTOSCAN = "nikto -host %s -p %s > %s._nikto" % (ip_address, port, ip_address)
	return

def httpsEnum(ip_address, port, folder):
	print "INFO: Detected https on " + ip_address + ":" + port
	print "INFO: Performing nmap web script scan for " + ip_address + ":" + port    
	HTTPSCANS = "nmap -sV -Pn -vv -p %s --script=http-vhosts,http-userdir-enum,http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-email-harvest,http-methods,http-method-tamper,http-passwd,http-robots.txt -oN {folder}{ip_address}_https.nmap {ip_address}".format(folder = folder, port = port, ip_address = ip_address)
	results = subprocess.check_output(HTTPSCANS, shell=True)
	DIRBUST = "./dirbust.py https://%s:%s %s" % (ip_address, port, ip_address) # execute the python script
	subprocess.call(DIRBUST, shell=True)
	#NIKTOSCAN = "nikto -host %s -p %s > %s._nikto" % (ip_address, port, ip_address)
	return

def mssqlEnum(ip_address, port, folder):
	print "INFO: Detected MS-SQL on " + ip_address + ":" + port
	print "INFO: Performing nmap mssql script scan for " + ip_address + ":" + port    
	MSSQLSCAN = "nmap -vv -sV -Pn -p {port} --script=ms-sql-info,ms-sql-config,ms-sql-dump-hashes --script-args=mssql.instance-port=1433,smsql.username-sa,mssql.password-sa -oX {folder}{ip_address}_mssql.xml %s".format(port = port, ip_address = ip_address, folder = folder)
	results = subprocess.check_output(MSSQLSCAN, shell=True)

def sshEnum(ip_address, port, folder):
	print "INFO: Detected SSH on " + ip_address + ":" + port
	SCRIPT = "./sshrecon.py %s %s" % (ip_address, port, folder)
	subprocess.call(SCRIPT, shell=True)
	return

def snmpEnum(ip_address, port, folder):
	print "INFO: Detected snmp on " + ip_address + ":" + port
	SCRIPT = "./snmprecon.py %s" % (ip_address, folder)         
	subprocess.call(SCRIPT, shell=True)
	return

def smtpEnum(ip_address, port, folder):
	print "INFO: Detected smtp on " + ip_address + ":" + port
	if port.strip() == "25":
	   SCRIPT = "./smtprecon.py %s" % (ip_address, folder)       
	   subprocess.call(SCRIPT, shell=True)
	else:
	   print "WARNING: SMTP detected on non-standard port, smtprecon skipped (must run manually)" 
	return

def smbEnum(ip_address, port, folder):
	print "INFO: Detected SMB on " + ip_address + ":" + port
	if port.strip() == "445":
	   SCRIPT = "./smbrecon.py %s 2>/dev/null" % (ip_address, folder)
	   subprocess.call(SCRIPT, shell=True)
	return

def ftpEnum(ip_address, port, folder):
	print "INFO: Detected ftp on " + ip_address + ":" + port
	SCRIPT = "./ftprecon.py %s %s" % (ip_address, port, folder)       
	subprocess.call(SCRIPT, shell=True)
	return

def nmapScan(ip_address):

	ip_address = ip_address.strip()

	# create results folder
	folder = './recon_enum/%s/' % (ip_address)
	create_dir(folder)

	print "INFO: Running general TCP/UDP nmap scans for " + ip_address
	serv_dict = {}
	TCPSCAN = "nmap -vv -Pn -A -sC -sS -T 4 -p- -oN '{folder}{ip_address}.nmap' -oX '{folder}{ip_address}_nmap_scan_import.xml' {ip_address}" .format(folder = folder, ip_address = ip_address)
	UDPSCAN = "nmap -vv -Pn -A -sC -sU -T 4 --top-ports 200 -oN '{folder}{ip_address}U.nmap' -oX '{folder}{ip_address}U_nmap_scan_import.xml' {ip_address}".format(folder = folder, ip_address = ip_address)
	results = subprocess.check_output(TCPSCAN, shell=True)
	udpresults = subprocess.check_output(UDPSCAN, shell=True)
	lines = results.split("\n")
	for line in lines:
		ports = []
		line = line.strip()
		if ("tcp" in line) and ("open" in line) and not ("Discovered" in line):
			while "  " in line: 
				line = line.replace("  ", " ");
			linesplit= line.split(" ")
			service = linesplit[2] # grab the service name
	 		port = line.split(" ")[0] # grab the port/proto
			if service in serv_dict:
				ports = serv_dict[service] # if the service is already in the dict, grab the port list
	 		ports.append(port) 
	 		serv_dict[service] = ports # add service to the dictionary along with the associated port(2)

	# go through the service dictionary to call additional targeted enumeration functions 
	for serv in serv_dict: 
		ports = serv_dict[serv]	
		if (serv == "http"):
			for port in ports:
				port = port.split("/")[0]
				multProc(httpEnum, ip_address, port, folder)
		elif (serv == "ssl/http") or ("https" in serv):
			for port in ports:
				port = port.split("/")[0]
				multProc(httpsEnum, ip_address, port, folder)
		elif "ssh" in serv:
			for port in ports:
				port = port.split("/")[0]
				multProc(sshEnum, ip_address, port, folder)
		elif "smtp" in serv:
			for port in ports:
				port = port.split("/")[0]
				multProc(smtpEnum, ip_address, port, folder)
		elif "snmp" in serv:
			for port in ports:
				port = port.split("/")[0]
				multProc(snmpEnum, ip_address, port, folder)
		elif ("domain" in serv):
			for port in ports:
				port = port.split("/")[0]
				multProc(dnsEnum, ip_address, port, folder)
		elif ("ftp" in serv):
			for port in ports:
				port = port.split("/")[0]
				multProc(ftpEnum, ip_address, port, folder)
		elif "microsoft-ds" in serv:	
			for port in ports:
				port = port.split("/")[0]
				multProc(smbEnum, ip_address, port, folder)
		elif "ms-sql" in serv:
			for port in ports:
				port = port.split("/")[0]
				multProc(httpEnum, ip_address, port, folder)
	  
	print "INFO: TCP/UDP Nmap scans completed for " + ip_address 
	return


def create_dir(filename):
	if not os.path.exists(os.path.dirname(filename)):
		try:
			os.makedirs(os.path.dirname(filename))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise



# grab the discover scan results and start scanning up hosts
print "############################################################"
print "####                      RECON SCAN                    ####"
print "####            A multi-process service scanner         ####"
print "####        http, ftp, dns, ssh, snmp, smtp, ms-sql     ####"
print "############################################################"
 
if __name__=='__main__':
   
	httpEnum("10.13.13.101", "80", "./recon_enum/")
	exit(0)

	f = open('./targets.txt', 'r') # CHANGE THIS!! grab the alive hosts from the discovery scan for enum
	for scanip in f:
		jobs = []
		p = multiprocessing.Process(target=nmapScan, args=(scanip,))
		jobs.append(p)
		p.start()
	f.close() 
