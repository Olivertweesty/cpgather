#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ipaddress
import pickle
import os
from tldextract import extract
from fqdn import FQDN
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def uniq(listval):
    last = object()
    for item in listval:
        if item == last:
            continue
        yield item
        last = item

def sort_uniq(listval):
    return list(uniq(sorted(listval)))

def checkFqdn(val):
    fqdn = FQDN(str(val))
    return fqdn.is_valid

def splitHostname(hname):
    try:
        host, domain, tld = extract(hname)
        return host,domain,tld
    except:
        return False,False,False


def loadData(file):
    with open(file, 'rb') as f:
        ndata = pickle.load(f)

    return ndata

def saveData(file,data):
    with open(file, 'wb') as f:
        pickle.dump(data, f)

def saveFile(filename,content):
    with open(filename, "w") as h:
        for item in content:
            h.write(item + "\n")

def appendFile(filename,content):
    with open(filename, "a") as h:
        h.write(content)

def readFile(filename):
    if os.path.isfile(filename) == False:
        return False
    with open(filename, "r") as f:
        content = f.readlines()
    return content

def parseUrlProtoHostPort(urlstr):
    proto = ""
    host = ""
    port=""
    uridata = urlparse(urlstr)
    proto = str(uridata.scheme)
    if len(uridata.scheme) < 2: # "//"
        proto = "http"

    if ":" in uridata.netloc: # we have a port definition
        port = str(uridata.netloc.split(':')[1])
        host = str(uridata.netloc.split(':')[0])
    else:
        if uridata.scheme == "http":
            port = "80"
        if uridata.scheme == "https":
            port = "443"
        host = str(uridata.netloc)

    return proto,host,port

def getUrlPath(url):
    uridata = urlparse(url)
    return uridata.path

def getFullHostList(domain):
    try:
        from modules.mod_amass import parseAmassStruct
    except:
        pass
    hosts_file = readFile(domain+".hosts")
    unique = list()
    for h in hosts_file:
        hosts = dict()
        found = False
        h_from_hostsfile = h.rstrip('\n').rstrip(' ')

        massdns_structured_hosts = parseMassdnsStruct(domain)
        amass_structured_hosts = parseAmassStruct(domain)

        for m_item in massdns_structured_hosts:
            if m_item['A'] == h_from_hostsfile:
                hosts['A'] = m_item['A']
                hosts['ipv4'] = m_item['ipv4']
                unique.append(hosts)
                found = True
                break

        if found == True:
            continue

        for a_item in amass_structured_hosts:
            if a_item['A'] == h_from_hostsfile:
                hosts['A'] = a_item['A']
                hosts['ipv4'] = a_item['ipv4']
                unique.append(hosts)
                break

    return unique

def isGlobalIpv4(ipaddr):
    try:
        ipObj = ipaddress.ip_address(unicode(ipaddr))
    except:
        try:
            ipObj = ipaddress.ip_address(ipaddr)
        except:
            return False
    if ipObj.is_private == False and ipObj.version == 4:
        return True
    else:
        return False

def ipFilter(iplist):
    unique = list()
    for ip in iplist:
        new = ip.rstrip('\n')
        if isGlobalIpv4(new):
           if new not in unique:
               unique.append(new)
    return unique

def hostFilter(hostlist):
    unique = list()
    for host in hostlist:
        nhost = host.rstrip('\n')
        if nhost not in unique:
            unique.append(nhost)
    return unique

def isMimetype(valor):
    if os.path.isfile("/etc/mime.types") == False:
        return False
    with open("/etc/mime.types", "r") as f:
        content = f.read()
        if re.search(valor,content):
            return True
        return False
