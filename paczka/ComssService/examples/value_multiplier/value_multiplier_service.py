#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.service.sync import SyncService
from ComssService.ServiceController import ServiceController

class MultiplierService(SyncService):

    def run(self):
        while True:  # będzie się wykonywać tak długo, jak będzie działać usługa
            received_dict = self.read_object('1')  # odczytaj wejsciowy slownik
#             print 'GOT:', received_dict
            curr_params = self.get_parameters()
            value_to_multiply = curr_params['value_to_multiply']
            if value_to_multiply in received_dict:
                received_dict[value_to_multiply] *= curr_params['multiply_by']


            self.send_object('2', received_dict)  # na wyjście o id '2' wyślij przetworzony slownik

if __name__ == '__main__':
    # Uruchomienie usługi:
    desc_file_name = 'value_multiplier_service.xml'
    s = ServiceController(MultiplierService, desc_file_name)
    s.start()

    # teraz wystarczy w kosoli uruchomić ten skrypt, aby usługa zaczęła działać
