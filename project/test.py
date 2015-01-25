#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
import feedparser
import re
import datetime
import pprint
from peewee import *
from models import Cities
from models import Judgment
from models import Rss
from models import MetaData
from models import Key

detail = []
metric = {}
links = []
linksNew = []
ddarr = []
dtarr = []
art = []


def getContentDataFromUrl(url):
    link = url.replace('details', 'content')

    content = urllib2.urlopen(link).read()
    soup = BeautifulSoup(content)
    for soup in soup.find_all(text=re.compile("^art.")):
        art.append(soup)

    # for soup in soup.find_all(text=re.compile("^[0-9]{1,2}(\.)[0-9]{3}(\,)[0-9]{2}")):
    #     print(soup)

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

def checkExistLinkInDatabase():
    for row in MetaData.select():
        for key in links:
            if row.links != key:
                linksNew.append(key)

rss = 'http://orzeczenia.piotrkow-tryb.so.gov.pl/rsscontent/15200000'

getAllLinksFromRss(rss);
checkExistLinkInDatabase()

# print linksNew

for linkurl in linksNew:

    url = linkurl


    rssId = 0

    getContentDataFromUrl(url)

    for i in Rss.select().where(Rss.link == rss):
        rssId = i.idrssFeed
    metric = getMetricDataFromLink(url)
    title = ''
    chairman = ''
    date_of_judgment = ''
    date_publication = ''
    signature = ''
    judge = ''
    recorder = ''
    legal_basis = ''
    faculty = ''


    for key, val in metric.items():
        if key == "Tytuł:":
            title = val
        elif key == "Data orzeczenia:":
            date_of_judgment = val
        elif key == "Data publikacji:":
            date_publication = val
        elif key == "Sygnatura:":
            signature = val
        elif key == "Sąd:":
            judge = val
        elif key == "Protokolant:":
            recorder = val
        elif key == "Podstawa prawna:":
            legal_basis = val
        elif key == "Przewodniczący:":
            chairman = val
        elif key == "Wydział:":
            faculty = val

    # a = list(set(art))
    #
    # for tmp in a:
    #     print tmp

    try:

        metadata = MetaData.create(
            links = url,
            name = 'name',
            date = datetime.datetime.now(),
            rss = rssId
        )

        judgmentResult = Judgment(
            title = title,
            chairman = chairman,
            date_of_judgment = date_of_judgment,
            date_publication = date_publication,
            signature = signature,
            recorder = recorder,
            legal_basis = legal_basis,
            metadata = 16,
            cities = 3
        )

        judgmentResult.save(force_insert=True)
        # for tmp in art:
        #     keys = Key.create(
        #         typ = 'art',
        #         value = tmp,
        #         judgment = judgmentResult,
        #     )
        print 'Wykonało się'
    except:
        raise


# print metric
# getAllLinksFromRss(url)
# checkExistLinkInDatabase(rss)
# print linksNew
