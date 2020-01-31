#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from modules.misc import isGlobalIpv4, readFile


def execMassdns(domain,resolvers):
    '''
    :param domain: Target domain so we can reach related files (massdns report and hosts file)
    :param resolvers: A list of open dns servers (resolvers), 1 per line
    :return: the massdns execution output (standard and errors)
    '''
    if os.path.isfile(domain + ".massdns") == False or os.path.getsize(domain + ".massdns") == 0:
        p = subprocess.Popen(
            ['massdns', '-r', resolvers, '-t', "A", '-o', "S", '-w', domain + ".massdns", domain + ".hosts"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

    else:
        out = ""
        err = ""
        print "  + massdns report found, Skipping..."

    return out, err


def parseMassdns(domain):
    iplist = list()
    content = readFile(domain+".massdns")
    for item in content:
        if " CNAME " in item: # no cnames, please
            continue
        ip=item.split()[2]
        if isGlobalIpv4(ip):
            iplist.append(ip.rstrip("\n"))
    return iplist

def parseMassdnsStruct(domain):
    m_file = readFile(domain+".massdns")
    aux=list()
    for massdns_item in m_file:
        hosts=dict()
        line = massdns_item.replace('. ', ',').replace(' ', ',')
        if line.split(',')[1] == "CNAME":
            continue
        host_massdns = line.split(',')[0].rstrip('\n')
        ip_massdns = line.split(',')[2].rstrip('\n')

        if isGlobalIpv4(ip_massdns):
            hosts['vhost'] = host_massdns
            hosts['ipaddr'] = ip_massdns
            aux.append(hosts)

    return aux


def getAllipsFor(url):
    ips = list()
    url = url.rstrip("/")
    host, dom, tld = splitHostname(url)
    ipdb = parseMassdnsStruct(dom + "." + tld)
    for line in ipdb:
        if url == line['vhost']:
            ips.append(line['ipaddr'])

    return ips