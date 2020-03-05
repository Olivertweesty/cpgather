#!/usr/bin/env python
# -*- coding: utf-8 -*-
from misc import readFile, saveFile
from crtsh import crtshAPI


def crtshQuery(domain):
    found = list()
    if os.path.isfile(domain + ".sub.crtsh") == False or os.path.getsize(domain + ".sub.crtsh") == 0:

        rawlist = crtshAPI().search(domain)[0]
        for item in rawlist:
            for k, v in item.items():
                if k == "name_value":
                    if '\n' in v:
                        for tok in v.split('\n'):
                            found.append(tok)
                    else:
                        found.append(v)

        found = list(set(found))
        saveFile(domain + ".sub.crtsh", found)

    else:

        temp = readFile(domain + ".sub.crtsh")
        for item in temp:
            if len(item) > 2:
                found.append(item.rstrip("\n"))
    return found
