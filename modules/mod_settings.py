#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

IPV4_REGEX='^([0-9]{1,3}\.){3}[0-9]{1,3}(\/([0-9]|[1-2][0-9]|3[0-2]))?$'

DOCUMENT_ROOT="/var/www/html"

CPPATH=""

# strings for webserver identification (default pages):


iis = ["internet information services","Welcome","Bienvenido","Willkommen", "Bem-vindo", "Bienvenue", "Benvenuto", "Welkom"]
nginx = ["Welcome to nginx!", "see this page","the nginx web server","successfully installed", "Further configuration is required", "Thank you for using nginx"]
apache_old = ["It works!","This is the default web page for this server.","The web server software is running but no content has been added, yet."]
apache_new = ["Apache2","Default Page","It works!","replace this file","apache2","default configuration","mods-enabled"]


# credits and reference: https://github.com/zigoo0/JSONBee
known_jsonp_endpoints = '''
a.sm.cn
accounts.google.com
ads.pictela.net
ads.yap.yahoo.com
adss.yahoo.com
fe3.cbs.vip.gq1.yahoo.com
adserver.adtechus.com
ajax.googleapis.com
api-metrika.yandex.ru
api.cmi.aol.com
api.m.sm.cn
api.mixpanel.com
api.userlike.com
api.vk.com
app-e.marketo.com
app-sjint.marketo.com
appcenter.intuit.com
bebezoo.1688.com
count.tbcdn.cn
cse.google.com
detector.alicdn.com
googleads.g.doubleclick.net
m.addthis.com
mkto.uber.com/
passport.ngs.ru
portal.pf.aol.com
search.twitter.com
suggest.taobao.com
translate.yandex.net
twitter.com
ui.comet.aol.com
ulogin.ru
wb.amap.com
www.aol.com
www.blogger.com
www.google.com
www.googleadservices.com
www.meteoprog.ua
www.sharethis.com
www.travelpayouts.com
www.youku.com
'''