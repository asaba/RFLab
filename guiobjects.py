'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os
from utility import unit_class

unit_tmp = unit_class()


def return_checkbox_list(parent, label):
    """
    return a sizer:
    -------------------------------------------
    | label     | checkboxlist     | button   |
    -------------------------------------------
    label text is label
    checkboxlist is an empty checkbox list
    button text is "Load"
    
    return also checkboxlist object and the  button object
    
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
    checkboxlist = wx.CheckListBox(parent, -1)
    button = wx.Button(parent, 0, "Load")
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(checkboxlist, 0, wx.ALL, 5)
    Sizer.Add(button, 0, wx.ALL, 5)

    return checkboxlist, button, Sizer


def return_file_browse(parent, label, enabled=False):
    """
    return a sizer:
    ------------------------------------------------------------
    | label     | textcontrol | button   | checkbox (optional) |
    ------------------------------------------------------------
    label text is label
    button text is "..."
    
    return also the textcontrol object and the button object
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
    txt = wx.TextCtrl(parent, wx.ID_ANY)
    button = wx.Button(parent, 0, "...")
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(txt, 0, wx.ALL, 5)
    Sizer.Add(button, 0, wx.ALL, 5)
    if enabled:
        cb = wx.CheckBox(parent, -1, "", (10, 10))
        cb.SetValue(True)
        Sizer.Add(cb, 0, wx.ALL, 5)
    else:
        cb = None
    return txt, button, cb, Sizer


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
    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
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
    label = wx.StaticText(parent, wx.ID_ANY, "...", size=(150, -1))

    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(button, 0, wx.ALL, 5)
    Sizer.Add(label, 0, wx.ALL, 5)
    return button, label, Sizer


def return_textbox_labeled(parent, label, unit=False, enabled=False, enable_text="", read=False, button_text="Read",
                           read_command=""):
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
    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
    txt = wx.TextCtrl(parent, wx.ID_ANY)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(txt, 0, wx.ALL, 5)
    if enabled:
        cb = wx.CheckBox(parent, -1, enable_text, (10, 10))
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
        read_button = wx.Button(parent, 0, button_text)
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
    label = wx.StaticText(parent, wx.ID_ANY, "Instrument", size=(150, -1))
    label_IP = wx.StaticText(parent, wx.ID_ANY, "IP", size=(150, -1))
    txt_IP = wx.TextCtrl(parent, wx.ID_ANY, value="192.168.150.1")
    Sizer_IP = wx.BoxSizer(wx.VERTICAL)
    Sizer_IP.Add(label_IP, 0, wx.ALL, 5)
    Sizer_IP.Add(txt_IP, 0, wx.ALL, 5)
    label_Port = wx.StaticText(parent, wx.ID_ANY, "Port", size=(-1, -1))
    txt_Port = wx.TextCtrl(parent, wx.ID_ANY, value="5025", size=(50, -1))
    Sizer_Port = wx.BoxSizer(wx.VERTICAL)
    Sizer_Port.Add(label_Port, 0, wx.ALL, 5)
    Sizer_Port.Add(txt_Port, 0, wx.ALL, 5)
    label_Timeout = wx.StaticText(parent, wx.ID_ANY, "Timeout (ms)", size=(-1, -1))
    txt_Timeout = wx.TextCtrl(parent, wx.ID_ANY, value="5000", size=(100, -1))
    Sizer_Timeout = wx.BoxSizer(wx.VERTICAL)
    Sizer_Timeout.Add(label_Timeout, 0, wx.ALL, 5)
    Sizer_Timeout.Add(txt_Timeout, 0, wx.ALL, 5)
    label_instrtype = wx.StaticText(parent, wx.ID_ANY, "Type", size=(-1, -1))
    combobox_instrtype = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), value="INSTR",
                                     choices=["SOCKET", "INSTR", "TELNET", "VSCD"], style=wx.CB_READONLY)
    Sizer_instrtype = wx.BoxSizer(wx.VERTICAL)
    Sizer_instrtype.Add(label_instrtype, 0, wx.ALL, 5)
    Sizer_instrtype.Add(combobox_instrtype, 0, wx.ALL, 5)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(Sizer_IP, 0, wx.ALL, 5)
    Sizer.Add(Sizer_Port, 0, wx.ALL, 5)
    Sizer.Add(Sizer_Timeout, 0, wx.ALL, 5)
    Sizer.Add(Sizer_instrtype, 0, wx.ALL, 5)

    return txt_IP, txt_Port, txt_Timeout, combobox_instrtype, Sizer


