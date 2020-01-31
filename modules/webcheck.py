#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib3
from multiprocessing import Pool
import time
from lxml import html
from PIL import Image
import pytesseract
import cv2
import os
from modules.photon import execPhoton, parsePhoton
from modules.massdns import parseMassdnsStruct
from reppy.robots import Robots
from misc import saveFile
from wappalyzer import execWappalyzer

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse



scrapdata = list()



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

# verificar hostnames nos certificados por ip
# jenkins exploit: finder:
# https://ravirajput.github.io/recon_by_armaanpathan12345/#/9


def FindWebFromList(nmapObj,domain):
    # https://github.com/arbazkiraak/certasset/blob/master/subs_cert.py
    # webgrep https://github.com/LLazarek/webgrep.git")

    massdnsstruct = parseMassdnsStruct(domain)
    webhosts = list()
    for ip in nmapObj.all_hosts():

        vhostlist = getHostnameFromIp(massdnsstruct,ip)
        openports = nmapObj[ip]['tcp'].keys()
        for port in openports:
            service_details = nmapObj[ip]['tcp'][port]
            try:
                if service_details['script']:
                    havetls = True
            except:
                havetls = False
            if havetls and "http" in service_details['name']:
                if port == "443":
                    webhosts.append("https://" + ip + "/")
                else:
                    webhosts.append("https://" + ip + ":" + str(port) + "/")
                if len(vhostlist)>0:
                    for vhost in vhostlist:
                        if port == "443":
                            webhosts.append("https://" + str(vhost) + "/")
                        else:
                            webhosts.append("https://" + str(vhost) + ":" + str(port) + "/")

            if not havetls and "http" in service_details['name']:
                if port == "80":
                    webhosts.append("http://" + ip + "/")
                else:
                    webhosts.append("http://" + ip + ":" + str(port) + "/")
                if len(vhostlist)>0:
                    for vhost in vhostlist:
                        if port == "80":
                            webhosts.append("http://" + str(vhost) + "/")
                        else:
                            webhosts.append("http://" + str(vhost) + ":" + str(port) + "/")

        webhosts = list(set(webhosts))
        saveFile(domain+".web",webhosts)
    return webhosts




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






def ParseWebResponse(urlstruct):
    global scrapdata
    if valid_url is not False:
        '''
        print("  + url: " + str(urlstruct['url']))
        for a in urlstruct['a']:
            print("  + a: " + str(a))
        for js in urlstruct['js']:
            print("  + js: " + str(js))

        print("="*100)
        '''
        scrapdata.append(urlstruct)


def FetchWebContent(url):
    ret = dict()
    try:
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'         # avoid ssl errors
        requests.packages.urllib3.contrib.pyopenssl.extract_from_urllib3()  # avoid ssl errors
        response = requests.get(url, verify=False, timeout=5)               # verify=False avoid ssl errors
        webpage = html.fromstring(response.content)
        ret['url'] = url
        ret['a'] = webpage.xpath('//a/@href')
        ret['js'] = webpage.xpath('//script/@src')
        ret['headers'] = response.headers
        out,err = execWappalyzer(url)
        ret['stack'] = out

    except:
        return False
    else:
        return ret

'''
def ContentSecurityPolicy(urldata):

    for urldata in scrapdata:
        print(str(urldata['url']))
        h = urldata['headers']
        for k, v in h.items():
            if k ==  "Content-Security-Policy" or k == "X-Content-Security-Policy":

'''







def ScrapWeb(webhosts):
    global scrapdata
    urllib3.disable_warnings()
    p = Pool(processes=100)
    for url in webhosts:
        p.apply_async(FetchWebContent, (url,), callback=ParseWebResponse)
    p.close()
    p.join()

    for urldata in scrapdata:
        print(str(urldata['url']))
        h = urldata['headers']
        for k, v in h.items():
            print("  + %s: %s" % (k, v))

        '''
        for a in each['a']:
            print(str(a))
        for js in each['js']:
            print("\t"+str(js))

        '''

    return True






