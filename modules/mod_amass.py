#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import validators
from modules.misc import readFile


def execAmass(domain):
    out = ""
    err = ""
    if os.path.isfile(domain + ".amass") == False or os.path.getsize(domain + ".amass") == 0:
        p = subprocess.Popen(
            ['amass', 'enum', '--passive', '-o', domain + ".amass", '-d',domain],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    else:
        print("  + Amass report found. Skipping...")

    return out,err


def parseAmass(domain):
    content=""
    if os.path.isfile(domain + ".amass"):
        with open(domain+".amass", "r") as f:
            content = f.readlines()

    return content

def parseAmassStruct(domain):
    a_file = readFile(domain+".amass")
    aux=list()
    for amass_item in a_file:
        hosts = dict()
        host_amass = amass_item.split(',')[0].rstrip('\n')
        ip_amass = amass_item.split(',')[1].rstrip('\n')

        if validators.ipv4(ip_amass):
            hosts['A'] = host_amass
            hosts['ipv4'] = ip_amass
            aux.append(hosts)
    return aux
