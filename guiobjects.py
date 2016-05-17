'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os
from utility import unit_class

unit_tmp = unit_class()

def return_file_browse(parent, label):
    """
    return a sizer:
    --------------------------------------
    | label     | textcontrol | button   |
    --------------------------------------
    label text is label
    button text is "..."
    
    return also the textcontrol object and the button object
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size = (150,-1))
    txt = wx.TextCtrl(parent, wx.ID_ANY)
    button = wx.Button(parent, 0, "...")
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(txt, 0, wx.ALL, 5)
    Sizer.Add(button, 0, wx.ALL, 5)
    return txt, button, Sizer

def return_simple_button(parent, label, button_txt):
    """
    return a sizer
    --------------------------
    | label    |  button     |
    --------------------------
    label text is label 
    button text is button_text
    
    return also the button object
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size = (150,-1))
    button = wx.Button(parent, 0, button_txt)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(button, 0, wx.ALL, 5)
    return button, Sizer

def return_test_instrument(parent):
    """
    return sizer
    --------------------
    | button  | label  |
    --------------------
    button test is "Test comunication"
    label text is "..."
    
    return button object and label object
    label object is used to write the response from instrument
    """
    
    button = wx.Button(parent, 0, "Test comunication")
    label = wx.StaticText(parent, wx.ID_ANY, "...", size = (150,-1))
   
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(button, 0, wx.ALL, 5)
    Sizer.Add(label, 0, wx.ALL, 5)
    return button, label, Sizer

