#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import time
from peewee import *
from models import Rss
import time
import sys
from color import bcolors

chars_to_send = 'qwertyQWERTY'

desc_file_name = 'preprocess.xml'
controller = DevServiceController(desc_file_name)
try:
    for key in Rss.select():
        controller.send_data('1', key.link)
        print bcolors.UNDERLINE + "Obiekt:", key.name, " został wysłany" + bcolors.ENDC
        for i in range(100):
            time.sleep(1)
            sys.stdout.write("Opóźnienie:\r%d%%" % i)
            sys.stdout.flush()
except:
    raise
finally:
    controller.close_all_connections()
