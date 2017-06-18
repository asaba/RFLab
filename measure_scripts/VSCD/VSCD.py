#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  VSCD.py
#  Jul 29, 2015 17:26:37 EDT
#  Copyright 2015
#         
#  Andre Young <andre.young@cfa.harvard.edu>
#  Harvard-Smithsonian Center for Astrophysics
#  60 Garden Street, Cambridge
#  MA 02138
#  
#  Changelog:
#  	AY: Created 2015-07-29

"""
tscpy class for the TSC5120A instrument.
"""

from numpy import loadtxt, array
from re import finditer, search
from StringIO import StringIO
from telnetlib import Telnet, socket
from time import sleep
from utility import create_csv
import datetime
import os


WAIT_AFTER_CONNECT = 2.0
WAIT_AFTER_SEND = 0.1


class VSCD:

    _vscd = None

    @property
    def connected(self):
        return self._connected

    @property
    def last_read(self):
        return self._last_read

    @property
    def socket(self):
        return self._socket

    @property
    def vscd(self):
        return self._vscd

    def __init__(self, host, port):
        self._tc = Telnet(host, port)
        self._socket = (host, port)
        sleep(WAIT_AFTER_CONNECT)
        self._receive()
        # for some reason first send-receive does not work, so dummy
        tmp = self._last_read
        self._show('ADEV')
        if tmp.find('Welcome') == -1:
            self.tc.close()
            self._connected = False
            self._last_read = None
            self._socket = None
            self._tc = None
        else:
            self._show(VSCD.show_params.keys()[0])
            self._connected = True
            self._last_read = tmp

    def write(self, command):
        #send a command to instrument
        #TODO
        command_complete = ""
        command_head = command
        command_tail = self._calculate_control_char(command_head)
        command_complete = command_head + command_tail
        self._send(command_complete)
        return 0

    def read(self):
        #read last buffer info
        #TODO
        # check control char
        command_complete = self.last_read()
        command_head = command_complete[:-1]
        command_tail = command_complete[-1]
        if command_tail == self._calculate_control_char(command_head):
            # control char is OK
            return command_head
        else:
            return 0

    def ask(self, command):
        self.write(command)
        sleep(WAIT_AFTER_CONNECT)
        return self.read()

    def close(self):
        self.vscd.close()
        self._last_read = None

    # raw communication
    def _receive(self):
        try:
            raw_recv = self.vscd.read_very_eager()
            suffix_remove_str = '\r=' + self.socket[0] + ' > '
            idx_suffix = raw_recv.find(suffix_remove_str)
            if not idx_suffix == -1:
                raw_recv = raw_recv[:idx_suffix]
            self._last_read = raw_recv
            return self._last_read
        except EOFError:
            return None

    def _send(self, snd):
        try:
            self.tc.write(snd)
            sleep(WAIT_AFTER_SEND)
            return True
        except socket.error:
            return False

    def _calculate_control_char(self, command):
        #TODO
        result = 0
        for index in range(0, len(command)):
            result += command[index]
        return result

    # user-interface, get different things
    def get_freq(self):
        command = "{ATT"
        result = self.ask(command)
        return result

    def get_att(self):
        command = "{ATT"
        result = self.ask(command)
        return result

    def get_rf_status(self):
        command = "{ATT"
        result = self.ask(command)
        return result

    def set_att(self, value):
        command = "{ATT" + value
        self.write(command)

    def set_freq(self, value):
        command = "{ATT" + value
        self.write(command)

    def set_rf_status(self, value):
        command = "{ATT" + value
        self.write(command)
