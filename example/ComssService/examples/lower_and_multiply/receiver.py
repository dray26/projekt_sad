#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import random
import time
import os

desc_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../value_multiplier/value_multiplier_service.xml')  # prepare proper absolute path

controller = DevServiceController(desc_file_name)
try:
    while True:
        print controller.read_object('2')
except:
    raise
finally:
    controller.close_all_connections()
