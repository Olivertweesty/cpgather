#!/usr/bin/env python
# -*- coding: utf-8 -*-
# /*
#
#
# */
__version__ = '0.1'

import argparse
import sys
import os

from modules.amass import execAmass, parseAmass
from modules.sublist3r import execSublist3r, parseSublist3r
from modules.subfinder import execSubfinder, parseSubfinder
from modules.massdns import execMassdns, parseMassdns
from modules.masscan import execMasscan
from modules.masstomap import execMton
from modules.nmap import nmap_LoadXmlObject
from modules.misc import loadData, saveData, saveFile, readFile
from modules.s3scanner import execS3Scanner
from modules.waybackmachine import WayBackMachine
from modules.forwarddns import parseForwardDnsFile
from modules.webcheck import FindWebFromList

SUBWL="/usr/share/wordlists/SecLists/Discovery/DNS/bitquark-subdomains-top100000.txt"   # Wordlist for subdomain bruteforcing
RESOLVERS="/usr/share/massdns/lists/resolvers.txt"                                      # List of open DNS we can use to resolve / brute dns subdomains

global CPPATH
CPPATH=os.path.dirname(os.path.realpath(__file__))

'''

mecanica:
OK - receber dominio e/ou lista de ips do escopo - OK 
OK - rodar amass, subfinder e massdns para descobrir os hosts do escopo - OK
OK - rodar masscan pra descobrir portas abertas
OK - dns subdomain bforce - OK
OK - rodar nmap full - OK
OK - decobrir destas portas abertas, quais sao webservers/http - ok
ripar - we have cloudfront cnames? cloudfrunt! git clone https://github.com/disloops/cloudfrunt.git
OK - rodar eyewitness para tirar screenshot de todos os webservers encontrados e publicar - ok
OK - rodar wappalyzer pra identificar stack das aplicacoes - ok
 - rodar photon-crawler (python photon.py -u https://teslamotors.com -l 3 -t 4 --wayback -o teste)
 - rodar cralwer para validar URLS mapeaveis na aplicacao
    - pegar todos os arquivos JS e jogar no LinkFinder para encontrar endpoints
 - rodar gobuster e descobrir diretorios nestes apps (wordlists de common webapps, common dirs, robotsdisallowed, minha custom)
 - identificar todos os webserver com pagina padrao (ngnix, apache, iis, ...)
    - testar a lista de subdominios encontrados contra estes servers e verificar se as apps aparecem (pode ser openproxy, ou pode ser vhost)
    - rodar a ferramenta virtual-host-discovery para forcar vhosts nesse ip (forca-bruta) (pegar wordlist de webapps comuns)
    - hash do EyeWitness pra ver se o resultado muda ? ou size da pagina...
    - CORStest
 - temos wordpress? wpscan
 - temos joomla? jooscan
 - CORStest
 -
 - testes adicionais
 -  brutespray em ftp e ssh
 -  testssl
 -  parameth em webapps + tplmap + sqlmap + grabber (xss) + (ssrf) (identificar se variavel recebe uma URL ou um path pra arquivo, fuzz pra verificar ssrf usando a cheatsheet do jhaddi wlalarmx)
 -  wpscan
 -
 - como estar IDOR ? verificar numeros em parametros (id, email, hash ) tool = commix
 -
 -
 -
 -

'''

def banner():
    print "cpgather "+str(__version__)+" @ dogasantos"
    print "------------------------------------------------"
    print " Recon, Scan, Detect, Map, Analyze, Hack"
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
    parser.add_argument('-ds', '--dirsearch', help='Enable directory discovery', required=False, action='store_true')
    parser.add_argument('-ns', '--noscan', help='Do not execute portscan', required=False, action='store_true')
    parser.add_argument('-ps', '--ports', help='Specify comma separated list of ports that should be scanned (all tcp by default)', required=False, nargs='?')
    parser.add_argument('-b', '--bruteforce', help='Enable FTP and SSH bruteforce', required=False, action='store_true')
    parser.add_argument('-e', '--tlsssl', help='Enable TLS/SSL checks for common vulnerabilities', required=False, action='store_true')
    parser.add_argument('-p', '--parameter', help='Enable parameter discovery', required=False, action='store_true')
    parser.add_argument('-v', '--verbose', help='Enable Verbosity',  required=False, action='store_true')
    parser.add_argument('-sw', '--wordlist', help='Specify a wordlist for subdomain discovery (otherwise default one)', required=False, nargs='?')
    parser.add_argument('-dw', '--dirwordlist', help='Specify a wordlist for directory discovery (otherwise default one)', required=False, nargs='?')
    return parser.parse_args()


