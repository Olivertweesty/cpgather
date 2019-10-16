#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import pytesseract
import cv2
import os
from modules.photon import execPhoton, parsePhoton
from modules.massdns import parseMassdnsStruct
from reppy.robots import Robots

#dirsearch/dirsearch.py -b -t 100 -e php,asp,aspx,jsp,html,zip,jar,sql -x 500,503 -r -w $WORDLIST_PATH/raft-large-words.txt -u $url --plain-text-report=$DIR_PATH/dirsearch/$fqdn.tmp






def findJWT(url):
    '''
    testing
    :param url:
    :return:
    '''
    jwtvalue = ""
    response = requests.get(url)
    if 'jwt-session' in response.headers['Set-Cookie']:
        cookie = response.headers['Set-Cookie']
        for cval in cookie.split(";"):
            if "jwt-session" in cval:
                jwtvalue = cval.split("=")[1]

    elif 'JWT' in response.headers and "Authorization" in response.headers:
        jwtvalue = response.headers['Authorization']
    print response.headers
    return jwtvalue

# nao temos nmapobj
def FindWebFromNmapObj(nmapObj,list_of_hosts_found):
    print "[*] FindWeb"
    weblist = list()

    for ip in nmapObj.all_hosts():
        openports = nmapObj[ip]['tcp'].keys()
        for port in openports:
            service_details = nmapObj[ip]['tcp'][port]
            if "http" in service_details['name']:
                proto = "http"
                try:
                    scripts = service_details['script']
                    for script_name in scripts:
                        if script_name == "ssl-cert":
                            proto = "https"
                except:
                    pass

                if len(list_of_hosts_found) > 0:
                    for item in list_of_hosts_found:
                        if ip in item:
                            vhost = item.split(":")[0]
                            weblist.append(proto + "://" + vhost + ":" + str(port))
                weblist.append(proto + "://" + ip + ":" + str(port))

    weblist = sort_uniq(weblist)
    return weblist


def FindWebFromList(list_of_host_dict,domain):
   return False


'''
{'tls': False,
'name': u'http',
'ipaddr': u'104.27.150.118',
'svc_script': u'fingerprint-strings: AAAAAAA\
                http-headers: AAAAAA',
'state': u'open',
'host_script': '',
'banner': u'cloudflare  ',
'port': u'80'
}

'''

def FindWebFromList_old(list_of_host_dict,list_of_hosts_found):
    web = list()
    for host in list_of_host_dict:
        srv=dict()

        found=False
        # we have http[s]-alt when nmap can't probe due to firewall restrictions.
        # so it will assume http[s] to standard 80 443 ports, and http[s]-alt for non standard ports.

        if host['name'] == "http" or host['name'] == "http-alt":
            srv['proto'] = "http://"
            srv['ipaddr'] = host['ipaddr']
            srv['port'] = host['port']
            found=True

        if host['name'] == "https" or host['name'] == "https-alt":
            srv['proto'] = "https://"
            srv['ipaddr'] = host['ipaddr']
            srv['port'] = host['port']
            found = True

        if found:
            web.append(srv)
    return web


def goSpideURL(domain, target):

    # here, we can set burpsuite as our proxy so the crawling phase can feed the sitemap generation and passive scanning
    # this is designed to help us with further investigation/analysis using burp.
    #
    #########

    # skip when:
    # step 1 - check if we have blank page
    # step 2 - check if we have blocking page
    # step 3 - 301 to different vhost (check if that new vhost is present in .hosts and .webservers file (new sub?) )

    savedir = domain + ".crawler"
    execPhoton(target, savedir)
    found = parsePhoton(target, savedir)

    return found

def getWebserversRawFile(domain):
    with open(domain + ".webservers", "r") as f:
        content = f.readlines()
    return content


def checkWebDefault():

    files = os.listdir("teste-nginx/screens/")

    for fname in sorted(files):
        if os.path.isfile("./teste-nginx/screens/"+fname):
            image = cv2.imread("./teste-nginx/screens/"+fname)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            filename = "/var/tmp/{}.png".format(os.getpid())
            cv2.imwrite(filename, gray)
            text = pytesseract.image_to_string(Image.open(filename))
            #print(text)
            points=0

            for str in iisdefault:
                if str in text:
                    points+=1

            if points == len(iisdefault):
                print "IIS DEFAULT PAGE FOUND"

            points = 0
            for str in nginxdefault:
                if str in text:
                    points+=1

            if points == len(nginxdefault):
                print "Ngnix Found"

            points = 0
            for str in apachedefault:
                if str in text:
                    points+=1

            if points == len(apachedefault):
                print "Apache server Found"

            points = 0
            for str in apachedebian:
                if str in text:
                    points+=1

            if points == len(apachedebian):
                print "Apache debian Found"

            points = 0
            for str in apacheubuntu:
                if str in text:
                    points+=1

            if points == len(apacheubuntu):
                print "Apache Ubuntu Found"


            os.remove(filename)
        else:
            print "nao eh arquivo??"