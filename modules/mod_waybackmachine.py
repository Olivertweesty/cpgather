#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
from . import misc

def WayBackMachine(domain):
    if os.path.isfile(domain + ".sub.wayback") == False or os.path.getsize(domain + ".sub.wayback") == 0:
        url = "http://web.archive.org/cdx/search/cdx?url=*."+domain+"&output=json&fl=original&collapse=urlkey"
        response = requests.get(url)
        jdata = response.json()
        hostnames = list()
        for item in jdata:
            proto, host, port = misc.parseUrlProtoHostPort(item[0])
            if "host" not in host and len(host)>2:
                hostnames.append(host)
        hostnames=list(set(hostnames))
        misc.saveFile(domain + ".sub.wayback", hostnames)

    else:
        hostnames=list()
        temp = misc.readFile(domain + ".sub.wayback")
        for item in temp:
            if len(item) > 2:
                hostnames.append(item.rstrip("\n"))
    return hostnames
