#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import time
import sys
import json
import os
from threading import RLock
from ComssService.service.utils import ServiceCommunicationWatcherThread

# if you catch one of these errors, beware - services can be screwed up, but try again - maybe just connections problems
SOCKET_ERRORS_TO_RETRY = [9, 32, 104, 109, 111]
# if you catch one of these errors, its ok - just coninue
SOCKET_ERRORS_TO_PASS = [4]

global instance_logger

class DevEncoding(object):
    def __init__(self):
        self.encode = json.dumps
        self.decode = json.loads

class SyncService(object):

    FILES_DIR = '/tmp/comss'
    LOGS_DIR = '/tmp/comss/log'
    SEND_TRY_INTERVAL = 3
    MAX_SEND_RETRIES = 10
    SEND_TIMEOUT = 10
    READ_TRY_INTERVAL = 3
    MAX_READ_RETRIES = 10
    SOCKET_TIMEOUT = 20
    in_encoding = 'json'
    out_encoding = 'json'
    buffer = 4096
    watch_input = True

    def __init__(self, instance_id, inputs, outputs, exec_params, update_params_host, *args, **kwargs):
        self.__update_params_lock = RLock()
        self.__parameters_lock = RLock()
        self.__stopped = False
        self.instance_id = instance_id
        self.inputs = inputs
        self.outputs = outputs
        self.__sockets = {}
        self.__parameters = self.format_params(exec_params)

        self.__in_encoder = DevEncoding()
        self.__out_encoder = DevEncoding()

        self.update_params_host = update_params_host
        self.__service_communication_watcher = ServiceCommunicationWatcherThread(self)

    def format_params(self, params):
        return params

    def __prepare_read(self, input_id):
        input_format, socket, conn, file_like = self.inputs[input_id]
        if not conn:
            socket.listen(1)
            c = socket.accept()
            new_conn, addr = c
            conn = new_conn
            self.inputs[input_id] = (input_format, socket, conn, conn.makefile())

    def __get_conn(self, input_id):
        self.__prepare_read(input_id)
        input_format, socket, conn, as_file = self.inputs[input_id]
        return conn

    def __get_file_like_conn(self, input_id):
        self.__prepare_read(input_id)
        input_format, socket, conn, as_file = self.inputs[input_id]
        return as_file

    def __read(self, input_id, buff=None):
        if buff is None:
            buff = SyncService.buffer
        conn = self.__get_conn(input_id)
        msg = conn.recv(buff)
        return msg

    def __clear_sockets(self, input_id):
        input_format, socket, _, _ = self.inputs[input_id]
        self.inputs[input_id] = (input_format, socket, None, None)
        time.sleep(self.READ_TRY_INTERVAL)

    def read(self, input_id, buff=None):
        counter = self.MAX_READ_RETRIES
        while True:
            try:
                read_buffer = self.__read(input_id, buff)
            except Exception as e:
                if not e.errno in SOCKET_ERRORS_TO_RETRY or counter <= 0:
                    raise e
                counter -= 1
                self.__clear_sockets(input_id)
            else:
                if not read_buffer:
                    counter -= 1
                    self.__clear_sockets(input_id)
                else:
                    return read_buffer

    def __read_raw_msg(self, input_id):
        file_like = self.__get_file_like_conn(input_id)
        msg = file_like.readline()
        return msg

    def read_raw_msg(self, input_id):
        counter = self.MAX_READ_RETRIES
        while True:
            try:
                read_buffer = self.__read_raw_msg(input_id)
            except Exception as e:
                __errno = getattr(e, 'errno', None)
                if __errno is  None:
                    raise
                elif __errno in SOCKET_ERRORS_TO_PASS:
                    continue
                elif not e.errno in SOCKET_ERRORS_TO_RETRY or counter <= 0:
                    raise e
                counter -= 1
                self.__clear_sockets(input_id)
            else:
                if not read_buffer:
                    counter -= 1
                    self.__clear_sockets(input_id)
                else:
                    return read_buffer

    def read_object(self, input_id):
        raw_msg = self.read_raw_msg(input_id)
        return self.__in_encoder.decode(raw_msg)

    def __send(self, output_id, msg):
        if not output_id in self.__sockets:
            output_format, output_addr = self.outputs[output_id]
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            output_ip, output_port = output_addr.split(':')
            s.connect((output_ip, int(output_port)))
            self.__sockets[output_id] = s
        self.__sockets[output_id].send(msg)

    def send(self, output_id, msg):
        counter = self.MAX_SEND_RETRIES
        while True:
            try:
                self.__send(output_id, msg)
            except Exception as e:
                if getattr(e, 'errno', None) is None:
                    raise e
                if not e.errno in SOCKET_ERRORS_TO_RETRY or counter <= 0:
                    raise e
                counter -= 1
                if output_id in self.__sockets:
                    del(self.__sockets[output_id])
                time.sleep(self.SEND_TRY_INTERVAL)
            else:
                break

    def send_raw_msg(self, output_id, msg):
        msg += '\n'
        self.send(output_id, msg)

    def send_object(self, output_id, msg):
        self.send_raw_msg(output_id, self.__out_encoder.encode(msg))

    def _notify_started(self, started_ok=True):
        if started_ok:
            self.__service_communication_watcher.start()

    def __update(self, new_parameters):
        with self.__parameters_lock:
            self.__parameters.update(self.format_params(new_parameters))

    def update(self, new_parameters):
        self.__update(new_parameters)

    def get_parameters(self):
        with self.__parameters_lock:
            return self.__parameters

    def run(self):
        raise NotImplementedError

    def stop(self):
        pass

    def _stop(self):
        if not self.__stopped:
            self.__stopped = True
            self.stop()

    def prepare(self):
        pass
