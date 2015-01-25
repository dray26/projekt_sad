#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.service.sync import SyncService
from ComssService.ServiceController import ServiceController
from bs4 import BeautifulSoup
import urllib2
import feedparser
from peewee import *
from models import Cities
from models import Judgment
from models import JudgmentData
from models import JudgmentType
from models import MetaData
from models import Rss
from models import Statistic

def getAllLinksFromRss(rss):
    feed = feedparser.parse(rss)
    links = []
    for key in feed["items"]:
        links.append(key['link'])


class Preprocess(SyncService):

    def run(self):
        while True:  # będzie się wykonywać tak długo, jak będzie działać usługa
            data = self.read('1')  # odczytaj dane z wejścia '1'. Nie przejmuj się ilością - jak tylko coś jest, to odczytaj
















            self.send('2', data.upper())  # na wyjście o id '2' wyślij przetworzone dane

if __name__ == '__main__':
    # Uruchomienie usługi:
    desc_file_name = 'preprocess.xml'
    s = ServiceController(Preprocess, desc_file_name)
    s.start()

