#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController

desc_file_name = 'value_multiplier_service.xml'

controller = DevServiceController(desc_file_name)
try:
    while True:
        print controller.read_object('2')
except:
    pass
finally:
    controller.close_all_connections()