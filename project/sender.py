#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import time
from peewee import *
from models import Rss


chars_to_send = 'qwertyQWERTY'

desc_file_name = 'preprocess.xml'
controller = DevServiceController(desc_file_name)
try:
    for key in Rss.select():
        controller.send_data('1', key.link)
        print "SENT:", key.link
        time.sleep(0.5)
except:
    raise
finally:
    controller.close_all_connections()
