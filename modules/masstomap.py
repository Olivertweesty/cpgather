#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import xml.dom.minidom
from base64 import b64encode

def execMton(domain):

    workingdir = os.getcwd()
    if os.path.isfile(domain + ".nmap.xml") == False and \
            os.path.isfile(domain + ".nmap.grepable") == False and \
            os.path.isfile(domain + ".nmap.txt") == False:

        p = subprocess.Popen(
            ['masstomap', '-m', workingdir + "/" + domain + ".masscan", '-o', workingdir + "/" + domain, '-vv'],cwd=workingdir,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
    else:
        out = ""
        err = ""
        print "  + Nmap report found, Skipping..."

    print err

    return out,err


def parseNmapXML(xmlreport):
    '''
        the parsing scheme has been taken from here: https://github.com/argp/nmapdb
        all credits to Patroklos Argyroudis - argp
        i'm just doing something different with the data
    '''
    print "   + Parsing portscan reports"

    if os.path.isfile(xmlreport) == False:
        print "[x] There is no portscan report here"
        return False
    if os.path.getsize(xmlreport) == 0:
        print "[x] There is no portscan content here"
        return False
    seen = list()
    hosts = list()
    doc = xml.dom.minidom.parse(xmlreport)

    for host_item in doc.getElementsByTagName("host"):
        try:
            a = host_item.getElementsByTagName("address")[0]
            ipaddress = a.getAttribute("addr")
        except:
            pass

        try:
            h = host_item.getElementsByTagName("hostname")[0]
            hostname = h.getAttribute("name")
        except:
            hostname = ""

        try:
            s = host_item.getElementsByTagName("hostscript")[0]
            script = s.getElementsByTagName("script")[0]
            sid = script.getAttribute("id")
            output = script.getAttribute("output")
            host_script = "%s:%s" % str(sid, b64encode(output))
        except:
            host_script = ""

        try:
            p = host_item.getElementsByTagName("ports")[0]
            ports = p.getElementsByTagName("port")
        except:
            pass

        for port_item in ports:

            port_number = port_item.getAttribute("portid")
            protocol = port_item.getAttribute("protocol")
            state_el = port_item.getElementsByTagName("state")[0]
            state = state_el.getAttribute("state")

            try:
                service = port_item.getElementsByTagName("service")[0]
                if service.getAttribute("tunnel"):
                     port_tls = True
                else:
                        port_tls = False

                port_name = service.getAttribute("name")
                product_descr = service.getAttribute("product")
                product_ver = service.getAttribute("version")
                product_extra = service.getAttribute("extrainfo")
            except:
                service = ""
                port_name = ""
                product_descr = ""
                product_ver = ""
                product_extra = ""

            service_str = "%s %s %s" % (product_descr, product_ver, product_extra)

            info_str = ""

            for i in (0, 1):
                try:
                    script = port_item.getElementsByTagName("script")[i]
                    script_id = script.getAttribute("id")
                    script_output = script.getAttribute("output")
                except:
                    script_id = ""
                    script_output = ""

                if script_id != "" and script_output != "":
                    info_str += "%s: %s\n" % (script_id, b64encode(script_output))

            if ipaddress + ":" + port_number in seen:
                continue
            else:
                seen.append(ipaddress + ":" + port_number)

                host = dict()
                host['ipaddr'] = ipaddress
                host['port'] = port_number
                host['proto'] = protocol
                host['name'] = port_name
                host['tls'] = port_tls
                host['state'] = state
                host['banner'] = service_str
                host['svc_script'] = info_str
                host['host_script'] = host_script
                hosts.append(host)

    return hosts