#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from modules.mod_settings import DOCUMENT_ROOT
import subprocess


def setEyePublic(domain):
    local = domain + ".eye"
    destination = DOCUMENT_ROOT + "/" + domain + '.eye'
    os.rename(local,destination)
    os.link(destination, local)

    return True

def execEyeWitness(domain):
    local = domain+".eye"
    if os.path.isdir(local) == False:
        os.mkdir(local)

    if os.path.isfile(local+"/report.html") == False:
        p = subprocess.Popen(
            ['/usr/share/EyeWitness/EyeWitness.py', '--web', '-f', domain + ".webservers",
            '-d', local, '--no-prompt'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    else:
        print "    + Skiping EyeWitness (you already have a report file for this domain)"

    return out,err

