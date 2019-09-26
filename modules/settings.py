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
