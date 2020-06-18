#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /*
#
#
# */
__version__ = '1.0'

import argparse
import sys
import os
import json

from modules.mod_amass import execAmass, parseAmass
from modules.mod_sublist3r import execSublist3r, parseSublist3r
from modules.mod_subfinder import execSubfinder, parseSubfinder
from modules.mod_massdns import execMassdns, parseMassdns
from modules.mod_masscan import execMasscan
from modules.masstomap import execMton
from modules.mod_nmap import nmap_LoadXmlObject
from modules.misc import saveFile, readFile, appendFile
from modules.mod_s3scanner import execS3Scanner
from modules.mod_waybackmachine import WayBackMachine
from modules.mod_crtsh import crtshQuery

from modules.mod_forwarddns import parseForwardDnsFile
from modules.mod_webcheck import FindWeb, RetrieveWebContent, wappFormat

SUBWL="/usr/share/wordlists/commonspeak2-wordlists/subdomains/subdomains.txt"
RESOLVERS="/usr/share/massdns/lists/resolvers.txt"                                      # List of open DNS we can use to resolve / brute dns subdomains

global CPPATH
CPPATH=os.path.dirname(os.path.realpath(__file__))


def banner():
    print "cpgather "+str(__version__)+" @ dogasantos"
    print "------------------------------------------------"
    print " subdomains, portscan, webstack, "
    print "------------------------------------------------"

def parser_error(errmsg):
    banner()
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: %s" %errmsg)
    sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -d target.com -l target-ip-list.txt -s phase")
    parser.error = parser_error
    parser._optionals.title = "Options:"
    parser.add_argument('-d', '--domain', help="Domain name we should work with", required=True)
    parser.add_argument('-ps', '--ports', help='Specify comma separated list of ports that should be scanned (all tcp by default)', required=False, nargs='?')
    parser.add_argument('-v', '--verbose', help='Enable Verbosity',  required=False, action='store_true')
    parser.add_argument('-sw', '--wordlist', help='Specify a wordlist for subdomain discovery (otherwise default one)', required=False, nargs='?')
    return parser.parse_args()


def TargetDiscovery(domain,wordlist):
    print "[*] Subdomain discovery phase"
    ips = list()
    hosts = list()

    print "  + Running amass"
    execAmass(domain)

    print "  + Running sublist3r"
    execSublist3r(domain)

    print "  + Running WayBack machine query"
    wayback_found_list = WayBackMachine(domain)

    #print "  + Running Crt.sh query"
    #crtsh_found_list = crtshQuery(domain)

    print "  + Running subfinder (bruteforce mode)"
    execSubfinder(domain,wordlist)

    print "  + Parsing subfinder report"
    subfinder_found_list = parseSubfinder(domain)
    for item in subfinder_found_list:
        hosts.append(item.rstrip("\n"))

    print "  + Parsing WayBack machine report"
    for item in wayback_found_list:
        hosts.append(item.rstrip("\n"))

    #print "  + Parsing Crt.sh report"
    #for item in crtsh_found_list:
    #    hosts.append(item.rstrip("\n"))

    print "  + Parsing amass report"
    amass_found_list = parseAmass(domain)
    for item in amass_found_list:
        hosts.append(item.rstrip("\n"))

    print "  + Parsing sublist3r report"
    sublist3r_found_list = parseSublist3r(domain)
    for item in sublist3r_found_list:
        hosts.append(item.rstrip("\n"))

    if os.path.isfile(domain + ".forwarddns") == True and os.path.getsize(domain + ".forwarddns") > 1:
        print("  + Parsing Forward Dns (project sonar) json file")
        fdns_host_list,fdns_cname_list = parseForwardDnsFile(domain)
        for h in fdns_host_list:
            hosts.append(h.rstrip("\n"))

    uhosts = list(set(hosts))

    saveFile(domain + ".hosts", uhosts)
    print "  + Hosts file created: " + domain + ".hosts"

    print "  + Running massdns"
    execMassdns(domain,RESOLVERS)
    print "  + Parsing massdns report"
    massdns_iplist = parseMassdns(domain)
    for nip in massdns_iplist:
        ips.append(nip)

    unique_ips = list(set(ips))
    saveFile(domain + ".ips", unique_ips)
    print "  + IPs file created: " + domain + ".ips"
    print "[*] Done: %d ips and %d hosts discovered" % (len(unique_ips), len(uhosts))

    return unique_ips,uhosts

def WebDiscovery(nmapObj, domain):
    print "[*] Web Discovery phase has started"
    if os.path.isfile(domain+".web") == False or os.path.getsize(domain+".web") == 0:
        webhosts=FindWeb(domain, nmapObj)
        saveFile(domain + ".web", webhosts)
    else:
        webhosts = readFile(domain + ".web")


    print "[*] Web Stack identification via (Wappalyzer)"
    if os.path.isfile(domain+".wapp") == False or os.path.getsize(domain+".wapp") == 0:
        list_of_webstack = RetrieveWebContent(webhosts)
        list_of_webstack = wappFormat(list_of_webstack)

        for item in list_of_webstack:
            njson = json.dumps(item)
            appendFile(domain + ".wapp", njson)
            appendFile(domain + ".web." + str(item['status']) + ".txt", item['url']+"\n")
    else:
        list_of_webstack = readFile(domain + ".wapp")



    return webhosts,list_of_webstack

def S3Discovery(domain,verbose):
    print "[*] S3 Buckets Discovery phase has started"
    execS3Scanner(domain)
    list = readFile(domain+".buckets")
    if verbose:
        for bucket in list:
            print "    + Bucket Found: %s" %str(bucket.rstrip("\n"))
    return True


if __name__ == "__main__":
    args = parse_args()
    user_domain = args.domain
    user_verbose = args.verbose
    user_subdomain_wordlist = args.wordlist
    user_ports = args.ports
    banner()
   
    if user_ports is not None:
        ports = user_ports
    else:
        ports="80,443,8080,8443"
    nmapObj = False
    
    ips,hosts = TargetDiscovery(user_domain,user_subdomain_wordlist)
    if len(ips) == 0:
        user_noscan = True

    if not user_noscan:
        print "[*] Port Scanning phase started"
        if os.path.isfile(user_domain + ".nmap.xml") == False or os.path.getsize(user_domain + ".nmap.xml") == 0:
            print "  + Running masscan against %s targets" % str(len(ips))
            execMasscan(user_domain, ports)
            oports = readFile(user_domain + ".masscan")
            if len(oports) > 0:
                print("  + Running nmap fingerprinting and scripts")
                execMton(user_domain)
            else:
                print("[x] No open ports found for this domain. Aborting...")
                sys.exit(1)
        else:
            print "  + Nmap report found, loading data..."
        nmapObj = nmap_LoadXmlObject(user_domain + ".nmap.xml")

    if nmapObj:
        list_of_webservers_found, list_of_webstack = WebDiscovery(nmapObj, user_domain)


    else:
        print("[*] Web discovery skipped (no open ports found)")

    S3Discovery(user_domain, user_verbose)

    print("[*] cpgather finished! ")




