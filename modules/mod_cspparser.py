#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

def getCspPolicyFromUrl(url):

    csp_header=""
    response = requests.get(url)
    if 'Content-Security-Policy' in response.headers:
        csp_header = response.headers['Content-Security-Policy']
    elif 'content-security-policy-report-only' in response.headers:
        csp_header = response.headers['content-security-policy-report-only:']
    return csp_header


def parseCspPolicy(domain,csp_header):

    same_domain = list()
    other_domain = list()
    o_host, o_dom, o_tld = splitHostname(domain)
    for tok in csp_header.split():
        if "http" in tok:
            hname = tok.rstrip(';')
            a,b,c = splitHostname(hname)
            if b == o_dom and c == o_tld:
                same_domain.append(hname)
            else:
                other_domain.append(hname)
    return same_domain,other_domain