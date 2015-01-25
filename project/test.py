#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import feedparser
import re
import pprint
from peewee import *
from models import Cities
from models import Judgment
from models import Judgment_Data
from models import Rss
from models import MetaData
from models import Statistic

detail = []
metric = {}
links = []
linksNew = []
ddarr = []
dtarr = []

def getContentDataFromUrl(url):
    link = url.replace('details', 'content')

    content = urllib2.urlopen(link).read()
    soup = BeautifulSoup(content)
    # for soup in soup.find_all(text=re.compile("^art.")):
    #     print(soup)

    for soup in soup.find_all(text=re.compile("^[0-9]{1,2}(\.)[0-9]{3}(\,)[0-9]{2}")):
        print(soup)

def getMetricDataFromLink(url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    dd = soup.find_all('dd')
    dt = soup.find_all('dt')

    for ddTmp in dd:
        ddarr.append(ddTmp.get_text().encode('utf-8'))
    for dtTmp in dt:
        dtarr.append(dtTmp.get_text().encode('utf-8'))
    resultMetric = dict(zip(dtarr, ddarr))
    return resultMetric

    # for key, val in resultMetric.items():
    #     if key == "Przewodniczący:":
    #         print val

def getAllLinksFromRss(rss):
    feed = feedparser.parse(rss)
    for key in feed["items"]:
        links.append(key['link'])

def checkExistLinkInDatabase(link):
    for row in MetaData.select():
        for key in links:
            if row.links != key:
                linksNew.append(key)


























rss = 'http://orzeczenia.wroclaw.sa.gov.pl/details/odszkodowanie/155000000000503_I_ACa_000787_2013_Uz_2013-09-18_001'

url = 'http://orzeczenia.piotrkow-tryb.so.gov.pl/rsscontent/15050000'
# feed = feedparser.parse(rss)
getContentDataFromUrl(rss)
try:
    judgment_data = Judgment_Data.create(
        name="Rejonowy"
    )
    metadata = MetaData.create(
        links='test',
        rss = 2
    )
    judgmentData = Judgment(
        title = 'title',
        chairman = 'chairman',
        date_of_judgment = 'chairman',
        date_publication = 'chairman',
        signature = 'chairman',
        judges = 'chairman',
        recorder = 'chairman',
        legal_basis = 'chairman',
        judgmentdata = judgment_data,
        metadata = metadata,
        cities = 3
    )

    judgmentData.save(force_insert=True)
except:
    raise

# metric = getMetricDataFromLink(rss)
#
# for key, val in metric.items():
#     if key == "Przewodniczący:":
#         print val
# print metric
# getAllLinksFromRss(url)
# checkExistLinkInDatabase(rss)
# print linksNew