def return_usb_instrument(parent):
    """
    return sizer
    --------------------------------------------------------------------------------------------
    |        |  label_com_port   | label_timeout       | label_baudrate  | label_search_button |
    | label  |-------------------|---------------------|-----------------|---------------------|
    |        |  combobox_com_port| textcontrol_timeout | combobox_baud   | search_button       |
    --------------------------------------------------------------------------------------------
    label text is "Instrument USB"
    label_com_port text is "COM Port"
    label_timeout text is "Timeout (ms)"
    label_boudrate is "Boundrate"
    label_search_button is "Search"
    
    return also combobox_com_port, txt_timeout_timeout, combobox_bound, search_button objects
    It's used to define comunication USB instrument settings in combination with sizer
    returned by return_test_instrument used for test test instrument comunication
    """
    label = wx.StaticText(parent, wx.ID_ANY, "Instrument USB", size=(150, -1))
    label_com_port = wx.StaticText(parent, wx.ID_ANY, "COM Port", size=(150, -1))
    combobox_com_port = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=["Click search button"],
                                    style=wx.CB_READONLY)
    Sizer_com_port = wx.BoxSizer(wx.VERTICAL)
    Sizer_com_port.Add(label_com_port, 0, wx.ALL, 5)
    Sizer_com_port.Add(combobox_com_port, 0, wx.ALL, 5)
    label_timeout = wx.StaticText(parent, wx.ID_ANY, "Timeout (ms)", size=(-1, -1))
    txt_timeout = wx.TextCtrl(parent, wx.ID_ANY, value="5000", size=(50, -1))
    Sizer_Timeout = wx.BoxSizer(wx.VERTICAL)
    Sizer_Timeout.Add(label_timeout, 0, wx.ALL, 5)
    Sizer_Timeout.Add(txt_timeout, 0, wx.ALL, 5)
    label_baudrate = wx.StaticText(parent, wx.ID_ANY, "Baud rate", size=(-1, -1))
    combobox_baud = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), value="5600",
                                choices=["300", "600", "1200", "2400", "4800", "9600", "14400", "19200", "28800",
                                         "38400", "57600", "115200"], style=wx.CB_READONLY)
    Sizer_BaudRate = wx.BoxSizer(wx.VERTICAL)
    Sizer_BaudRate.Add(label_baudrate, 0, wx.ALL, 5)
    Sizer_BaudRate.Add(combobox_baud, 0, wx.ALL, 5)
    label_search_button = wx.StaticText(parent, wx.ID_ANY, "Search COM", size=(-1, -1))
    search_button = wx.Button(parent, 0, "Search")
    Sizer_search = wx.BoxSizer(wx.VERTICAL)
    Sizer_search.Add(label_search_button, 0, wx.ALL, 5)
    Sizer_search.Add(search_button, 0, wx.ALL, 5)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(Sizer_com_port, 0, wx.ALL, 5)
    Sizer.Add(Sizer_Timeout, 0, wx.ALL, 5)
    Sizer.Add(Sizer_BaudRate, 0, wx.ALL, 5)
    Sizer.Add(Sizer_search, 0, wx.ALL, 5)

    return combobox_com_port, txt_timeout, combobox_baud, search_button, Sizer


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

    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
    combobox = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(),
                           style=wx.CB_READONLY)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(combobox, 0, wx.ALL, 5)
    return combobox, Sizer


