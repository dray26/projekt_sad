#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json

# remeber that inputs and outputs from json are reversed
# because we send to input and receive from output

class DevServiceController(object):
    def __init__(self, desc_path):
        self.desc_path = desc_path
        self.out_sockets = {}
        self.in_sockets = {}
        with open(self.get_json_path(), 'r') as f:
            self.json_data = json.load(f)

    def update_params(self, new_params):
        host, port = self.json_data['dev_communication_address'].split(':')
        print host, port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, int(port)))
        s.sendall(json.dumps(new_params) + '\n')
        s.close()

    def get_json_path(self):
        return self.desc_path.rsplit('.', 1)[0] + '.json'

    def get_out_socket(self, out_id):
        if not out_id in self.out_sockets:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = self.json_data['inputs'][out_id].split(':')
            s.connect((host, int(port)))
            self.out_sockets[out_id] = s
        return self.out_sockets[out_id]

    def send_data(self, out_id, data):
        s = self.get_out_socket(out_id)
        s.sendall(data)

    def send_raw_msg(self, out_id, msg):
        self.send_data(out_id, msg + '\n')

    def send_object(self, out_id, msg):
        self.send_raw_msg(out_id, json.dumps(msg))

    def get_in_socket(self, in_id):
        if not in_id in self.in_sockets:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host, port = self.json_data['outputs'][in_id].split(':')
            s.bind((host, int(port)))
            s.listen(1)
            new_conn, addr = s.accept()
            self.in_sockets[in_id] = (new_conn, new_conn.makefile())
        return self.in_sockets[in_id]

    def read_data(self, in_id, buff=1024):
        s, file_like = self.get_in_socket(in_id)
        return s.recv(buff)

    def read_raw_msg(self, in_id):
        s, file_like = self.get_in_socket(in_id)
        return file_like.readline()

    def read_object(self, in_id):
        return json.loads(self.read_raw_msg(in_id))

    def close_all_connections(self):
        for out_id, out_socket in self.out_sockets.iteritems():
            try:
                out_socket.close()
            except:
                pass
        for in_id, (in_socket, in_gile_like) in self.in_sockets.iteritems():
            try:
                in_socket.close()
            except:
                pass
