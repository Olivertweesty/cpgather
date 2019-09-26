#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
from lxml import etree

def parseLinkFinder(savefile):
    tree = etree.parse(savefile)
    endpoints = list()
    for element in tree.xpath('//div[@class="container"]//*'):
        endpoints.append(element.text)

    return endpoints


def execLinkFinder(remote_jsfile,reportlocation):
    vhost, proto, port, path, query, fragment = splitURI(remote_jsfile)

    savefile = reportlocation+"/lfinder"+npath+".html"
    # target = https://sub.domain.com/JS/release/endpoints.js
    # reportlocation = domain.com.crawler/sub.domain.com.443/
    # npath = lfinder-JS-release-endpoints.js.html
    npath = path.replace("/","-").replace(" ","")
    p = subprocess.Popen(
        ['linkfinder', '-o', savefile ,'-i', remote_jsfile],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    return savefile