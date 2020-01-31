#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess

def execSublist3r(domain):
    if os.path.isfile(domain + ".sublist3r") == False or os.path.getsize(domain + ".sublist3r") == 0:

        p = subprocess.Popen(['sublist3r', '-d', domain, '-o', domain + ".sublist3r"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    else:
        out = ""
        err = ""
        print "  + Sublist3r report found. Skipping..."

    return out,err

def parseSublist3r(domain):
    found = list()
    if os.path.isfile(domain + ".sublist3r"):
        f = open(domain+".sublist3r")
        content = f.readlines()
        for item in content:
            found.append(item.rstrip("\n"))
    return found