def return_comboBox(parent, label, choices_list):
    """
    return sizer
    --------------------------
    | label    |  combobox   |
    --------------------------
    label text is label 
    combobox is list choices_list
    
    return also the combobox object
    """

    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
    combobox = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=choices_list, style=wx.CB_READONLY)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
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
    label = wx.StaticText(parent, id=wx.ID_ANY, label=label, size=(150, -1))
    cb = wx.CheckBox(parent, -1, 'Enable', (10, 10))
    cb.SetValue(True)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(cb, 0, wx.ALL, 5)
    return cb, Sizer


def return_spinctrl(parent, label, max_value=10):
    """
    return sizer
    ----------------------------
    | label    |  spincoontrol |
    ----------------------------
    label text is label 
    
    return also the spincoontrol object
    """
    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
    sc = wx.SpinCtrl(parent, -1, '', size=(60, -1))
    sc.SetRange(0, max_value)
    sc.SetValue(1)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
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
    label = wx.StaticText(parent, wx.ID_ANY, label, size=(150, -1))
    sc_min = wx.SpinCtrl(parent, -1, '', size=(60, -1))
    sc_min.SetRange(-10, 10)
    sc_min.SetValue(1)
    sc_max = wx.SpinCtrl(parent, -1, '', size=(60, -1))
    sc_max.SetRange(-10, 10)
    sc_max.SetValue(1)
    sc_step = wx.SpinCtrl(parent, -1, '', size=(60, -1))
    sc_step.SetRange(1, 10)
    sc_step.SetValue(1)
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(label, 0, wx.ALL, 5)
    Sizer.Add(sc_min, 0, wx.ALL, 5)
    Sizer.Add(sc_max, 0, wx.ALL, 5)
    Sizer.Add(sc_step, 0, wx.ALL, 5)
    return sc_min, sc_max, sc_step, Sizer