def return_textbox_labeled(parent, label, unit = False, enabled = False, read = False, read_command=""):
    """
    return sizer
    -----------------------------------------------------------------------------------------
    | label  | textcontrol | checkbox (optional)  | combobox (optional) | button (optional) |
    -----------------------------------------------------------------------------------------
    label text is label
    checkbox is optional
    combobox is list of unit chooser and it is optional
    button text is "Read" and it is used to send a read_command string
    
    return also textcontrol object, checkbox object (or None), combobox object (or None), button object and the command string
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size = (150,-1))
    txt = wx.TextCtrl(parent, wx.ID_ANY)
    Sizer   = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(txt, 0, wx.ALL, 5)
    if enabled:
        cb = wx.CheckBox(parent, -1, "", (10, 10))
        cb.SetValue(False)
        Sizer.Add(cb, 0, wx.ALL, 5)
    else:
        cb = None
    if unit:
        combobox = wx.ComboBox(parent, -1, size=(-1, -1), choices=unit_tmp.return_unit_list(), style=wx.CB_READONLY)
        Sizer.Add(combobox, 0, wx.ALL, 5)
    else:
        combobox = None
    if read:
        read_button = wx.Button(parent, 0, "Read")
        Sizer.Add(read_button, 0, wx.ALL, 5)
    else:
        read_button = None
    
    return txt, combobox, cb, Sizer, read_button, read_command

def return_instrument(parent):
    """
    return sizer
    --------------------------------------------------------------------------------------
    |        | label_IP       | label_port       | label_timeout       | label_instr_type|
    | label  |----------------|------------------|---------------------|-----------------|
    |        | textcontrol_IP | textcontrol_port | textcontrol_timeout | combobox_type   |
    --------------------------------------------------------------------------------------
    label text is "Instrument"
    label_IP text is "IP"
    label_port text is "Port"
    label_timeout text is "Timeout (ms)"
    label_instr_type is "Type"
    textcontrol_IP default value is "192.168.150.1"
    textcontrol_port default value is "5025"
    textcontrol_timeout default value is "5000"
    
    return also txt_IP, txt_Port, txt_Timeout, combobox_instrtype objects
    It's used to define comunication instrument settings in combination with sizer
    returned by return_test_instrument used for test test instrument comunication
    """
    label = wx.StaticText(parent, wx.ID_ANY, "Instrument", size = (150,-1))
    label_IP = wx.StaticText(parent, wx.ID_ANY, "IP", size = (150,-1))
    txt_IP = wx.TextCtrl(parent, wx.ID_ANY, value = "192.168.150.1")
    Sizer_IP   = wx.BoxSizer(wx.VERTICAL)
    Sizer_IP.Add(label_IP, 0, wx.ALL, 5)
    Sizer_IP.Add(txt_IP, 0, wx.ALL, 5)
    label_Port = wx.StaticText(parent, wx.ID_ANY, "Port", size = (-1,-1))
    txt_Port = wx.TextCtrl(parent, wx.ID_ANY, value = "5025", size = (50,-1))
    Sizer_Port   = wx.BoxSizer(wx.VERTICAL)
    Sizer_Port.Add(label_Port, 0, wx.ALL, 5)
    Sizer_Port.Add(txt_Port, 0, wx.ALL, 5)
    label_Timeout = wx.StaticText(parent, wx.ID_ANY, "Timeout (ms)", size = (-1,-1))
    txt_Timeout = wx.TextCtrl(parent, wx.ID_ANY, value="5000", size = (100,-1))
    Sizer_Timeout   = wx.BoxSizer(wx.VERTICAL)
    Sizer_Timeout.Add(label_Timeout, 0, wx.ALL, 5)
    Sizer_Timeout.Add(txt_Timeout, 0, wx.ALL, 5)
    label_instrtype = wx.StaticText(parent, wx.ID_ANY, "Type", size = (-1,-1))
    combobox_instrtype = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), value="INSTR", choices=["SOCKET", "INSTR", "TELNET"], style=wx.CB_READONLY)
    Sizer_instrtype   = wx.BoxSizer(wx.VERTICAL)
    Sizer_instrtype.Add(label_instrtype, 0, wx.ALL, 5)
    Sizer_instrtype.Add(combobox_instrtype, 0, wx.ALL, 5)
    Sizer   = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(Sizer_IP, 0, wx.ALL, 5)
    Sizer.Add(Sizer_Port, 0, wx.ALL, 5)
    Sizer.Add(Sizer_Timeout, 0, wx.ALL, 5)
    Sizer.Add(Sizer_instrtype, 0, wx.ALL, 5)
    
    return txt_IP, txt_Port, txt_Timeout, combobox_instrtype, Sizer

def return_comboBox_unit(parent, label):
    """
    return sizer
    --------------------------
    | label    |  combobox   |
    --------------------------
    label text is label 
    combobox is list of unit chooser
    
    return also the combobox object
    """
    
    label = wx.StaticText(parent, wx.ID_ANY, label, size = (150,-1))
    combobox = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(), style=wx.CB_READONLY)
    Sizer   = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(combobox, 0, wx.ALL, 5)
    return combobox, Sizer

def return_checkbox_labeled(parent, label):
    """
    return sizer
    --------------------------
    | label    |  checkbox   |
    --------------------------
    label text is label 
    checkbox text is 'Enable'
    
    return also the checkbox object
    """
    label = wx.StaticText(parent, id=wx.ID_ANY, label=label, size = (150,-1))
    cb = wx.CheckBox(parent, -1, 'Enable', (10, 10))
    cb.SetValue(True)
    Sizer   = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(cb, 0, wx.ALL, 5)
    return cb, Sizer

def return_spinctrl(parent, label):
    """
    return sizer
    ----------------------------
    | label    |  spincoontrol |
    ----------------------------
    label text is label 
    
    return also the spincoontrol object
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size = (150,-1))
    sc = wx.SpinCtrl(parent, -1, '', size = (60, -1))
    sc.SetRange(0, 10)
    sc.SetValue(1)
    Sizer   = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(sc, 0, wx.ALL, 5)
    return sc, Sizer


