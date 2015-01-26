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
dataArt = []
dataDate = []
dataPrice = []


def getContentDataFromUrl(url):
    link = url.replace('details', 'content')

    content = urllib2.urlopen(link).read()
    soup = BeautifulSoup(content)
    soup2 = BeautifulSoup(content)
    for soup in soup.find_all(text=re.compile("^(art.) ([0-9]{1,4})")):
        dataArt.append(soup)

    for date in soup2.find_all(text=re.compile("^([0-9]{1,2} [a-z]* [0-9]{4})")):
        dataDate.append(date)

    # for price in soup.find_all(text=re.compile("^(?:\d*\.[0-9]{3} zł)|(?:\d*\.[0-9]{3},[0-9]{2} zł)")):
    #     dataPrice.append(price)

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
    for key in links:
        exist = MetaData.select().where(MetaData.links == key)
        if not exist.exists():
            linksNew.append(key)



rss = 'http://orzeczenia.piotrkow-tryb.so.gov.pl/rsscontent/15200000'

getAllLinksFromRss(rss);
checkExistLinkInDatabase()
url = 'http://orzeczenia.krakow.sa.gov.pl/details/Odszkodowanie/152000000000503_I_ACa_000592_2013_Uz_2014-04-17_001'
getContentDataFromUrl(url)
# pprint.pprint(dataDate)
# pprint.pprint(dataArt)
# pprint.pprint(linksNew)
# print linksNew
# i = 0

for linkurl in linksNew:

    url = linkurl
    rssId = 0

    getContentDataFromUrl(url)

    artDup = list(set(dataArt))
    dateDup = list(set(dataDate))

    rssId =  Rss.select().where(Rss.link == rss).get()

    metric = getMetricDataFromLink(url)

    title = ''
    date_of_judgment = ''
    date_publication = ''
    signature = ''
    judgment_name = ''
    judge = ''
    faculty = ''
    chairman = ''
    recorder = ''
    legal_basis = ''

    for key, val in metric.items():
        if key == "Tytuł:":
            title = val
        elif key == "Data orzeczenia:":
            date_of_judgment = val
        elif key == "Data publikacji:":
            date_publication = val
        elif key == "Sygnatura:":
            signature = val
        elif key == "Sędziowie:":
            judge = val
        elif key == "Sąd:":
            judgement_name = val
        elif key == "Protokolant:":
            recorder = val
        elif key == "Podstawa prawna:":
            legal_basis = val
        elif key == "Przewodniczący:":
            chairman = val
        elif key == "Wydział:":
            faculty = val

    try:

        metadata = MetaData.create(
            links = url,
            rss = rssId
        )

        judgmentResult = Judgment(
            title = title,
            date_of_judgment = date_of_judgment,
            date_publication = date_publication,
            signature = signature,
            judgement_name = judgement_name,
            judges = judge,
            faculty = faculty,
            chairman = chairman,
            recorder = recorder,
            legal_basis = legal_basis,
            metadata = metadata,
            cities = 3
        )

        judgmentResult.save(force_insert=True)
        for tmpArt in artDup:
            keys = Key.create(
                typ = 'art',
                value = tmpArt,
                judgment = judgmentResult,
            )
        for tmpDate in dateDup:
            keys = Key.create(
                typ = 'date',
                value = tmpDate,
                judgment = judgmentResult,
            )
        print 'Wykonało się'
    except:
        raise


# print metric
# getAllLinksFromRss(url)
# checkExistLinkInDatabase(rss)
# print linksNew
