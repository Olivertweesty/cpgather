#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

def execWappalyzer(target):
    p = subprocess.Popen(["wappalyzer", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #p = subprocess.Popen(["/usr/bin/nodejs","/usr/share/wappalyzer/node_modules/wappalyzer/index.js", target], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out,err
