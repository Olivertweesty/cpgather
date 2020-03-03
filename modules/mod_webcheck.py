#!/usr/bin/env python
# -*- coding: utf-8 -*-
from modules.mod_massdns import parseMassdnsStruct
from modules.mod_wappalyzer import execWappalyzer
from modules.misc import sort_uniq
import concurrent.futures
import requests
from urllib3.exceptions import InsecureRequestWarning
import json
from bs4 import BeautifulSoup
try:
    from urllib import unquote
except:
    from urllib.parse import unquote



web_service_names = ["http","http-proxy","https","https-alt","ssl"]

def getHostnameFromIp(massdnsstruct,ip):
    host_ips = list()
    for node in massdnsstruct:
        if str(node['ipaddr'].rstrip()) == str(ip.rstrip()):
            host_ips.append(str(node['vhost'].rstrip()))
    return host_ips

def FindWeb(domain, nmapObj):
    weblist = list()
    massdnsstruct = parseMassdnsStruct(domain)

    for ip in nmapObj.all_hosts():
        vhostlist = getHostnameFromIp(massdnsstruct, ip)
        openports = nmapObj[ip]['tcp'].keys()
        for port in openports:
            service_details = nmapObj[ip]['tcp'][port]
            for wtag in web_service_names:
                if wtag == service_details['name']:
                    proto = "http"
                    if service_details['name'] == 'ssl' \
                            or 'https' in service_details['name'] \
                            or service_details['tunnel'] == "ssl":
                        proto = "https"

                    if len(vhostlist) > 0:
                        for vhost in vhostlist:
                            weblist.append(proto + "://" + vhost + ":" + str(port))
                    else:
                        weblist.append(proto + "://" + ip + ":" + str(port))

    weblist = sort_uniq(weblist)
    return weblist


'''
    list(
        url: string
        headers: string
        js: list
        ahref: list
        applications: dict
    )

'''
def wappFormat(wappObj):
    final_content = list()
    for each in wappObj:
        js = list()
        ahref = list()
        a = dict()
        scripts = dict()
        new_data = dict()
        wappjson = json.loads(each['stack'][0])

        try:
            if each['a']:
                havelinks = True
        except:
            havelinks = False

        try:
            if each['js']:
                havejs = True
        except:
            havejs = False

        if havelinks:
            for item in each['a']:
                item = item.replace(" ", '')
                item = item.replace("\n", '')
                if '%' in item:
                    item = unquote(str(item))
                if "javascript:void(0)" in item:
                    continue
                if "#" == item:
                    continue
                if "//" in item:
                    ahref.append(item)
                a['href'] = ahref

        if havejs:
            for item in each['js']:

                item = item.replace(" ", '')
                item = item.rstrip()
                if '%' in item:
                    item = unquote(str(item))
                if "javascript:" in item:
                    continue
                if "#" == item:
                    continue
                if item not in js:
                    js.append(item)
                scripts["js"] = js

        for k, v in wappjson['urls'].items():
            k = k.rstrip('/')
            if k == each['url']:
                new_data['url'] = each['url']
                new_data['status'] = each['status']
                # iplist=getAllipsFor(k)
                new_data['ips'] = k
                new_data['headers'] = dict(each['headers'])

                if len(a) > 0:
                    new_data['ahref'] = a['href']
                else:
                    new_data['ahref'] = a

                if len(scripts) > 0:
                    new_data['js'] = scripts['js']
                else:
                    new_data['js'] = scripts

                wappalyzer_result = wappjson.get('applications')
                if len(wappalyzer_result) > 0:
                    wapp = list()

                    for item in wappalyzer_result:
                        witem = dict()
                        witem['name'] = str(item['name'])
                        witem['version'] = str(item['version'])
                        witem['confidence'] = str(item['confidence'])
                        wapp.append(witem)

                    new_data['applications'] = wapp
                else:
                    new_data['applications'] = list(dict())

                final_content.append(dict(new_data))

    return final_content

def getUrl(url,timeout):
    ret=dict()
    ahr=list()
    jsf=list()
    url=url.rstrip()
    r = requests.get(url, timeout=timeout, verify=False)
    soup = BeautifulSoup(r.content, features="lxml")
    ret['url'] = url
    ret['status'] = r.status_code
    scripts = soup.find_all("script")
    for tag in scripts:
        try:
            jsf.append(tag['src'])
        except:
            pass
        else:
            ret['js'] = jsf

    links = soup.find_all("a")
    for tag in links:
        try:
            ahr.append(tag['href'])
        except:
            pass
        else:
            ret['a'] = ahr

    ret['headers'] = r.headers
    ret['stack'] = execWappalyzer(url)

    return ret

def RetrieveWebContent(urls):
    list_of_webstack = list()
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
    # We can use a with statement to ensure threads are cleaned up promptly
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Start the load operations and mark each future with its URL
        future_to_url = { executor.submit(getUrl, url, 60): url for url in urls }
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                wp = future.result()
            except Exception as exc:
                pass # just pass
            else:
                list_of_webstack.append(dict(wp))
    return list_of_webstack