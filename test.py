#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import re

html_page = urllib2.urlopen("http://orzeczenia.wroclaw.sa.gov.pl/rsscontent/15500000")
soup = BeautifulSoup(html_page)
for link in soup.findAll('a'):
    print link.get('href')