def return_spinctrl_min_max(parent, label):
    """
    return sizer
    ----------------------------------------------------------------------
    | label    |  spincoontrol_min | spincoontrol_max | spincoontrol_step |
    ----------------------------------------------------------------------
    label text is label 
    
    return also the spincoontrol object
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size = (150,-1))
    sc_min = wx.SpinCtrl(parent, -1, '', size = (60, -1))
    sc_min.SetRange(-10, 10)
    sc_min.SetValue(1)
    sc_max = wx.SpinCtrl(parent, -1, '', size = (60, -1))
    sc_max.SetRange(-10, 10)
    sc_max.SetValue(1)
    sc_step = wx.SpinCtrl(parent, -1, '', size = (60, -1))
    sc_step.SetRange(1, 10)
    sc_step.SetValue(1)
    Sizer   = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(sc_min, 0, wx.ALL, 5)
    Sizer.Add(sc_max, 0, wx.ALL, 5)
    Sizer.Add(sc_step, 0, wx.ALL, 5)
    return sc_min, sc_max, sc_step, Sizer

def return_min_max_step_labeled(parent, label, unit = False):
    """
    return sizer
    -------------------------------------------------------------------------------------------------
    |          |  label_min                |  label_max                |  label_step                |
    |          |---------------------------|---------------------------|----------------------------|
    | label    | textcontrol_min           | textcontrol_max           | textcontrol_step           |
    |          |---------------------------|---------------------------|----------------------------|
    |          | combobox_min (optional)   | combobox_max (optional)   | combobox_step (optional)   |
    -------------------------------------------------------------------------------------------------
    label text is label
    label_min text is "Min"
    label_max text is "Max"
    label_step text is "Step"
    combobox_min, combobox_max, combobox_step are optional and used for units
    
    return also textcontrol_min, textcontrol_max, textcontrol_step objects
    if selected it'return also combobox_min, combobox_max, combobox_step or None
    """
    label = wx.StaticText(parent, id=wx.ID_ANY, label=label, size = (150,-1))
    #min
    label_min = wx.StaticText(parent, id=wx.ID_ANY, label="Min", size = (100,-1))
    txt_min = wx.TextCtrl(parent, wx.ID_ANY)
    if unit:
        combobox_min = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(), style=wx.CB_READONLY)
    else:
        combobox_min = None
    Sizer_min_sub = wx.BoxSizer(wx.HORIZONTAL)
    Sizer_min_sub.Add(txt_min, 0, wx.ALL, 5)
    
    #Sizer_min.Add(txt_min, 0, wx.ALL, 5)
    if unit:
        Sizer_min_sub.Add(combobox_min, 0, wx.ALL, 5)
    Sizer_min   = wx.BoxSizer(wx.VERTICAL)
    Sizer_min.Add(label_min, 0, wx.ALL, 5)
    Sizer_min.Add(Sizer_min_sub, 0, wx.ALL, 5)
    #max
    label_max = wx.StaticText(parent, id=wx.ID_ANY, label="Max", size = (100,-1))
    txt_max = wx.TextCtrl(parent, wx.ID_ANY)
    if unit:
        combobox_max = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(), style=wx.CB_READONLY)
    else:
        combobox_max = None
    Sizer_max_sub = wx.BoxSizer(wx.HORIZONTAL)
    Sizer_max_sub.Add(txt_max, 0, wx.ALL, 5)
    
    #Sizer_min.Add(txt_min, 0, wx.ALL, 5)
    if unit:
        Sizer_max_sub.Add(combobox_max, 0, wx.ALL, 5)
    Sizer_max   = wx.BoxSizer(wx.VERTICAL)
    Sizer_max.Add(label_max, 0, wx.ALL, 5)
    Sizer_max.Add(Sizer_max_sub, 0, wx.ALL, 5)
    #step
    label_step = wx.StaticText(parent, id=wx.ID_ANY, label="Step", size = (100,-1))
    txt_step = wx.TextCtrl(parent, wx.ID_ANY)
    if unit:
        combobox_step = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(), style=wx.CB_READONLY)
    else:
        combobox_step = None
    Sizer_step_sub = wx.BoxSizer(wx.HORIZONTAL)
    Sizer_step_sub.Add(txt_step, 0, wx.ALL, 5)
    
    #Sizer_min.Add(txt_min, 0, wx.ALL, 5)
    if unit:
        Sizer_step_sub.Add(combobox_step, 0, wx.ALL, 5)
    Sizer_step   = wx.BoxSizer(wx.VERTICAL)
    Sizer_step.Add(label_step, 0, wx.ALL, 5)
    Sizer_step.Add(Sizer_step_sub, 0, wx.ALL, 5)
    Sizer   = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(Sizer_min, 0, wx.ALL, 5)
    Sizer.Add(Sizer_max, 0, wx.ALL, 5)
    Sizer.Add(Sizer_step, 0, wx.ALL, 5)
    return txt_min, combobox_min, txt_max, combobox_max, txt_step, combobox_step, Sizer
    