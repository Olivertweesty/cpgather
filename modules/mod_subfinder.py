#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess


def getSubfinderRawFile(domain):
    with open(domain + ".subfinder", "r") as f:
        content = f.readlines()
    return content

def execSubfinder(domain,wordlist):
    if os.path.isfile(domain + ".subfinder") == False or os.path.getsize(domain + ".subfinder") == 0:
        p = subprocess.Popen(
            ['subfinder', '-d', domain, '-b','-w',wordlist, '-t', '100','-nW','-o', domain + ".subfinder"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    else:
        out = ""
        err = ""
        print "  + Subfinder report found. Skipping..."
    return out,err

def parseSubfinder(domain):

    sf_hostlist = list()
    if os.path.isfile(domain + ".subfinder"):
        f = open(domain + ".subfinder", "r")
        content = f.readlines()
        for item in content:
            sf_hostlist.append(item.rstrip('\n'))
        sf_hostlist = list(set(sf_hostlist))
        f.close()

    return sf_hostlist



