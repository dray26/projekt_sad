#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import sys

desc_file_name = 'preprocess.xml'
controller = DevServiceController(desc_file_name)
try:
    while True:
        sys.stdout.write(controller.read_data('2', 1024))
        sys.stdout.flush()
except:
    raise
finally:
    controller.close_all_connections()