def TargetDiscovery(domain,wordlist):
    print "[*] Target Discovery"
    ips = list()
    hosts = list()

    print "  + Running amass"
    execAmass(domain)

    print "  + Running sublist3r"
    execSublist3r(domain)

    print "  + Running WayBack machine query"
    wayback_found_list = WayBackMachine(domain)

    print "  + Running subfinder (bruteforce mode)"
    execSubfinder(domain,wordlist)

    print "  + Parsing subfinder report"
    subfinder_found_list = parseSubfinder(domain)
    for item in subfinder_found_list:
        hosts.append(item.rstrip("\n"))

    print "  + Parsing WayBack machine report"
    for item in wayback_found_list:
        hosts.append(item.rstrip("\n"))

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

def PortScanning(ips, domain, verbose, ports):
    print "[*] Port Scanning phase started"
    if verbose:
        print "  + Running masscan against %s targets" %str(len(ips))
    execMasscan(domain,ports)

    if verbose:
        print "  + Running nmap fingerprinting and scripts"
    execMton(domain)
    #hosts = parseNmapXML(domain + ".nmap.xml")
    nmapObj = nmap_LoadXmlObject(domain + ".nmap.xml")

    return nmapObj


def WebDiscovery(nmapObj, domain):

    print "[*] Web Discovery phase has started"
    webhosts = FindWebFromList(nmapObj,domain)
    print "[*] Scrapping first page of each webhost"
    ScrapWeb(webhosts)


    print "[*] Web Stack identification via (Wappalyzer)"



    '''
        salvar em arquivo .http
        
        rodar wappalyzer
        identificar quais tem tela padrao do webserver
        eyewitness
        dirsearch ou ffuf
        photon crawler 2 niveis
        linkfinder ou outra ferramenta pra pegar todos os arquivos javascript, parsear e descobrir novas urls
         + photon nas urls novas com 2 niveis
         + photon nas urls do dirsearc/ffuf
        identificar webapps conhecidas no report do crawler (fckeditor, jqueryupload, swfupload, etc)
        identificar todos os recursos carregados de URLS externas de cada página, e salvar links quebrados
        gitrob pra verificar .git aberto!
         
    '''

    return True

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
    user_dirsearch = args.dirsearch
    user_bruteforce = args.bruteforce
    user_tlsssl = args.tlsssl
    user_verbose = args.verbose
    user_subdomain_wordlist = args.wordlist
    user_dir_wordlist = args.dirwordlist
    user_noscan = args.noscan
    user_ports = args.ports

    banner()
    if user_dir_wordlist:
        wordlist = user_dir_wordlist
    else:
        wordlist = SUBWL

    if user_ports is not None:
        ports = user_ports
    else:
        ports="1-65535"


    ips,hosts = TargetDiscovery(user_domain,wordlist)
    if not user_noscan:
        if os.path.isfile(user_domain+".pickle") == False or os.path.getsize(user_domain+".pickle") == 0:
            nmapObj = PortScanning(ips, user_domain, user_verbose, ports)
            if nmapObj is not False:
                saveData(user_domain+".pickle",nmapObj)
            else:
                print("  + no open ports found")
        else:
            nmapObj=loadData(user_domain+".pickle")
    else:
        nmapObj=False

    if nmapObj is not False:
        list_of_webservers_found = WebDiscovery(nmapObj, user_domain)
    else:
        print("[*] Web discovery skipped (no open ports found)")
    S3Discovery(user_domain, user_verbose)



