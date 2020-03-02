#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.mod_massdns import parseMassdnsStruct
from modules.misc import sort_uniq

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

scrapdata = list()

def getHostnameFromIp(massdnsstruct,ip):
    host_ips = list()
    for node in massdnsstruct:
        if str(node['ipaddr'].rstrip()) == str(ip.rstrip()):
            host_ips.append(str(node['vhost'].rstrip()))
    return host_ips

def FindWeb(domain, nmapObj):
    weblist = list()
    massdnsstruct = parseMassdnsStruct(domain)

    for ip in nmapObj.all_hosts():
        vhostlist = getHostnameFromIp(massdnsstruct, ip)
        openports = nmapObj[ip]['tcp'].keys()
        for port in openports:
            service_details = nmapObj[ip]['tcp'][port]
            for wtag in web_service_names:
                if wtag == service_details['name']:
                    proto = "http"
                    if service_details['name'] == 'ssl' \
                            or 'https' in service_details['name'] \
                            or service_details['tunnel'] == "ssl":
                        proto = "https"

                    if len(vhostlist) > 0:
                        for vhost in vhostlist:
                            weblist.append(proto + "://" + vhost + ":" + str(port))
                    else:
                        weblist.append(proto + "://" + ip + ":" + str(port))

    weblist = sort_uniq(weblist)
    return weblist


