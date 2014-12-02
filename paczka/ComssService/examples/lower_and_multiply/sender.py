#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import random
import time
import os

desc_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../lower_service/lower_service.xml')  # prepare proper absolute path
controller = DevServiceController(desc_file_name)

def get_random_case(str_val):
    if random.random() > 0.5:
        return str_val.upper()
    else:
        return str_val.lower()

try:
    while True:
        dict_to_send = {get_random_case('a'): random.randint(0, 100),
                        get_random_case('b'): random.randint(0, 100),
                        get_random_case('c'): random.randint(0, 100),
                        }
        controller.send_object('1', dict_to_send)
        print "SENT:", dict_to_send
        time.sleep(0.5)
except:
    raise
finally:
    controller.close_all_connections()
