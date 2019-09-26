#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os
from modules.linkfinder import execLinkFinder, parseLinkFinder

def getPhotonRawFile(filename):
    with open(filename, "r") as f:
        content = f.readlines()
    return content


def splitURI(target):
    from urlparse import urlparse
    uriobj = urlparse(target)
    hostname = uriobj.hostname.rstrip('\n')
    protocol = uriobj.scheme
    if uriobj.port is None:
        port = "80"
    else:
        port = str(uriobj.port)
    path = uriobj.path
    query = uriobj.query
    fragment = uriobj.fragment

    return hostname,protocol,port,path,query,fragment

def execPhoton(target,savedir):
    '''
    :param domain: Target domain so we can reach related files (massdns report and hosts file)
    :param resolvers: A list of open dns servers (resolvers), 1 per line
    :return: the massdns execution output (standard and errors)
    '''

    vhost, proto, port, path, query, fragment = splitURI(target)

    # format: domain.crawler/n.domain.com.443/
    reportlocation = savedir + "/" + vhost + "." + port

    if os.path.isdir(savedir) == False:
        os.mkdir(savedir)
        os.mkdir(reportlocation)

    p = subprocess.Popen(['/usr/share/photon/photon.py', '-u', target, '-o',reportlocation ,'-t','4', '--level','1','--wayback' ],stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    return out, err

def dumpEndpoints(jsfile,list_endpoints,location):
    report = location + "/script." + jsfile.replace("/","-").replace(" ","")
    f = open(report,"w")
    for ep in list_endpoints:
        f.write(ep)


def parsePhoton(target,savedir):
    vhost, proto, port, path, query, fragment = splitURI(target)
    reportlocation = savedir + "/" + vhost + "." + port

    scripts = reportlocation +"/scripts.txt"
    if os.path.isfile(scripts):
        scriptfound = getPhotonRawFile(scripts)
        for jsfile in scriptfound:
            savefile = execLinkFinder(jsfile)
            list_endpoints = parseLinkFinder(savefile)
            dumpEndpoints(jsfile,list_endpoints,reportlocation)

        # to-do: feed photon with new discovered js/endpoints
        # parsescripts, send to linkfinder, feed crawler to check those endpoints
        # linkfinder -o 1.html -i http://201.63.229.138/JS/release/automidia.applauncher.js


    intel = reportlocation +"/intel.txt"
    if os.path.isfile(intel):
        pass # placeholder
             # s3 buckets list among other useful things

    fuzzable = reportlocation +"/fuzzable.txt"
    if os.path.isfile(fuzzable):
        found = len(getPhotonRawFile(fuzzable))
             # we can feed sqli, commix, and others with this
    else:
        found = 0

    robots = reportlocation +"/robots.txt"
    if os.path.isfile(robots):
        pass # placeholder
             # we cab just add this to burp later if we're not using burp as proxy atm


    externalreferences = reportlocation + "/external.txt"
    if os.path.isfile(externalreferences):
        pass # placeholder
             # check for broken references
             # takeover

    return found