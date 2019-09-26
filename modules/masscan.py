#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

def execMasscan(domain):
    '''

    :param domain: target domain so we can reach domain.ips file properly
    :return: standard masscan output / errors
    '''
    if os.path.isfile(domain + ".masscan") == False or os.path.getsize(domain + ".masscan") == 0:
        p = subprocess.Popen(
            ['/usr/bin/masscan', '-p', '1-65535', '--randomize-hosts', '-Pn', '-iL', domain + ".ips", '--output-format=list',
             '--output-file=' + domain + ".masscan", '--rate', "10000"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    else:
        out = ""
        err = ""
        print "  + masscan report found, Skipping..."

    return out,err


def parseMasscan(masscanreport, verbose):
    print "[*] Parsing masscan report file"
    m = open(masscanreport, "r")
    masscan_report_content = m.readlines()
    iplist = list()
    for item in masscan_report_content:
        if '#' in item:
            continue
        if "Discovered open port" in item:
            iplist.append(item.split()[5])
            # ['Discovered', 'open', 'port', '45507/tcp', 'on', '192.168.0.1']
        if "open tcp" in item:
            iplist.append(item.split()[3])
    iplist = list(set(iplist))  # uniq
    ipdict = dict((el, 0) for el in iplist)

    if verbose:
        print "  + Filtering entries"

    for unique_ip in iplist:
        pl = list()
        for item in masscan_report_content:
            if '#' in item:
                continue
            if "open tcp" in item:
                if unique_ip == item.split()[3]: #ip
                    pl.append(item.split()[2]) #port
            if "Discovered open port" in item:
                if unique_ip == item.split()[5]: #ip
                    pl.append(item.split()[3].split("/")[0]) #port
        ipdict[unique_ip] = list(pl)

    if verbose:
        print "  + Creating new report"

    f = open(masscanreport + ".new", "w")
    for ip, ports in ipdict.iteritems():
        target_ports = ','.join(ports)
        f.write(ip + ":" + target_ports + "\n")

    f.close()
    if verbose:
        print "  + Done"

    return ipdict