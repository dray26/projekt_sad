#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import socket
import json

class ServiceCommunicationWatcherThread(threading.Thread):
    def __init__(self, handler):
        threading.Thread.__init__(self)
        self.daemon = True
        self.handler = handler
        self.host = self.handler.update_params_host

    def do_method_update_params(self, **kwargs):
        self.handler.update(kwargs)
        return self.handler.get_parameters()

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((self.host.split(':')[0], int(self.host.split(':')[1])))
            while True:
                s.listen(1)
                new_conn, addr = s.accept()
                file_like = new_conn.makefile()
                d = file_like.readline()
                self.handler.update(json.loads(d))
        except:
            raise
        finally:
            s.close()