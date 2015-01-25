#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import random
import time

chars_to_send = 'qwertyQWERTY'

desc_file_name = 'lower_service.xml'
controller = DevServiceController(desc_file_name)
try:
    while True:
        char = random.choice(chars_to_send)
        controller.send_data('1', char)
        print "SENT:", char
        time.sleep(0.5)
except:
    raise
finally:
    controller.close_all_connections()
