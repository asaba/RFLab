'''
Created on 26/mag/2016

@author: sabah
'''

import serial
import time


class USBInstrument():
    def __init__(self, comport, baudrate=9600, timeout=5000):
        if comport:
            self.serialport = self.createserialport(comport, baudrate, timeout)
        else:
            print("Error on serial port")

    def createserialport(self, comport, baudrate, timeout):
        # return serialport for comunication
        if type(timeout) is str or type(timeout) is unicode:
            eval_timeout = eval(timeout)
        else:
            eval_timeout = timeout
        eval_timeout = eval_timeout / 1000
        return serial.Serial(port=comport, baudrate=baudrate, timeout=eval_timeout)

    def openport(self):
        if not self.serialport.isOpen():
            self.serialport.open()

    def closeport(self):
        try:
            self.serialport.close()
        except:
            pass


class USB_PM5(USBInstrument):
    # Extention to USB instrument for PM5 Power meter
    # ask to E1? command
    def __init__(self, comport, baudrate=9600, timeout=5000):
        USBInstrument.__init__(self, comport=comport, baudrate=baudrate, timeout=timeout)

    def write(self, command):
        if command == "E1?":
            try:
                self.serialport.openport()
            except:
                pass
            # a = self.serialport.IsOpen()
            # if a == False:
            #    self.serialport.openport()
            # Command to ask value in exponential format
            try:
                self.write_hr(38, 1, 2, 37)
            except:
                pass
        elif command == "?VC":
            self.write_3(b"?", b"V", b"C", chr(0), chr(0), chr(0), chr(0))
        elif command == "?D1":
            self.write_3(b"?", b"D", b"1", chr(0), chr(0), chr(0), chr(0))

    def read(self):
        # time.sleep(1)
        try:
            line = self.serialport.read(6)
            if ord(line[0]) == 171:
                line = line + self.serialport.read(14 - 6)
                print("Comunication Error 171 (0xAB)")
                return "0"
            elif ord(line[0]) == 85:
                line = line + self.serialport.read(14 - 6)
                return line[1:]
            else:
                return line

        except:
            print("read: Error reading from serial")
            return "0"

    def ask(self, command):
        self.write(command)
        time.sleep(1)
        result = self.read()
        self.closeport()
        return result

    def write_bytes(self, *args):
        if len(args) == 7:
            self.write_3(*args)
        elif len(args) == 4:
            self.write_hr(*args)

    def write_3(self, value_0, value_1, value_2, value_3=chr(0), value_4=chr(0), value_5=chr(0), value_6=chr(0)):
        self.serialport.write(value_0)
        self.serialport.write(value_1)
        self.serialport.write(value_2)
        self.serialport.write(value_3)
        self.serialport.write(value_4)
        self.serialport.write(value_5)
        self.serialport.write(value_6)
        self.serialport.write(b"\r")

    def write_hr(self, value_0, value_1, value_2, value_3):
        self.serialport.write(chr(value_0))
        self.serialport.write(chr(value_1))
        self.serialport.write(chr(value_2))
        self.serialport.write(chr(value_3))
