'''
Created on 29/dic/2015

@author: sabah
'''

import wx, os
from IPy import IP
import pyvisa
from measure_scripts.debug import SMB_class, FSV_class, NRP2_class, TSC_class, SAB_class, PM5_class
from measure_scripts.USBInstruments import USB_PM5
from measure_scripts.tscpy import instruments


def browse_file(parent, text_control_file, dialog_text = "Choose a file", wildcard = "*.csv"):
    defaultFile = ""
    try:
        defaultFile = text_control_file.GetValue()
    except:
        defaultFile = ""
    dlg = wx.FileDialog(parent, dialog_text, os.getcwd(), defaultFile = defaultFile, wildcard = wildcard, style = wx.OPEN)
    if dlg.ShowModal() == wx.ID_OK:
        path = dlg.GetPath()
        #mypath = os.path.basename(path)
        text_control_file.SetValue(path)
    else:
        if os.path.exists(defaultFile):
            text_control_file.SetValue(defaultFile)
        else:
            text_control_file.SetValue("")

def create_instrument(ip, port, timeout, instr_type, TEST_MODE = False, instrument_class = "SMB"):
    if TEST_MODE:
        if instrument_class == "SMB":   
            instrument = SMB_class()
        elif instrument_class == "FSV": 
            instrument = FSV_class()
        elif instrument_class == "NRP2": 
            instrument = NRP2_class()
        elif instrument_class == "TSC": 
            instrument = TSC_class()
        elif instrument_class == "SAB": 
            instrument = SAB_class()
        return instrument
    rm = pyvisa.ResourceManager()
    if instr_type == "SOCKET":        
        instrument = rm.open_resource("TCPIP::{ip}::{port}::SOCKET".format(ip = ip, port = port))
        instrument.write_termination = "\n"
        instrument.read_termination = "\n"
    elif instr_type == "INSTR":
        instrument = rm.open_resource("TCPIP::{ip}::INSTR".format(ip = ip))
    elif instr_type == "TELNET":
        instrument = instruments.TSC5120A(ip, port)
    instrument.timeout = timeout
    return instrument


def create_USB_instrument(com_port, timeout, baudrate, TEST_MODE = False, instrument_class = "PM5"):
    if TEST_MODE:
        if instrument_class == "PM5":   
            instrument = PM5_class()
        return instrument
    instrument = USB_PM5(com_port, eval(baudrate), timeout)
    return instrument

def check_USB_instrument_comunication(instrument_COM, instrument_Timeout, instrument_Baud):
    
    try:
        INST = create_USB_instrument(instrument_COM, instrument_Timeout, instrument_Baud)
        #self.instrument_label.SetLabel(INST.ask("*IDN?"))
        result = INST.ask("?D1")
        #result = INST.ask("E1?")
        #result = INST.ask("?VC")
        INST.closeport()
        return (1, result)
    except:
        return (0, "Comunication Error")

def check_instrument_comunication(instrument_IP, instrument_Port, instrument_Timeout, instrument_type):
    #INST = create_instrument(instrument_IP, instrument_Port, instrument_Timeout, instrument_type)
    #return (1, INST.ask("*IDN?"))
    try:
        INST = create_instrument(instrument_IP, instrument_Port, instrument_Timeout, instrument_type)
        #self.instrument_label.SetLabel(INST.ask("*IDN?"))
        return (1, INST.ask("*IDN?"))
    except:
        #self.instrument_label.SetLabel("Comunication Error")
        return (0, "Comunication Error")

def check_value_is_IP(value, value_text):
    value_invalid = False
    try:
        IP(value)
    except:
        value_invalid = True
    if value_invalid:
        error_message(value_text + " invalid", 'Error "' + value_text + '"')
    return 1

def check_value_min_max(value, value_text, minimum=None, maximum=None):
    
    value_invalid = False
    if value is None:
        value_invalid = True
    elif value == "":
        value_invalid = True
    if not value_invalid and not(minimum is None):
        if eval(value)<= maximum:
            value_invalid = True
    if not value_invalid and not(maximum is None):
        if eval(value)> maximum:
            value_invalid = True
        
    if value_invalid:
        error_message(value_text + " invalid", 'Error "' + value_text + '"')
        return 0
    return 1

def check_steps_count(value_text, minimum, maximum, steps, counter):
    
    value_invalid = False
    if abs(minimum - maximum)/steps >= counter:
        value_invalid = True
    if value_invalid:
        error_message(value_text + " invalid", 'Error "' + value_text + '"')
    return 1

def error_message(body, header):
    dlg = wx.MessageDialog(None, body, header, wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    return 0

def check_value_is_valid_file(value, value_text):
    value_invalid = False
    if value is None:
        value_invalid = True
    elif value == "":
        value_invalid = True
    else: 
        try:
            if not os.path.isfile(value):
                value_invalid = True
        except:
            value_invalid = True
    if value_invalid:
        error_message(value_text + " invalid", 'Error "' + value_text + '"')
    return 1

def check_value_not_none(value, value_text):
    value_invalid = False
    if value is None:
        value_invalid = True
    elif value == "":
        value_invalid = True
    if value_invalid:
        error_message(value_text + " invalid", 'Error "' + value_text + '"')
    return 1
    
def resultError(parent = None):
    dlg = wx.MessageDialog(parent, "Measure Error", 'Measure Error', wx.OK | wx.ICON_ERROR)
    dlg.ShowModal()
    
def resultOK(parent = None):
    dlg = wx.MessageDialog(parent, "Measure completed", 'Measure completed', wx.OK | wx.ICON_INFORMATION)
    dlg.ShowModal()
    