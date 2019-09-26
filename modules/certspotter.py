#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import requests
import sys

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

def Certspotter(domain):

    if os.path.isfile(domain + ".sub.certspotter") == False or os.path.getsize(domain + ".sub.certspotter") == 0:
        url = "https://api.certspotter.com/v1/issuances?domain=" + domain + "&include_subdomains=true&expand=dns_names&expand=issuer&expand=cert"
        response = requests.get(url)
        everyline=response.text.split("\n")
        for line in everyline:
            if "dns_names" in line:
                nospaces = line.replace(" ","")
                print nospaces



    return True




hnames = Certspotter("starbucks.com")
