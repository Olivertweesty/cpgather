#!/usr/bin/env python
# -*- coding: utf-8 -*-
#shoutz to project sonar@rapid7
import json
from modules.misc import splitHostname
try:
    from modules.misc import readFile
except:
    pass

def parseForwardDnsFile(domain):
    list_of_hostnames = list()
    cnames_found = list()
    originalsub, originalhost, originaltld = splitHostname(domain)

    rawf = readFile(domain + ".forwarddns")
    for line in rawf:
        jsondata = json.loads(line)
        name = jsondata["name"]
        value = jsondata["value"]

        if jsondata["type"] == "a":
            proto, host, tld = splitHostname(name)
            if host == originalhost and tld == originaltld:
                list_of_hostnames.append(name)

        if jsondata["type"] == "cname":
            proto, host1, tld1 = splitHostname(name)
            proto, host2, tld2 = splitHostname(value)

            if (host1 == originalhost and tld1 == originaltld) or (host2 == originalhost and tld2 == originaltld):
                crecord = dict()
                crecord["sub"] = name
                crecord["dst"] = value
                cnames_found.append(crecord)

    list_of_hostnames=list(set(list_of_hostnames))

    return list_of_hostnames,cnames_found