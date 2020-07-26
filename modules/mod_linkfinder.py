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


def execLinkFinder(remote_jsfile):
    p = subprocess.Popen(
        ['linkfinder', '-o cli' ,'-i', remote_jsfile],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out