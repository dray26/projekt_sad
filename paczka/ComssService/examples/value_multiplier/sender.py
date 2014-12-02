#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ComssService.dev.control import DevServiceController
import random
import time

desc_file_name = 'value_multiplier_service.xml'
controller = DevServiceController(desc_file_name)

UPDATE_PARAMS_INTERVAL = 20

try:
    iters_to_update = UPDATE_PARAMS_INTERVAL
    while True:
        iters_to_update -= 1
        if iters_to_update <= 0:
            new_params = {'multiply_by':random.randint(0, 3),
                          'value_to_multiply': random.choice(['a', 'b', 'c'])}
            controller.update_params(new_params)
            print 'PARAMS UPDATED', new_params
            iters_to_update = UPDATE_PARAMS_INTERVAL

        dict_to_send = {'a': random.randint(0, 100),
                        'b': random.randint(0, 100),
                        'c': random.randint(0, 100),
                        }
        controller.send_object('1', dict_to_send)
        print "SENT:", dict_to_send
        time.sleep(0.5)
except:
    raise
finally:
    controller.close_all_connections()
