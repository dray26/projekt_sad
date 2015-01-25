#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.service.sync import SyncService
from ComssService.ServiceController import ServiceController

class LowerService(SyncService):

    def run(self):
        while True:  # będzie się wykonywać tak długo, jak będzie działać usługa
            data = self.read('1')  # odczytaj dane z wejścia '1'. Nie przejmuj się ilością - jak tylko coś jest, to odczytaj
            self.send('2', data.lower())  # na wyjście o id '2' wyślij przetworzone dane

if __name__ == '__main__':
    # Uruchomienie usługi:
    desc_file_name = 'lower_service.xml'
    s = ServiceController(LowerService, desc_file_name)
    s.start()

