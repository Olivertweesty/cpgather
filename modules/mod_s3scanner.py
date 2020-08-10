#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import os



def execS3Scanner(domain):
    '''
    :param domain: target domain
    :return: amass std output and errors
    '''

    if os.path.isfile(domain + ".buckets") == False or os.path.getsize(domain + ".buckets") == 0:
        p = subprocess.Popen(['s3scanner', '-o', domain + ".buckets", domain + ".hosts"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()

    else:
        out = ""
        err = ""
        print("  + S3 Bucket list found, skipping...")

    return out,err

