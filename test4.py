#!/usr/bin/env python
# -*- coding: utf-8 -*-


import feedparser

from peewee import *
from project.models import Rss
import nltk
from bs4 import BeautifulSoup
import urllib2





url = "http://orzeczenia.bialystok.sa.gov.pl/details/$N/150500000000503_I_ACa_000600_2014_Uz_2014-12-12_002"
content = urllib2.urlopen(url).read()

soup = BeautifulSoup(content)

for soup in soup.find_all('dd'):
    print(soup.get_text())


# when you're ready to start querying, remember to connect
#
# rss = 'http://orzeczenia.piotrkow-tryb.so.gov.pl/rsscontent/15050000'
# # for pet in Rss.select():
# #     rss = pet.link
# feed = feedparser.parse(rss)
# for key in feed["items"]:
#     metric = key['link']
#
# print (metric+'\n')
# response = urllib2.urlopen(metric)
# html = response.read()
#
# print(html)