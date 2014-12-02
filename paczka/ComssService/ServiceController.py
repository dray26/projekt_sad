#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import signal
import os
from xml.dom.minidom import parse
import json

class ServiceController(object):
    def __init__(self, service_class, desc_path):
        self.service_class = service_class
        self.desc_path = desc_path

    def __getText(self, nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc).strip()

    def __get_value_from_node(self, node, tag_name):
        return self.__getText(node.getElementsByTagName(tag_name)[0].childNodes)

    def read_desc_from_xml(self):
        dom = parse(self.desc_path)
#         address = self.__getText(dom.getElementsByTagName('address')[0].childNodes)
        input_formats = {}

        inputs_dom = dom.getElementsByTagName('inputs')
        if inputs_dom:
            for input_dom in inputs_dom[0].getElementsByTagName('input'):
                input_formats[self.__get_value_from_node(input_dom, 'id')] = self.__get_value_from_node(input_dom, 'name')

        output_formats = {}
        outputs_dom = dom.getElementsByTagName('outputs')
        if outputs_dom:
            for output_dom in outputs_dom[0].getElementsByTagName('output'):
                output_formats[self.__get_value_from_node(output_dom, 'id')] = self.__get_value_from_node(output_dom, 'name')

        return input_formats, output_formats

    def read_from_json(self):
        json_path = self.desc_path.rsplit('.')[0] + '.json'
        with open(json_path, 'r') as f:
            return json.load(f)

    def start(self):
        input_formats, output_formats = self.read_desc_from_xml()

        json_data = self.read_from_json()
        inputs_dict = json_data.get('inputs', {})
        outputs_dict = json_data.get('outputs', {})
        params = json_data.get('parameters', {})
        update_host = json_data.get('dev_communication_address', '127.0.0.1:0')

        inputs = {}
        for input_id in inputs_dict:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((inputs_dict[input_id].split(':')[0], int(inputs_dict[input_id].split(':')[1])))  # 0 takes free port
            s.listen(1)
            inputs[input_id] = (input_formats[input_id], s, None, None)

        outputs = {}
        for output_id in outputs_dict:
            outputs[output_id] = (output_formats[output_id], outputs_dict[output_id])

        service = self.service_class('development', inputs, outputs, params, update_host)
        try:
            signal.signal(signal.SIGTERM, lambda *args, **kwargs: service._stop())
            service._notify_started()
            service.prepare()
            service.run()
        except:
            raise
        finally:
            try:
                service._stop()
            except:
                pass
