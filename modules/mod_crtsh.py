#!/usr/bin/env python
# -*- coding: utf-8 -*-

from crtsh import crtshAPI

def crtsh(domain):
    found = list()
    rawlist = crtshAPI().search(domain)[0]
    for item in rawlist:
        for k,v in item.items():
            if k == "name_value":
                if '\n' in v:
                    for tok in v.split('\n'):
                        found.append(tok)
                else:
                    found.append(v)

    found = list(set(found))
    return found