#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.service.sync import SyncService
from ComssService.ServiceController import ServiceController
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
from color import bcolors
import time
import sys
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
    print bcolors.UNDERLINE + 'TRWA: Pobieranie słów kluczowych z treści' + bcolors.ENDC
    link = url.replace('details', 'content')

    content = urllib2.urlopen(link).read()
    soup = BeautifulSoup(content)
    soup2 = BeautifulSoup(content)
    for soup in soup.find_all(text=re.compile("^(art.) ([0-9]{1,4})")):
        dataArt.append(soup.encode('utf-8'))

    for date in soup2.find_all(text=re.compile("^([0-9]{1,2} [a-z]* [0-9]{4})")):
        dataDate.append(date.encode('utf-8'))

    # for price in soup.find_all(text=re.compile("^(?:\d*\.[0-9]{3} zł)|(?:\d*\.[0-9]{3},[0-9]{2} zł)")):
    #     dataPrice.append(price)

def getMetricDataFromLink(url):
    print bcolors.UNDERLINE + 'TRWA: Pobieranie danych z metryki' + bcolors.ENDC
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

def getAllLinksFromRss(rss):
    print bcolors.UNDERLINE + 'TRWA: Pobieranie linków z kanału RSS' + bcolors.ENDC
    feed = feedparser.parse(rss)
    for key in feed["items"]:
        links.append(key['link'])

def checkExistLinkInDatabase():
    print bcolors.UNDERLINE + 'TRWA: Sprawdzanie czy linki znajdują się już w bazie' + bcolors.ENDC
    for key in links:
        exist = MetaData.select().where(MetaData.links == key)
        if not exist.exists():
            linksNew.append(key)


class Preprocess(SyncService):

    def run(self):
        while True:  # będzie się wykonywać tak długo, jak będzie działać usługa
            rss = self.read('1')  # odczytaj dane z wejścia '1'. Nie przejmuj się ilością - jak tylko coś jest, to odczytaj
            getAllLinksFromRss(rss);
            checkExistLinkInDatabase()


            # pprint.pprint(linksNew)

            if linksNew:
                for linkurl in linksNew:

                    url = linkurl


                    getContentDataFromUrl(url)

                    artDup = list(set(dataArt))
                    dateDup = list(set(dataDate))

                    rssId =  Rss.select().where(Rss.link == rss).get()

                    metric = getMetricDataFromLink(url)

                    title = ''
                    date_of_judgment = ''
                    date_publication = ''
                    signature = ''
                    judgement_name = ''
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
                            rss = rssId.idrssFeed
                        )
                        judgmentResult = Judgment.create(
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
                            cities = rssId.idrssFeed
                        )


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

                        self.send('2', "Dane zostały poprawnie zapisane w bazie danych")  # na wyjście o id '2' wyślij przetworzone dane

                    except:
                        raise
            else:
                print bcolors.OKBLUE + 'Brak linków lub wszystkie linki zostały dodane' + bcolors.ENDC


if __name__ == '__main__':
    # Uruchomienie usługi:
    desc_file_name = 'preprocess.xml'
    s = ServiceController(Preprocess, desc_file_name)
    s.start()

