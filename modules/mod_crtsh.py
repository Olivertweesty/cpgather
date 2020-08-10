#!/usr/bin/env python
# -*- coding: utf-8 -*-
from . import misc
from crtsh import crtshAPI
import os
import json


def crtshQuery(domain):
    found = list()
    if os.path.isfile(domain + ".sub.crtsh") == False or os.path.getsize(domain + ".sub.crtsh") == 0:
        try:
            rawlist = crtshAPI().search(domain)[0]
        except:
            rawlist = list()

        for item in rawlist:
            print("="*10)
            print(item)
            print(len(item))
            print(type(item))
            print("="*10)
            item = json.loads(item)
            for k, v in item.items():
                if k == "name_value":
                    if '@' in v:
                        continue
                    if '*' in v:
                        continue
                    if misc.checkFqdn(v) == False:
                        continue
                    if '\n' in v:
                        for tok in v.split('\n'):
                            found.append(tok)
                    else:
                        found.append(v)

        found = list(set(found))
        misc.saveFile(domain + ".sub.crtsh", found)
    else:

        temp = misc.readFile(domain + ".sub.crtsh")
        for item in temp:
            if len(item) > 2:
                found.append(item.rstrip("\n"))
    return found