def return_min_max_step_labeled(parent, label, unit=False, single_unit=False, button_text=None):
    """
    return sizer
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    |          |  label_min      |                     | label_max        |                     | label_step        |                       |  label_unit (opt.)    |                   |
    | label    |-----------------|---------------------|------------------|---------------------|-------------------|-----------------------|-----------------------| button_calc(opt.) |
    |          | textcontrol_min | combobox_min (opt.) | textcontrol_max  | combobox_max (opt.) | textcontrol_step  |  combobox_step (opt.) |  combobox_unit (opt.) |                   |
    -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    label text is label
    label_min text is "Min"
    label_max text is "Max"
    label_step text is "Step"
    label_unit test is "Unit"
    combobox_min, combobox_max, combobox_step, label_unit test, combobox_unit are optional and used for units
    button_cal is optional 
    
    return also textcontrol_min, textcontrol_max, textcontrol_step objects
    if selected it'return also combobox_min, combobox_max, combobox_step, combobox_unit, button_cal or None
    """
    label = wx.StaticText(parent, id=wx.ID_ANY, label=label, size=(150, -1))
    label_dummy_l = wx.StaticText(parent, id=wx.ID_ANY, label="", size=(150, -1))
    Sizer_label = wx.BoxSizer(wx.VERTICAL)
    Sizer_label.Add(label_dummy_l, 0, wx.ALL, 5)
    Sizer_label.Add(label, 0, wx.ALL, 5)
    # min
    label_min = wx.StaticText(parent, id=wx.ID_ANY, label="Min", size=(60, -1))
    txt_min = wx.TextCtrl(parent, wx.ID_ANY)
    if unit:
        combobox_min = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(),
                                   style=wx.CB_READONLY)
    else:
        combobox_min = None
    Sizer_min_sub = wx.BoxSizer(wx.HORIZONTAL)
    Sizer_min_sub.Add(txt_min, 0, wx.ALL, 5)

    # Sizer_min.Add(txt_min, 0, wx.ALL, 5)
    if unit:
        Sizer_min_sub.Add(combobox_min, 0, wx.ALL, 5)
    Sizer_min = wx.BoxSizer(wx.VERTICAL)
    Sizer_min.Add(label_min, 0, wx.ALL, 5)
    Sizer_min.Add(Sizer_min_sub, 0, wx.ALL, 5)
    # max
    label_max = wx.StaticText(parent, id=wx.ID_ANY, label="Max", size=(60, -1))
    txt_max = wx.TextCtrl(parent, wx.ID_ANY)
    if unit:
        combobox_max = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(),
                                   style=wx.CB_READONLY)
    else:
        combobox_max = None
    Sizer_max_sub = wx.BoxSizer(wx.HORIZONTAL)
    Sizer_max_sub.Add(txt_max, 0, wx.ALL, 5)

    # Sizer_min.Add(txt_min, 0, wx.ALL, 5)
    if unit:
        Sizer_max_sub.Add(combobox_max, 0, wx.ALL, 5)
    Sizer_max = wx.BoxSizer(wx.VERTICAL)
    Sizer_max.Add(label_max, 0, wx.ALL, 5)
    Sizer_max.Add(Sizer_max_sub, 0, wx.ALL, 5)
    # step
    label_step = wx.StaticText(parent, id=wx.ID_ANY, label="Step", size=(60, -1))
    txt_step = wx.TextCtrl(parent, wx.ID_ANY)
    if unit:
        combobox_step = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(),
                                    style=wx.CB_READONLY)
    else:
        combobox_step = None
    Sizer_step_sub = wx.BoxSizer(wx.HORIZONTAL)
    Sizer_step_sub.Add(txt_step, 0, wx.ALL, 5)

    # Sizer_min.Add(txt_min, 0, wx.ALL, 5)
    if unit:
        Sizer_step_sub.Add(combobox_step, 0, wx.ALL, 5)
    Sizer_step = wx.BoxSizer(wx.VERTICAL)
    Sizer_step.Add(label_step, 0, wx.ALL, 5)
    Sizer_step.Add(Sizer_step_sub, 0, wx.ALL, 5)

    if single_unit:
        # unit
        label_unit = wx.StaticText(parent, id=wx.ID_ANY, label="Unit", size=(60, -1))
        combobox_unit = wx.ComboBox(parent, -1, pos=(50, 170), size=(-1, -1), choices=unit_tmp.return_unit_list(),
                                    style=wx.CB_READONLY)
        Sizer_unit_sub = wx.BoxSizer(wx.HORIZONTAL)

        Sizer_unit_sub.Add(combobox_unit, 0, wx.ALL, 5)
        Sizer_unit = wx.BoxSizer(wx.VERTICAL)
        Sizer_unit.Add(label_unit, 0, wx.ALL, 5)
        Sizer_unit.Add(Sizer_unit_sub, 0, wx.ALL, 5)
    else:
        combobox_unit = None

    if button_text is None:
        button_cal = None
    else:
        # unit
        button_cal = wx.Button(parent, 0, button_text)
        label_dummy_b = wx.StaticText(parent, id=wx.ID_ANY, label="", size=(60, -1))
        Sizer_calc_sub = wx.BoxSizer(wx.VERTICAL)
        Sizer_calc_sub.Add(label_dummy_b, 0, wx.ALL, 5)
        Sizer_calc_sub.Add(button_cal, 0, wx.ALL, 5)

    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(Sizer_label, 0, wx.ALL, 5)
    Sizer.Add(Sizer_min, 0, wx.ALL, 5)
    Sizer.Add(Sizer_max, 0, wx.ALL, 5)
    Sizer.Add(Sizer_step, 0, wx.ALL, 5)
    if single_unit:
        Sizer.Add(Sizer_unit, 0, wx.ALL, 5)
    if button_text is None:
        pass
    else:
        Sizer.Add(Sizer_calc_sub, 0, wx.ALL, 5)
    return txt_min, combobox_min, txt_max, combobox_max, txt_step, combobox_step, combobox_unit, button_cal, Sizer


def return_image(parent, image_path):
    """
    return sizer
    ----------------------------
    | image                    |
    ----------------------------
    label is an image 
    """
    image = wx.StaticBitmap(parent, -1, wx.Bitmap(image_path, wx.BITMAP_TYPE_ANY))
    Sizer = wx.BoxSizer(wx.HORIZONTAL)
    Sizer.Add(image, 0, wx.ALL, 5)
    return Sizer
