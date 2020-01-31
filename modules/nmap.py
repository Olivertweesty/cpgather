#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nmap

def nmap_create():
    return nmap.PortScanner()

def nmap_LoadXmlObject(filename):
    nm = nmap.nmap_create()
    nxo = open(filename, "r")
    xmlres = nxo.read()
    nm.analyse_nmap_xml_scan(xmlres)
    return nm

def nmap_GetSinglePortState(target, proto, targetport):

    print("[*] nmap_GetSinglePortState")
    targetport = int(targetport)
    target = str(target)

    NMAP_ARGUMENTS = "--privileged -Pn --open "
    if proto == "udp":
        NMAP_ARGUMENTS += "-sU "
    if proto == "tcp":
        NMAP_ARGUMENTS = "-sS "

    nm = nmap_create()
    results = nm.scan(hosts=target, ports=str(targetport), arguments=NMAP_ARGUMENTS)
    hostresults = results['scan']
    if not hostresults:
        return False

    if hostresults[target][proto][targetport]['state'] == "open":
        return True
    else:
        return False


def nmap_ExecuteNmapOnTargetList(domain, ports):
    targetfile = domain+".ips"

    NMAP_SCRIPTS = 'http-title,http-server-header,http-methods,' \
                   'ssl-cert,ssl-enum-ciphers,' \
                   'banner'

    NMAP_ARGUMENTS = "--privileged -Pn --open -f -sV " \
                     "-oG " + domain + ".nmap.grepable" \
                     " -oN  " + domain + ".nmap.text" \
                     " --script=" + NMAP_SCRIPTS + \
                     " -iL " + targetfile


    nmObj = nmap_create()
    nmObj.scan(hosts="", ports=ports, arguments=NMAP_ARGUMENTS)
    xmlout = nmObj.get_nmap_last_output()
    xmlreportfile = projectname + ".nmap.xml"
    fx = open(xmlreportfile, "w")
    fx.write(xmlout)
    fx.close()
    return nmObj


def nmap_GetScriptData(nmapObj, host, proto, port, scriptname):
    try:
        data=nmapObj[host][proto][int(port)]['script'][scriptname]
    except:
        data=False
    return data


def nmap_ShowPrettyReport(nmapObj):
    print("[*] Nmap report")
    for ip in nmapObj.all_hosts():
        print("[*] Host: " + ip)
        openports = nmapObj[ip]['tcp'].keys()
        for port in openports:
            service_details = nmapObj[ip]['tcp'][port]
            print("[*] Port: " + str(port))
            print("  + Product: " + service_details['product'])
            print("  + version: " + service_details['version'])
            print("  + name: " + service_details['name'])
            print("  + state: " + service_details['state'])
            try:
                scripts = service_details['script']
                for script_name in scripts:
                    print("  + script: " + script_name)
                    print(service_details['script'][script_name].replace("\\n", "\n"))
                    print("=" * 100)
            except:
                pass
    return True

def nmap_ListOpenTcpPorts(nmapObj):
    pitem=list()
    allports = list()
    for ip in nmapObj.all_hosts():
        openports = nmapObj[ip]['tcp'].keys()
        pitem.append(openports)

    for hostitem in pitem:
        for plist in hostitem:
            allports.append(plist)

    return allports


