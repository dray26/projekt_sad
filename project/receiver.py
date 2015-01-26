#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import sys
from color import bcolors



desc_file_name = 'preprocess.xml'
controller = DevServiceController(desc_file_name)
try:
    while True:
        # sys.stdout.write(controller.read_data('2', 1024))
        # sys.stdout.flush()
        print bcolors.OKGREEN + controller.read_data('2', 1024) + bcolors.ENDC
except:
    raise
finally:
    controller.close_all_connections()