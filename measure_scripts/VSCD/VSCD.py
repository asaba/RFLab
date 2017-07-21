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
    def address(self):
        return self._address

    @property
    def vscd(self):
        return self._vscd

    def __init__(self, host, port, device_address=65):
        port = eval(port)
        self._vscd = Telnet(host, port)
        self._socket = (host, port)
        self._address = device_address
        sleep(WAIT_AFTER_CONNECT)
        self._receive()
        # for some reason first send-receive does not work, so dummy
        tmp = self._last_read
        self.valid_command=["EQAA",
                            "EQAB",
                            "EQAC",
                            "ZET",
                            "BSA",
                            "FE",
                            "FA",
                            "FB",
                            "TA",
                            "TB",
                            "QA",
                            "QB",
                            "ID",
                            "VW",
                            "VF",
                            "ZO",
                            "ZA",
                            "DA",
                            "ZR",
                            "ZC",
                            "ZI",
                            "ZB",
                            "ZW",
                            "ZP",
                            "ZT",
                            "ZD",
                            "ZG",
                            "ZJ",
                            "ZF",
                            "EA",
                            "EE",
                            "EC",
                            "QT",
                            "SA",
                            "QS",
                            "G",
                            "J",
                            "A",
                            "B",
                            "F",
                            "I",
                            "T",
                            "C",
                            "M",
                            "U",
                            "X",
                            "Y",
                            "Q",
                            "N",
                            "O",
                            "S",
                            "R"]
        self.error_code = ["a", "b", "c", "g"]
        self._connected = True
        self._last_read = tmp

    def write(self, command_and_param):
        # send a command to instrument
        # The command is Header + device address + command code + parameters + Trailer + Checksum
        # TODO
        command_header = "{"
        command_address = chr(self.address)
        command_code_and_param = command_and_param
        command_trailer = "}"
        command_to_check = command_header + command_address + command_code_and_param + command_trailer
        command_checksum = self._calculate_control_char(command_to_check)
        command_complete = command_to_check + command_checksum
        self._send(command_complete)
        return 0

    def read(self):
        # read last buffer info
        # The response is Header + device address + OP  Code or Error code + response value + trailer + checksum
        # return the tuple (string of command, string of value or None)
        # check control char
        self._receive()
        command_complete = self.last_read
        if len(command_complete) < 5:
            # response too short
            return None, None
        checksum = command_complete[-1]
        if checksum != self._calculate_control_char(command_complete[:-1]):
            return None, None
        command_head = command_complete[0] #must be "{"
        if command_head != "{":
            return None, None
        command_address = command_complete[1]  # must be equal to chr(self.address)
        if command_address != chr(self.address):
            return None, None
        if command_complete[2] in self.error_code:
            return None, None
        command_trailer = command_complete[-2] # must be "}"
        if command_trailer != "}":
            return None, None
        for cmd in self.valid_command:
           if command_complete[2:].startswith(cmd):
               # the OPCODE is Valid
                if len(command_complete) == len(command_head) + len(command_address) + len(cmd) + len(command_trailer) + len(checksum):
                    # no value in response
                    value = None
                else:
                    value = command_complete[len(command_head) + len(command_address) + len(cmd) : -2]
                break
        return cmd, value

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
            # read all in output
            raw_recv = self.vscd.read_very_eager()
            self._last_read = raw_recv
            return self._last_read
        except EOFError:
            return None

    def _send(self, snd):
        try:
            self.vscd.write(snd)
            sleep(WAIT_AFTER_SEND)
            return True
        except socket.error:
            return False

    def _calculate_control_char(self, command):
        total = 0
        for index in range(0, len(command)):
            total += ord(command[index]) - 32
        result = total % 95 + 32
        return chr(result)

    # defined commands
    def get_ID(self):
        command = "ID"
        result = self.ask(command)
        return result

    def get_temp_fp(self):
        command = "QT1"
        result = self.ask(command)
        return result

    def get_temp_ctrl(self):
        command = "QT2"
        result = self.ask(command)
        return result

    def get_temp_board(self):
        command = "QT3"
        result = self.ask(command)
        return result

    def get_temp_synt(self):
        command = "QT4"
        result = self.ask(command)
        return result

    def get_freq(self):
        #frequency in Hz
        command = "FE?"
        result = self.ask(command)
        return result

    def get_att(self):
        command = "T?"
        result = self.ask(command)
        return result

    def get_rf_status(self):
        command = "M?"
        result = self.ask(command)
        return result

    def set_freq(self, value):
        #set frequency in Hz
        command = "FE" + value
        self.write(command)

    def set_att(self, value):
        command = "T" + value
        self.write(command)

    def set_rf_on(self):
        command = "U"
        self.write(command)

    def set_rf_off(self):
        command = "M"
        self.write(command)

