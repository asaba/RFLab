'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os

from guiobjects import return_checkbox_labeled, return_spinctrl, return_textbox_labeled, return_comboBox_unit, return_file_browse, return_instrument, return_test_instrument, return_simple_button, return_min_max_step_labeled, return_spinctrl_min_max, return_comboBox, return_usb_instrument
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument, browse_file, check_steps_count, error_message, check_instrument_comunication, check_USB_instrument_comunication
from measure_scripts.plotIP1graph import calculate_all_IP1, unit
from measure_scripts.plotSpuriusCGraph import plot_spurius_graph, order_and_group_data
from measure_scripts.csvutility import *
import matplotlib.pyplot as plt
from measure_scripts.graphutility import Graph_Axis_Range, graph_types, generic_graph_types
import serial.tools.list_ports
import webbrowser
import subprocess
from utility import inkscape_exec, buildfitsfileslist, return_max_min_from_data_table_row
from measure_scripts.instrumentmeasures import readFSV_sweep, FSV_reset_setup
from measure_scripts.plotXYgraph import plot_XY_Single, build_table_value_from_x_y
from measure_scripts.Spurius import spectrum_analyzer_IF_relative_level_enable

fig1=None

class InstrumentPanelClass(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.instrument_txt_IP, self.instrument_txt_Port, self.instrument_txt_Timeout, self.combobox_instrtype, self.instrument_sizer = return_instrument(self)
        self.instrument_test_button, self.instrument_label, self.instrument_test_sizer  = return_test_instrument(self)
        self.instrument_enable_status, self.instrument_enable_status_sizer = return_checkbox_labeled(self, "Instrument Status")
        self.instrument_test_button.Bind(wx.EVT_BUTTON, self.OnTestInstrument)
    
    def OnTestInstrument(self, event):
        dummy, response = check_instrument_comunication(self.instrument_txt_IP.GetValue(), self.instrument_txt_Port.GetValue(), eval(self.instrument_txt_Timeout.GetValue()), self.combobox_instrtype.GetValue())
        self.instrument_label.SetLabel(response)
        
        
class InstrumentUSBPanelClass(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.instrument_combobox_com_port, self.instrument_txt_timeout, self.instrument_combobox_baud, self.instrument_search_button, self.instrument_sizer = return_usb_instrument(self)
        self.instrument_test_button, self.instrument_label, self.instrument_test_sizer  = return_test_instrument(self)
        self.instrument_enable_status, self.instrument_enable_status_sizer = return_checkbox_labeled(self, "Instrument Status")
        
        self.instrument_test_button.Bind(wx.EVT_BUTTON, self.OnTestInstrument)
        self.instrument_search_button.Bind(wx.EVT_BUTTON, self.OnSearchCom)
    
    def OnSearchCom(self, event):
        
        ports_present = list(serial.tools.list_ports.comports())
        if len(ports_present) == 0:
            ports_present = [u"No device"]
        self.instrument_combobox_com_port.Clear()
        for c in ports_present:
            self.instrument_combobox_com_port.Append(unicode(c[0]))
            
    def OnTestInstrument(self, event):
        dummy, response = check_USB_instrument_comunication(self.instrument_combobox_com_port.GetValue(), eval(self.instrument_txt_timeout.GetValue()), self.instrument_combobox_baud.GetValue())
        response = [ord(x) for x in response]
        #response = [response[3], response[2]]
        response = response[3] << 8 + response[2]
        self.instrument_label.SetLabel(str(response))

class SetupPanelClass(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.result_file_name, self.result_file_name_button, dummy, self.sizer_result_file_name = return_file_browse(self, "Output File")
        self.result_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_Out)
    
    def File_browser_Out(self, event):
        browse_file(self, self.result_file_name, wildcard = "*", mode = wx.SAVE)
        #dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*", wx.SAVE)
        #if dlg.ShowModal() == wx.ID_OK:
        #    path = dlg.GetPath()
        #    self.result_file_name.SetValue(path)
        #else:
        #    self.result_file_name.SetValue("")
        #dlg.Destroy()
        
class PlotGraphPanelClass(wx.Panel):
    
    #input Data File
    #Graph Title
    
    def __init__(self, parent, input_file_wildcard = "*.csv"):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_file_name, self.data_file_name_button, dummy, self.sizer_data_file_name = return_file_browse(self, "Data File")
        self.wildcard = input_file_wildcard
        self.data_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_DataFile)
        
        #Graph Title
        self.graph_title, dummy, dummy, self.sizer_graph_title, dummy, dummy = return_textbox_labeled(self, "Graph title")
        
    
    def File_browser_DataFile(self, event):
        browse_file(self, self.data_file_name, wildcard = self.wildcard)
        
class TabPanelContinousVoltageSetup(SetupPanelClass):
    """
    Tab for Continous Voltage Measure
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        #Calibration Cable parameter
        
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
        
class TabPanelCalDummyCableSetup(SetupPanelClass):
    """
    Tab for Dummy Cable Calibration parameters
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        #Calibration Cable parameter
        
        #synthetizer_LO_frequency_min = 4600
        #self.frequency_min, self.frequency_min_unit, dummy, self.sizer_frequency_min, dummy, dummy = return_textbox_labeled(self, "Minimum Frequency", unit= True)

        #synthetizer_LO_frequency_max = 5000
        #self.frequency_max, self.frequency_max_unit, dummy, self.sizer_frequency_max, dummy, dummy = return_textbox_labeled(self, "Maximum Frequency", unit= True)
        
        #synthetizer_LO_frequency_step = 200
        #self.frequency_step, self.frequency_step_unit, dummy, self.sizer_frequency_step, dummy, dummy = return_textbox_labeled(self, "Frequency Step", unit= True)
        
        #self.frequency_min, self.frequency_min_unit, self.frequency_max, self.frequency_max_unit, self.frequency_step, self.frequency_step_unit, dummy, dummy, self.sizer_frequency = return_min_max_step_labeled(self, "Frequency", unit = True)
        self.frequency_min, dummy, self.frequency_max, dummy, self.frequency_step, dummy, self.frequency_unit, dummy, self.sizer_frequency = return_min_max_step_labeled(self, "Frequency", unit = False, single_unit = True)
        
        #synthetizer_LO_level_min = 6 #dBm
        self.output_level, dummy, dummy, self.sizer_output_level, dummy, dummy = return_textbox_labeled(self, "Output Power Level")
        
        self.output_frequency_unit, self.sizer_output_frequency_unit = return_comboBox_unit(self, "Output Frequency unit")
        
        #D:\Users\Andrea\Desktop
        #result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\misuraSpuri04122015" #without extension
        
        
        
        #sizer.Add(self.sizer_frequency_min, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_frequency_max, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_frequency_step, 0, wx.ALL, 5)
        sizer.Add(self.sizer_frequency, 0, wx.ALL, 5)
        sizer.Add(self.sizer_output_level, 0, wx.ALL, 5)
        sizer.Add(self.sizer_output_frequency_unit, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
        

class TabPanelCalCableSetup(SetupPanelClass):
    """
    Tab for Cable Calibration parameters
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.output_level, dummy, self.create_dummycable_cb, self.sizer_output_level, dummy, dummy = return_textbox_labeled(self, "Output Power Level (Dummy Cable)", enabled = True, enable_text = "Create Dummy Cable")
        
        
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_output_level, 0, wx.ALL, 5)
        
 
        self.SetSizer(sizer)
        

class TabPanelIP1CalcSetup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #IP1 calculation variables

        self.calibration_file_RF, self.calibration_file_RF_button, self.calibration_file_RF_enable, self.sizer_calibration_file_RF = return_file_browse(self, "Radio Frequency Cable Calibration File", enabled = True)
        self.calibration_file_RF_button.Bind(wx.EVT_BUTTON, self.File_browser_RF)
        

        sizer.Add(self.sizer_calibration_file_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
        
    def File_browser_RF(self, event):
        browse_file(self, self.calibration_file_RF)
        

class TabPanelSpuriusSetup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #spurius calculation variables

        #m_max_RF = 7
        #self.m_max_RF, self.sizer_m_max_RF = return_spinctrl(self, "Max m for RF")
        self.m_min_RF, self.m_max_RF, self.m_step_RF, self.sizer_m_RF = return_spinctrl_min_max(self, "m for RF (min/max/step)")
        #n_max_LO = 7
        #self.n_max_LO, self.sizer_n_max_LO = return_spinctrl(self, "Max n for LO")
        self.n_min_LO, self.n_max_LO, self.n_step_LO, self.sizer_n_LO = return_spinctrl_min_max(self, "n for LO (min/max/step)")
        
        #IF_high = 3000
        self.IF_low, self.IF_low_unit, dummy, self.sizer_IF_low, dummy, dummy = return_textbox_labeled(self, "Min Spurius Frequency", unit = True)
        
        #IF_high = 3000
        self.IF_high, self.IF_high_unit, dummy, self.sizer_IF_high, dummy, dummy = return_textbox_labeled(self, "Max Spurius Frequency", unit = True)
        
        #spurius_IF_unit = unit.MHz
        self.spurius_IF_unit, self.sizer_spurius_IF_unit = return_comboBox_unit(self, "Spurius Frequency unit")
        
        #calibration_file_LO = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_LO, self.calibration_file_LO_button, self.calibration_file_LO_enable, self.sizer_calibration_file_LO = return_file_browse(self, "Local Ocillator Cable Calibration File", enabled = True)
        self.calibration_file_LO_button.Bind(wx.EVT_BUTTON, self.File_browser_LO)
        
        #calibration_file_RF = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_RF, self.calibration_file_RF_button, self.calibration_file_RF_enable, self.sizer_calibration_file_RF = return_file_browse(self, "Radio Frequency Cable Calibration File", enabled = True)
        self.calibration_file_RF_button.Bind(wx.EVT_BUTTON, self.File_browser_RF)

        #calibration_file_IF = ""
        self.calibration_file_IF, self.calibration_file_IF_button, self.calibration_file_IF_enable, self.sizer_calibration_file_IF = return_file_browse(self, "Output Frequency Cable Calibration File", enabled = True)
        self.calibration_file_IF_button.Bind(wx.EVT_BUTTON, self.File_browser_IF)
        

        sizer.Add(self.sizer_m_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_n_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_IF_low, 0, wx.ALL, 5)
        sizer.Add(self.sizer_IF_high, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_IF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spurius_IF_unit, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
    
    def File_browser_LO(self, event):
        browse_file(self, self.calibration_file_LO)
        
    def File_browser_RF(self, event):
        browse_file(self, self.calibration_file_RF)
        
    def File_browser_IF(self, event):
        browse_file(self, self.calibration_file_IF)
        
class TabPanelPM5Setup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)


        #calibration_file_LO = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_LO, self.calibration_file_LO_button, self.calibration_file_LO_enable, self.sizer_calibration_file_LO = return_file_browse(self, "Local Ocillator Cable Calibration File", enabled = True)
        self.calibration_file_LO_button.Bind(wx.EVT_BUTTON, self.File_browser_LO)

        sizer.Add(self.sizer_calibration_file_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
    
    def File_browser_LO(self, event):
        browse_file(self, self.calibration_file_LO)

class TabPanelFSV(InstrumentPanelClass):
    """
    Tab for FSV
    """
    
    def __init__(self, parent, enable_show_function = False):
        
        InstrumentPanelClass.__init__(self, parent=parent )
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #spectrum_analyzer_state = "ON"
        #self.spectrum_analyzer_state, self.sizer_spectrum_analyzer_state = return_checkbox_labeled(self, "State")
        
        #spectrum_analyzer_sweep_points = 1001
        self.spectrum_analyzer_sweep_points, dummy, dummy, self.sizer_spectrum_analyzer_sweep_points, dummy, dummy = return_textbox_labeled(self, "Sweep points")
        
        #spectrum_analyzer_resolution_bandwidth = 1
        self.spectrum_analyzer_resolution_bandwidth, self.spectrum_analyzer_resolution_bandwidth_unit, dummy, self.sizer_spectrum_analyzer_resolution_bandwidth, dummy, dummy = return_textbox_labeled(self, "Resolution bandwidth", unit = True)
        
        #spectrum_analyzer_video_bandwidth = 1
        self.spectrum_analyzer_video_bandwidth, self.spectrum_analyzer_video_bandwidth_unit, dummy, self.sizer_spectrum_analyzer_video_bandwidth, dummy, dummy = return_textbox_labeled(self, "Video bandwidth", unit = True)
        
        #spectrum_analyzer_frequency_span = 100
        self.spectrum_analyzer_frequency_span, self.spectrum_analyzer_frequency_span_unit, dummy, self.sizer_spectrum_analyzer_frequency_span, dummy, dummy = return_textbox_labeled(self, "Frequency Span", unit = True)
        
        
        #spectrum_analyzer_frequency_marker_unit = unit.KHz
        self.spectrum_analyzer_frequency_marker_unit, self.sizer_spectrum_analyzer_frequency_marker_unit = return_comboBox_unit(self, "Frequency marker unit")
        

        ##spectrum_analyzer_attenuation = 0
        #self.spectrum_analyzer_attenuation, dummy, dummy, self.sizer_spectrum_analyzer_attenuation, dummy, dummy = return_textbox_labeled(self, "Attenuation")
        
        #gainAmplifier = 40 #dB
        self.gainAmplifier, dummy, dummy, self.sizer_gainAmplifier, dummy, dummy = return_textbox_labeled(self, "Gain Amplifier")

        #spectrum_analyzer_IF_atten = 0
        self.spectrum_analyzer_IF_atten, dummy, self.spectrum_analyzer_IF_atten_enable, self.sizer_spectrum_analyzer_IF_atten, dummy, dummy = return_textbox_labeled(self, "Attenuation", enabled = True)

        #spectrum_analyzer_IF_relative_level = 30
        self.spectrum_analyzer_IF_relative_level, dummy, self.spectrum_analyzer_IF_relative_level_enable, self.sizer_spectrum_analyzer_IF_relative_level, dummy, dummy = return_textbox_labeled(self, "Relative Level", enabled = True)
        

        #threshold_power = 30 #dB 
        self.threshold_power, dummy, dummy, self.sizer_threshold_power, dummy, dummy = return_textbox_labeled(self, "Threshould")
        
        self.spectrum_analyzer_central_frequency, self.spectrum_analyzer_central_frequency_unit, dummy, self.sizer_spectrum_analyzer_central_frequency, self.spectrum_analyzer_central_frequency_button, dummy = return_textbox_labeled(self, "Central Frequency", unit = True, enabled = False, enable_text = "", read = True, button_text = "Plot display")
        self.spectrum_analyzer_central_frequency_button.Bind(wx.EVT_BUTTON, self.OnPlotSpectrum)
        
        #FSV_delay = 1
        self.FSV_delay, dummy, dummy, self.sizer_FSV_delay, dummy, dummy = return_textbox_labeled(self, "Measure delay (s)")
        
        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_enable_status_sizer, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_spectrum_analyzer_state, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_sweep_points, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_resolution_bandwidth, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_video_bandwidth, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_frequency_span, 0, wx.ALL, 5)
        #if enable_show_function:
            
        
        sizer.Add(self.sizer_spectrum_analyzer_frequency_marker_unit, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_spectrum_analyzer_attenuation, 0, wx.ALL, 5)
        sizer.Add(self.sizer_gainAmplifier, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_IF_atten, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_IF_relative_level, 0, wx.ALL, 5)
        sizer.Add(self.sizer_threshold_power, 0, wx.ALL, 5)
        sizer.Add(self.sizer_FSV_delay, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_central_frequency, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
        
    def OnPlotSpectrum(self, event):
        #Function to plot the spectrum for actual parameters
        self.testmode = False
        try:
            if self.Parent.GrandParent.runmodeitem.IsChecked():
                dlg = wx.MessageDialog(None, 'Test mode. Instruments comunication disabled', "Test mode",  wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                self.testmode = True
        except:
            pass
        
        spectrum_analyzer_IP = self.instrument_txt_IP.GetValue()
        if check_value_is_IP(spectrum_analyzer_IP, "LO Synthetizer IP") == 0:
            return None
        
        spectrum_analyzer_Port = self.instrument_txt_Port.GetValue()
        if check_value_min_max(spectrum_analyzer_Port, "LO Synthetizer Port", minimum = 0) == 0:
            return None
        
        spectrum_analyzer_Timeout = self.instrument_txt_Timeout.GetValue()
        if check_value_min_max(spectrum_analyzer_Timeout, "LO Synthetizer Timeout", minimum = 0) == 0:
            return None
        
        spectrum_analyzer_instrType = self.combobox_instrtype.GetValue()
        
        spectrum_analyzer_state = self.instrument_enable_status.GetValue()
        
        
        if spectrum_analyzer_state:
            spectrum_analyzer_sweep_points = self.spectrum_analyzer_sweep_points.GetValue()
            if check_value_min_max(spectrum_analyzer_sweep_points, "Sweep points", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_sweep_points = eval(self.spectrum_analyzer_sweep_points.GetValue())
            
            
            spectrum_analyzer_resolution_bandwidth = self.spectrum_analyzer_resolution_bandwidth.GetValue()
            if check_value_min_max(spectrum_analyzer_resolution_bandwidth, "Resolution Bandwidth", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_resolution_bandwidth = eval(self.spectrum_analyzer_resolution_bandwidth.GetValue())
            
            spectrum_analyzer_resolution_bandwidth_unit = unit.return_unit(self.spectrum_analyzer_resolution_bandwidth_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_resolution_bandwidth_unit, "Resolution Bandwidth Unit") == 0:
                return None
            
            spectrum_analyzer_video_bandwidth = self.spectrum_analyzer_video_bandwidth.GetValue()
            if check_value_min_max(spectrum_analyzer_video_bandwidth, "Video Bandwidth", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_video_bandwidth = eval(self.spectrum_analyzer_video_bandwidth.GetValue())
            
            spectrum_analyzer_video_bandwidth_unit = unit.return_unit(self.spectrum_analyzer_video_bandwidth_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_video_bandwidth_unit, "Video Bandwidth Unit") == 0:
                return None
            
            spectrum_analyzer_frequency_span = self.spectrum_analyzer_frequency_span.GetValue()
            if check_value_min_max(spectrum_analyzer_frequency_span, "Frequency Span", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_frequency_span = eval(self.spectrum_analyzer_frequency_span.GetValue())
            
            spectrum_analyzer_frequency_span_unit = unit.return_unit(self.spectrum_analyzer_frequency_span_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_frequency_span_unit, "Frequency Span Unit") == 0:
                return None
            
            ##spectrum_analyzer_harmonic_number = spectrum_analyzer_harmonic_number
            #spectrum_analyzer_attenuation = self.notebook.tabFSV.spectrum_analyzer_attenuation.GetValue()
            #if check_value_not_none(spectrum_analyzer_attenuation, "Attenuation") == 0:
            #    return None
            
            gainAmplifier = self.gainAmplifier.GetValue() #dB
            if check_value_not_none(gainAmplifier, "Gain Amplifier") == 0:
                return None
            
            spectrum_analyzer_IF_atten_enable = self.spectrum_analyzer_IF_atten_enable.GetValue()
            spectrum_analyzer_IF_atten = self.spectrum_analyzer_IF_atten.GetValue()
            if check_value_not_none(spectrum_analyzer_IF_atten, "Attenuation") == 0:
                return None
            
            spectrum_analyzer_IF_relative_level = self.spectrum_analyzer_IF_relative_level.GetValue()
            if check_value_not_none(spectrum_analyzer_IF_relative_level, "Relative Power Level") == 0:
                return None
            
            spectrum_analyzer_IF_relative_level_enable = self.spectrum_analyzer_IF_relative_level_enable.GetValue()
            
            
            threshold_power = self.threshold_power.GetValue() #dB 
            if check_value_not_none(threshold_power, "Threshold Power Level") == 0:
                return None
            
            spectrum_analyzer_frequency_marker_unit = unit.return_unit(self.spectrum_analyzer_frequency_marker_unit.GetValue())
            #to check
            if check_value_not_none(spectrum_analyzer_frequency_marker_unit, "Marker Frequency Unit") == 0:
                return None
            
            FSV_delay = self.FSV_delay.GetValue()
            if check_value_min_max(FSV_delay, "FSV measure delay", minimum = 0) == 0:
                return None
            else:
                FSV_delay = eval(self.FSV_delay.GetValue()) 
            
            spectrum_analyzer_central_frequency = self.spectrum_analyzer_central_frequency.GetValue()
            if check_value_min_max(spectrum_analyzer_central_frequency, "Central Frequency", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_video_bandwidth = eval(self.spectrum_analyzer_video_bandwidth.GetValue())
            
            
            spectrum_analyzer_central_frequency_unit = unit.return_unit(self.spectrum_analyzer_central_frequency_unit.GetValue())
            #to check
            if check_value_not_none(spectrum_analyzer_central_frequency_unit, "Central Frequency Unit") == 0:
                return None
            
        
        try:
            FSV = create_instrument(spectrum_analyzer_IP, spectrum_analyzer_Port, eval(spectrum_analyzer_Timeout), spectrum_analyzer_instrType, TEST_MODE = self.testmode, instrument_class = "FSV", enable_state = spectrum_analyzer_state)
        except:
            dlg = wx.MessageDialog(None, "Spectrum analiser comunication error", 'Error Spectrum analiser', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        FSV_reset_setup(FSV, spectrum_analyzer_sweep_points, 
                    spectrum_analyzer_resolution_bandwidth, 
                    spectrum_analyzer_resolution_bandwidth_unit, 
                    spectrum_analyzer_video_bandwidth, 
                    spectrum_analyzer_video_bandwidth_unit, 
                    spectrum_analyzer_frequency_span, 
                    spectrum_analyzer_frequency_span_unit, 
                    spectrum_analyzer_IF_atten_enable, 
                    spectrum_analyzer_IF_atten, 
                    spectrum_analyzer_IF_relative_level_enable, 
                    spectrum_analyzer_IF_relative_level)
        
        
        table_value = build_table_value_from_x_y(*readFSV_sweep(FSV, 
                                                              FSV_delay, 
                                                              spectrum_analyzer_central_frequency, 
                                                              spectrum_analyzer_central_frequency_unit))
        
        x_max, x_min, y_max, y_min, z_max, z_min = return_max_min_from_data_table_row(table_value, 0, 2, None)
        
        axis_x_legend = "CF {central_frequency} {central_frequency_unit} -  - Span {span} {span_unit}".format(central_frequency = str(spectrum_analyzer_central_frequency),
                                                                                                              central_frequency_unit = unit.return_unit_str(spectrum_analyzer_central_frequency_unit),
                                                                                                              span = str(spectrum_analyzer_frequency_span),
                                                                                                              span_unit = unit.return_unit_str(spectrum_analyzer_frequency_span_unit))

        axis_y_legend = "Ref.Level {ref_level} dBm  - Attenuation {attenuation} dB".format(ref_level = str(spectrum_analyzer_IF_relative_level) if spectrum_analyzer_IF_relative_level_enable else "0",
                                                                                           attenuation = str(spectrum_analyzer_IF_atten) if spectrum_analyzer_IF_atten_enable else "0",)
        graph_x = Graph_Axis_Range(x_min, x_max, (x_max-x_min)/10, unit.Hz, axis_x_legend)
        graph_y = Graph_Axis_Range(y_min, y_max, (y_max-y_min)/10, unit.dB, axis_y_legend)
        graph_z = Graph_Axis_Range(0, 0 , 1, unit.Hz)
        
        fig = plt.figure()
        
        plot_XY_Single(fig1, table_value, 
                       graph_group_index = [1], 
                       x_index = 0, 
                       y_index = 2, 
                       z_index = None, 
                       legend_index = [(0, -1, "", 0)], 
                       legend_title = None, 
                       graph_title = "SA Sweep",
                       graph_type = "GG", 
                       graph_x = graph_x, 
                       graph_y = graph_y, 
                       graph_z = graph_z,
                       save = False)
        


class TabPanelPM5(InstrumentUSBPanelClass):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        InstrumentUSBPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #pm5_state = "ON"
        #self.pm5_state, self.sizer_pm5_state = return_checkbox_labeled(self, "State")
        #power_meter_misure_number = 1
        self.pm5_misure_number, self.sizer_pm5_misure_number = return_spinctrl(self, "Measures")
        
        #power_meter_misure_delay = 1 #seconds
        self.pm5_misure_delay, dummy, dummy, self.sizer_pm5_misure_delay, dummy, dummy = return_textbox_labeled(self, "Measure delay (s)")

        
        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_enable_status_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_pm5_misure_number, 0, wx.ALL, 5)
        sizer.Add(self.sizer_pm5_misure_delay, 0, wx.ALL, 5)

        self.SetSizer(sizer)

########################################################################
class TabPanelSMB(InstrumentPanelClass):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent, range_power = True):
        """"""
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #synthetizer_LO_state = "ON"
        #self.synthetizer_state, self.sizer_synthetizer_state = return_checkbox_labeled(self, "State")
        
        #self.synthetizer_frequency_min, self.synthetizer_frequency_min_unit, self.synthetizer_frequency_max, self.synthetizer_frequency_max_unit, self.synthetizer_frequency_step, self.synthetizer_frequency_step_unit, dummy, dummy, self.sizer_synthetizer_frequency = return_min_max_step_labeled(self, "Frequency", unit = True)
        
        self.synthetizer_frequency_min, dummy, self.synthetizer_frequency_max, dummy, self.synthetizer_frequency_step, dummy, self.synthetizer_frequency_unit, dummy, self.sizer_synthetizer_frequency = return_min_max_step_labeled(self, "Frequency", unit = False, single_unit = True)
        
        #self.synthetizer_level_step, dummy, dummy, self.sizer_synthetizer_level_step, dummy, dummy = return_textbox_labeled(self, "Power Level Step")
        if range_power:
            self.synthetizer_level_min, dummy, self.synthetizer_level_max, dummy, self.synthetizer_level_step, dummy, dummy, dummy, self.sizer_synthetizer_level = return_min_max_step_labeled(self, "Level", unit = False)
        else:
            self.synthetizer_level_fixed, dummy, dummy, self.sizer_synthetizer_level_fixed, dummy, dummy = return_textbox_labeled(self, "Fixed Power Level")
        
        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_enable_status_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_synthetizer_frequency, 0, wx.ALL, 5)
        if range_power:
            sizer.Add(self.sizer_synthetizer_level, 0, wx.ALL, 5)
        else:
            sizer.Add(self.sizer_synthetizer_level_fixed, 0, wx.ALL, 5)

 
        self.SetSizer(sizer)
    
class TabPanelSourceMeter (InstrumentPanelClass):
    """
    Tab for Keithley SourceMeter
    """
    
    def __init__(self, parent):
        
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)


class XYPlotGraphPanelClass(PlotGraphPanelClass):
    """
    Tab for Plot XY Graph ex. IP1, Spurius, ...
    """
    
    def __init__(self, parent, animated = False, z_axes = False, input_file_wildcard = "*.csv"):
        
        PlotGraphPanelClass.__init__(self, parent=parent, input_file_wildcard = input_file_wildcard)
        
        self.graph_x_label, dummy, dummy, self.sizer_graph_x_label, dummy, dummy = return_textbox_labeled(self, "X Axes Label")
        self.graph_x_min, dummy, self.graph_x_max, dummy, self.graph_x_step, dummy, self.graph_x_unit, self.grap_x_calc_button, self.sizer_graph_x = return_min_max_step_labeled(self, "X Axes", unit = False, single_unit = True, button_text = "Calculate")
        
        self.graph_y_label, dummy, dummy, self.sizer_graph_y_label, dummy, dummy = return_textbox_labeled(self, "Y Axes label", enabled=False, enable_text="Auto")
        self.graph_y_min, dummy, self.graph_y_max, dummy, self.graph_y_step, dummy, self.graph_y_unit, self.grap_y_calc_button, self.sizer_graph_y = return_min_max_step_labeled(self, "Y Axes", unit = False, single_unit = True, button_text = "Calculate")

        if z_axes:
            self.graph_z_label, dummy, dummy, self.sizer_graph_z_label, dummy, dummy = return_textbox_labeled(self, "Z Axes label", enabled=False, enable_text="Auto")
            self.graph_z_min, dummy, self.graph_z_max, dummy, self.graph_z_step, dummy, self.graph_z_unit, self.grap_z_calc_button, self.sizer_graph_z = return_min_max_step_labeled(self, "Z Axes", unit = False, single_unit = True, button_text = "Calculate")

        if animated:
            self.graph_animated, self.sizer_graph_animated = return_checkbox_labeled(self, "Animate Graph")


class TabPanelIP1PlotGraph(XYPlotGraphPanelClass):
    """
    Tab for Plot IP1 Graph
    """
    
    def __init__(self, parent):
        
        XYPlotGraphPanelClass.__init__(self, parent=parent, animated = True)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.plot_button, self.sizer_plot_button = return_simple_button(self, "Plot Graph", "Start")
        self.plot_button.Bind(wx.EVT_BUTTON, self.OnPlotGraph)
        #input Data File
        #Graph Title

        self.graph_x_label.ChangeValue("Input Power (dBm)")
        self.graph_y_label.ChangeValue("Output Power (dBm)")

        sizer.Add(self.sizer_data_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_title, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_animated, 0, wx.ALL, 5)
        sizer.Add(self.sizer_plot_button, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
    
    def OnPlotGraph(self, event):
        data_file_name = self.data_file_name.GetValue()
        if check_value_is_valid_file(data_file_name, "Data IP1 file") == 0:
            return None
        
        graph_title = self.graph_title.GetValue()
        graph_x_label = self.graph_x_label.GetValue()
        #graph_x_label_auto = self.graph_x_label_auto.GetValue()
        graph_x_min = self.graph_x_min.GetValue()
        if check_value_min_max(graph_x_min, "Graph X min", minimum = None) == 0:
            return None
        else:
            graph_x_min = eval(self.graph_x_min.GetValue())
        #graph_x_min_auto = self.graph_x_min_auto.GetValue()
        
        graph_x_max = self.graph_x_max.GetValue()
        if check_value_min_max(graph_x_max, "Graph X max", minimum = None) == 0:
            return None
        else:
            graph_x_max = eval(self.graph_x_max.GetValue())
        #graph_x_max_auto = self.graph_x_max_auto.GetValue()
        graph_x_step = self.graph_x_step.GetValue()
        if check_value_min_max(graph_x_step, "Graph X step", minimum = 0) == 0:
            return None
        else:
            graph_x_step = eval(self.graph_x_step.GetValue())
        #graph_x_step_auto = self.graph_x_step_auto.GetValue()
        graph_x_unit = unit.return_unit(self.graph_x_unit.GetValue()) or unit.MHz
        
        
        graph_y_label = self.graph_y_label.GetValue()
        #graph_y_label_auto = self.graph_y_label_auto.GetValue()
        
        graph_y_min = self.graph_y_min.GetValue()
        if check_value_min_max(graph_y_min, "Graph Y min", minimum = None) == 0:
            return None
        else:
            graph_y_min = eval(self.graph_y_min.GetValue())
        #graph_y_min_auto = self.graph_y_min_auto.GetValue()
        graph_y_max = self.graph_y_max.GetValue()
        if check_value_min_max(graph_y_max, "Graph Y max", minimum = None) == 0:
            return None
        else:
            graph_y_max = eval(self.graph_y_max.GetValue())
        #graph_y_max_auto = self.graph_y_max_auto.GetValue()
        graph_y_step = self.graph_y_step.GetValue()
        if check_value_min_max(graph_y_step, "Graph Y step", minimum = 0) == 0:
            return None
        else:
            graph_y_step = eval(self.graph_y_step.GetValue())
        #graph_y_step_auto = self.graph_y_step_auto.GetValue()
        graph_y_unit = unit.return_unit(self.graph_y_unit.GetValue()) or unit.MHz
        
        graph_animated = self.graph_animated.GetValue()
        
        dlg = wx.TextEntryDialog(self, "Insert Spurius Frequencies (MHz) - comma separated")
        dlg.ShowModal()
        result = dlg.GetValue()
        dlg.Destroy()
        IF_Frequency_selected = eval("[" + result + "]")
        IF_Frequency_selected = [unit.convertion_to_base(x, unit.MHz) for x in IF_Frequency_selected]
        
        current_font_style = self.Parent.GrandParent.get_selected_settings()
        
        graph_x = Graph_Axis_Range(graph_x_min, graph_x_max, graph_x_step, graph_x_unit, graph_x_label)
        graph_x.to_base()
        
        graph_y = Graph_Axis_Range(graph_y_min, graph_y_max, graph_y_step, graph_y_unit, graph_y_label)
        graph_y.to_base()
        
        calculate_all_IP1(data_file_name, 
                          graph_title, 
                          graph_x,
                          graph_y, 
                          IF_Frequency_selected,
                          graph_animated,
                          font_style = current_font_style)
        #self.instrument_label.SetLabel(response)


class TabPanelSpuriusCPlotGraph(XYPlotGraphPanelClass):
    """
    Tab for Plot IP1 Graph
    """
    
    def __init__(self, parent):
        
        XYPlotGraphPanelClass.__init__(self, parent=parent, animated = False, z_axes = True)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.graph_type, self.sizer_graph_type = return_comboBox(self, "Graph type", choices_list = graph_types.keys())

        self.plot_button, self.sizer_plot_button = return_simple_button(self, "Plot Graph", "Start")
        self.plot_button.Bind(wx.EVT_BUTTON, self.OnPlotGraph)
        self.x_index = 0
        self.y_index = 0
        self.z_index = 0
        self.row_data_filter = []
        self.grap_y_calc_button.param_to_calc = {"combobox": "self.graph_y_unit", 
                                                 "index" : "self.y_index", 
                                                 "textbox_min" : "self.graph_y_min", 
                                                 "textbox_max" : "self.graph_y_max", 
                                                 "filter" : "self.row_data_filter", 
                                                 "unit_index" : "self.y_unit_index"}
        self.grap_x_calc_button.param_to_calc = {"combobox": "self.graph_x_unit", 
                                                 "index" : "self.x_index", 
                                                 "textbox_min" : "self.graph_x_min", 
                                                 "textbox_max" : "self.graph_x_max", 
                                                 "filter" : "self.row_data_filter", 
                                                 "unit_index" : "self.x_unit_index"}
        self.grap_z_calc_button.param_to_calc = {"combobox": "self.graph_z_unit", 
                                                 "index" : "self.z_index", 
                                                 "textbox_min" : "self.graph_z_min", 
                                                 "textbox_max" : "self.graph_z_max", 
                                                 "filter" : "self.row_data_filter", 
                                                 "unit_index" : "self.z_unit_index"}
        #self.grap_x_max_calc_button.param_to_calc = {"combobox": "self.graph_x_unit", "type": "max", "index" : "self.x_index", "textbox" : "self.graph_x_max", "filter" : "self.row_data_filter", "unit_index" : "self.x_unit_index"}
        
        
        self.grap_y_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        self.grap_x_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        self.grap_z_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        #self.grap_x_max_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        #input Data File
        #Graph Title
        

        self.graph_x_label.ChangeValue("IF Frequency ({unit})")
        self.graph_x_min.ChangeValue("100")
        self.graph_x_max.ChangeValue("3000")
        self.graph_x_step.ChangeValue("100")
        self.graph_y_label.ChangeValue("IF Power Loss ({unit})")
        self.graph_y_min.ChangeValue("-20")
        self.graph_y_max.ChangeValue("0")
        self.graph_y_step.ChangeValue("2")

        sizer.Add(self.sizer_data_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_type, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_title, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_z_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_z, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_graph_animated, 0, wx.ALL, 5)
        sizer.Add(self.sizer_plot_button, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
    
    def check_values(self):
        self.data_file_name_value = self.data_file_name.GetValue()
        
        if check_value_is_valid_file(self.data_file_name_value, "Data Spurius file") == 0:
            return 0
        
        self.graph_type_value = self.graph_type.GetValue()
        if self.graph_type_value in graph_types.keys():
            self.graph_type_value = graph_types[self.graph_type_value]
        else:
            error_message("Graph type not selected", "Graph type error")
            return 0
        
        
    
    def OnCalcAuto(self, event):
        
        button = event.GetEventObject()

        param_to_calc = button.param_to_calc #{"type": "max", "index" : "self.x_index", "textbox" : "self.graph_y_max", "unit_index" : "self.x_unit_index",}

        m = []
        tmp_unit = unit.return_unit_str(unit.dBm) 
        for row in self.return_list_of_row():
            for d in row:
                if self.check_filter(d, eval(param_to_calc["filter"])):
                    m.append(d[eval(param_to_calc["index"])])
                    if eval(param_to_calc["unit_index"]) is not None:
                        tmp_unit = unit.return_unit_str(d[eval(param_to_calc["unit_index"])])
        if len(m) > 0:
            eval(param_to_calc["textbox_max"]).ChangeValue(str(max(m)))
            eval(param_to_calc["textbox_min"]).ChangeValue(str(min(m)))
            eval(param_to_calc["combobox"]).SetSelection(unit.return_unit_index(tmp_unit))
    
    def check_filter(self, row, row_filter):
        result = True
        for f in row_filter:
            index = f[0]
            filter_type = f[1]
            filter_value = f[2]
            if filter_type == "in":
                if row[index] in filter_value:
                    pass
                else:
                    return False
            elif filter_type == "not in":
                if row[index] not in filter_value:
                    pass
                else:
                    return False
        return result
    
    def return_list_of_row(self):
        if self.check_values() == 0:
            return []
        
        IF_Frequency_selected = [0]
        SD_LO_Frequency = 0
        SD_LO_Level = 0
        SD_RF_Level = 0
        graph_z_min = 0

        if self.graph_type_value == "LO":
            self.x_index = frequency_IF_index
            self.x_unit_index = unit_IF_index
            self.y_index = conversion_loss
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            self.row_data_filter = [(n_LO_index, "in", [1, -1]), (m_RF_index, "in", [1, -1])]
        elif self.graph_type_value == "RF":
            self.x_index = power_RF_index
            self.x_unit_index = None
            self.y_index = power_IF_index
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            self.row_data_filter = [(n_LO_index, "in", [1, -1]), (m_RF_index, "in", [1, -1])]
        elif self.graph_type_value == "SP":
            self.x_index = power_RF_index
            self.x_unit_index = None
            self.y_index = power_IF_index
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            dlg = wx.TextEntryDialog(self, "Insert Spurius Frequencies (MHz) - comma separated")
            dlg.ShowModal()
            result = dlg.GetValue()
            dlg.Destroy()
            IF_Frequency_selected = eval("[" + result + "]")
            IF_Frequency_selected = [unit.convertion_to_base(x, unit.MHz) for x in IF_Frequency_selected]
            self.row_data_filter = [(n_LO_index, "not in", [1, -1]), (m_RF_index, "not in", [1, -1])]
        elif self.graph_type_value == "SD":
            self.x_index = frequency_IF_index
            self.x_unit_index = unit_IF_index
            self.y_index = power_IF_index
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            graph_z_min = self.graph_z_min.GetValue()
            if check_value_min_max(graph_z_min, "Graph Z min", minimum = None) == 0:
                return []
            else:
                graph_z_min = eval(self.graph_z_min.GetValue())
            dlg = wx.TextEntryDialog(self, "Insert LO Frequency (MHz)")
            dlg.ShowModal()
            SD_LO_Frequency = dlg.GetValue()
            dlg.Destroy()
            SD_LO_Frequency = unit.convertion_to_base(eval(SD_LO_Frequency), unit.MHz)
            dlg = wx.TextEntryDialog(self, "Insert LO Level (dBm)")
            dlg.ShowModal()
            SD_LO_Level = dlg.GetValue()
            dlg.Destroy()
            SD_LO_Level = eval(SD_LO_Level)
            dlg = wx.TextEntryDialog(self, "Insert RF Level (dBm)")
            dlg.ShowModal()
            SD_RF_Level = dlg.GetValue()
            dlg.Destroy()
            SD_RF_Level = eval(SD_RF_Level)
            self.row_data_filter = [(n_LO_index, "not in", [1, -1]), (m_RF_index, "not in", [1, -1])]
        data_table, dummy, dummy, dummy, dummy, dummy, dummy = order_and_group_data(data_file_name = self.data_file_name_value, 
                       graph_type = self.graph_type_value, 
                       SD_LO_Frequency = SD_LO_Frequency,
                       SD_LO_Level = SD_LO_Level,
                       SD_RF_Level = SD_RF_Level,
                       SD_IF_Min_Level = graph_z_min,
                       IF_Frequency_selected = IF_Frequency_selected, 
                       savefile = False)
        return data_table

    
    def OnPlotGraph(self, event):
        result = [0]
        if self.check_values() == 0:
            return 0
        graph_title = self.graph_title.GetValue()
        graph_x_label = self.graph_x_label.GetValue()
        #graph_x_label_auto = self.graph_x_label_auto.GetValue()
        graph_x_min = self.graph_x_min.GetValue()
        if check_value_min_max(graph_x_min, "Graph X min", minimum = None) == 0:
            return None
        else:
            graph_x_min = eval(self.graph_x_min.GetValue())
        #graph_x_min_auto = self.graph_x_min_auto.GetValue()
        
        graph_x_max = self.graph_x_max.GetValue()
        if check_value_min_max(graph_x_max, "Graph X max", minimum = None) == 0:
            return None
        else:
            graph_x_max = eval(self.graph_x_max.GetValue())
        #graph_x_max_auto = self.graph_x_max_auto.GetValue()
        graph_x_step = self.graph_x_step.GetValue()
        if check_value_min_max(graph_x_step, "Graph X step", minimum = 0) == 0:
            return None
        else:
            graph_x_step = eval(self.graph_x_step.GetValue())
        #graph_x_step_auto = self.graph_x_step_auto.GetValue()
        graph_x_unit = unit.return_unit(self.graph_x_unit.GetValue()) or unit.Hz
        
        graph_x = Graph_Axis_Range(graph_x_min, graph_x_max, graph_x_step, graph_x_unit, graph_x_label)
        graph_x.to_base()
        
        
        #graph_y_label_auto = self.graph_y_label_auto.GetValue()
        
        if check_steps_count("X steps", minimum = graph_x_min, maximum = graph_x_max, steps=graph_x_step, counter = 50) == 0:
            return 0
        
        graph_y_label = self.graph_y_label.GetValue()
        
        graph_y_min = self.graph_y_min.GetValue()
        if check_value_min_max(graph_y_min, "Graph Y min", minimum = None) == 0:
            return None
        else:
            graph_y_min = eval(self.graph_y_min.GetValue())
        #graph_y_min_auto = self.graph_y_min_auto.GetValue()
        graph_y_max = self.graph_y_max.GetValue()
        if check_value_min_max(graph_y_max, "Graph Y max", minimum = None) == 0:
            return None
        else:
            graph_y_max = eval(self.graph_y_max.GetValue())
        #graph_y_max_auto = self.graph_y_max_auto.GetValue()
        graph_y_step = self.graph_y_step.GetValue()
        if check_value_min_max(graph_y_step, "Graph Y step", minimum = 0) == 0:
            return None
        else:
            graph_y_step = eval(self.graph_y_step.GetValue())
        #graph_y_step_auto = self.graph_y_step_auto.GetValue()
        
        graph_y_unit = unit.return_unit(self.graph_y_unit.GetValue()) or unit.Hz
        
        graph_y = Graph_Axis_Range(graph_y_min, graph_y_max, graph_y_step, graph_y_unit, graph_y_label)
        graph_y.to_base()
        
        graph_z_label = self.graph_z_label.GetValue()
        
        if self.graph_type_value == "SD":
            graph_z_min = self.graph_z_min.GetValue()
            if check_value_min_max(graph_z_min, "Graph Z min", minimum = None) == 0:
                return None
            else:
                graph_z_min = eval(self.graph_z_min.GetValue())
            graph_z_max = self.graph_z_max.GetValue()
            if check_value_min_max(graph_z_max, "Graph Z max", minimum = None) == 0:
                return None
            else:
                graph_z_max = eval(self.graph_z_max.GetValue())
            graph_z_step = self.graph_z_step.GetValue()
            if check_value_min_max(graph_z_step, "Graph Z step", minimum = 0) == 0:
                return None
            else:
                graph_z_step = eval(self.graph_z_step.GetValue())
            
            graph_z_unit = unit.return_unit(self.graph_z_unit.GetValue()) or unit.Hz
            
            graph_z = Graph_Axis_Range(graph_z_min, graph_z_max, graph_z_step, graph_z_unit, graph_z_label)
            graph_z.to_base()
            
            if check_steps_count("Z steps", minimum = graph_z_min, maximum = graph_z_max, steps=graph_z_step, counter = 50) == 0:
                return 0
        else:
            graph_z = Graph_Axis_Range(0, 0, 0, unit.Hz, "")
        
        IF_Frequency_selected = [0]
        SD_LO_Frequency = 0
        SD_LO_Level = 0
        SD_RF_Level = 0
        if self.graph_type_value == "SP":
            dlg = wx.TextEntryDialog(self, "Insert Spurius Frequencies (MHz) - comma separated")
            dlg.ShowModal()
            result = dlg.GetValue()
            dlg.Destroy()
            IF_Frequency_selected = eval("[" + result + "]")
            IF_Frequency_selected = [unit.convertion_to_base(x, unit.MHz) for x in IF_Frequency_selected]
        elif self.graph_type_value == "SD":
            dlg = wx.TextEntryDialog(self, "Insert LO Frequency (MHz)")
            dlg.ShowModal()
            SD_LO_Frequency = dlg.GetValue()
            dlg.Destroy()
            dlg = wx.TextEntryDialog(self, "Insert LO Level (dBm)")
            dlg.ShowModal()
            SD_LO_Level = dlg.GetValue()
            dlg.Destroy()
            dlg = wx.TextEntryDialog(self, "Insert RF Level (dBm)")
            dlg.ShowModal()
            SD_RF_Level = dlg.GetValue()
            dlg.Destroy()
            SD_LO_Frequency = unit.convertion_to_base(eval(SD_LO_Frequency), unit.MHz) 
            SD_LO_Level = eval(SD_LO_Level)
            SD_RF_Level = eval(SD_RF_Level)
        
        current_font_style = self.Parent.GrandParent.get_selected_settings()
        
        
        for frequency_IF_filter  in IF_Frequency_selected:
            result_folder = plot_spurius_graph(self.data_file_name_value, 
                           self.graph_type_value, 
                           graph_title, 
                           graph_x,
                           graph_y,
                           graph_z,
                           SD_LO_Frequency = SD_LO_Frequency,
                           SD_LO_Level = SD_LO_Level,
                           SD_RF_Level = SD_RF_Level,
                           IF_Frequency_selected = frequency_IF_filter,
                           font_style = current_font_style)
            
        try:
            last_svg = ""
            for svg_file in buildfitsfileslist(result_folder):
                last_svg = svg_file
                execute = [inkscape_exec, "-f", svg_file, '-M',  svg_file[:-4] + '.emf']
                print("saving " + svg_file[:-4] + '.emf')
                subprocess.call(execute)
        except:
            print("Error saving " + last_svg)
        try:
            if self.graph_type_value != "SD":
                webbrowser.open(result_folder)
        except:
            pass
        #self.instrument_label.SetLabel(response)
        
        #webbrowser.open('/home/test/test_folder')


class TabPanelGenericPlotGraph(XYPlotGraphPanelClass):
    """
    Tab for Plot IP1 Graph
    """
    
    def __init__(self, parent):
        
        XYPlotGraphPanelClass.__init__(self, parent=parent, animated = False, z_axes = False, input_file_wildcard = "*.txt")
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.graph_type, self.sizer_graph_type = return_comboBox(self, "Graph type", choices_list = generic_graph_types.keys())

        self.plot_button, self.sizer_plot_button = return_simple_button(self, "Plot Graph", "Start")
        self.plot_button.Bind(wx.EVT_BUTTON, self.OnPlotGraph)
        self.x_index = 0
        self.y_index = 0
        #self.z_index = 0
        self.row_data_filter = []
        self.grap_y_calc_button.param_to_calc = {"combobox": "self.graph_y_unit", "index" : "self.y_index", "textbox_min" : "self.graph_y_min", "textbox_max" : "self.graph_y_max", "filter" : "self.row_data_filter", "unit_index" : "self.y_unit_index"}
        self.grap_x_calc_button.param_to_calc = {"combobox": "self.graph_x_unit", "index" : "self.x_index", "textbox_min" : "self.graph_x_min", "textbox_max" : "self.graph_x_max", "filter" : "self.row_data_filter", "unit_index" : "self.x_unit_index"}
        #self.grap_z_calc_button.param_to_calc = {"combobox": "self.graph_z_unit", "index" : "self.z_index", "textbox_min" : "self.graph_z_min", "textbox_max" : "self.graph_z_max", "filter" : "self.row_data_filter", "unit_index" : "self.z_unit_index"}
        #self.grap_x_max_calc_button.param_to_calc = {"combobox": "self.graph_x_unit", "type": "max", "index" : "self.x_index", "textbox" : "self.graph_x_max", "filter" : "self.row_data_filter", "unit_index" : "self.x_unit_index"}
        
        
        self.grap_y_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        self.grap_x_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        #self.grap_z_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        #self.grap_x_max_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        #input Data File
        #Graph Title
        

        self.graph_x_label.ChangeValue("IF Frequency ({unit})")
        self.graph_x_min.ChangeValue("100")
        self.graph_x_max.ChangeValue("3000")
        self.graph_x_step.ChangeValue("100")
        self.graph_y_label.ChangeValue("IF Power Loss (dBm)")
        self.graph_y_min.ChangeValue("-20")
        self.graph_y_max.ChangeValue("0")
        self.graph_y_step.ChangeValue("2")

        sizer.Add(self.sizer_data_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_type, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_title, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_graph_z_label, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_graph_z, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_graph_animated, 0, wx.ALL, 5)
        sizer.Add(self.sizer_plot_button, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
    
    def check_values(self):
        self.data_file_name_value = self.data_file_name.GetValue()
        
        if check_value_is_valid_file(self.data_file_name_value, "Generic graph data file") == 0:
            return 0
        
        self.graph_type_value = self.graph_type.GetValue()
        if self.graph_type_value in generic_graph_types.keys():
            self.graph_type_value = generic_graph_types[self.graph_type_value]
        else:
            error_message("Graph type not selected", "Graph type error")
            return 0
        
    def OnCalcAuto(self, event):
        pass
        #button = event.GetEventObject()

        #param_to_calc = button.param_to_calc #{"type": "max", "index" : "self.x_index", "textbox" : "self.graph_y_max", "unit_index" : "self.x_unit_index",}

        #m = []
        #tmp_unit = unit.return_unit_str(unit.MHz) 
        #for row in self.return_list_of_row():
        #    for d in row:
        #        if self.check_filter(d, eval(param_to_calc["filter"])):
        #            m.append(d[eval(param_to_calc["index"])])
        #            if eval(param_to_calc["unit_index"]) is not None:
        #                tmp_unit = unit.return_unit_str(d[eval(param_to_calc["unit_index"])])
        #if len(m) > 0:
        #    eval(param_to_calc["textbox_max"]).ChangeValue(str(max(m)))
        #    eval(param_to_calc["textbox_min"]).ChangeValue(str(min(m)))
        #    eval(param_to_calc["combobox"]).SetSelection(unit.return_unit_index(tmp_unit))
    
    def check_filter(self, row, row_filter):
        result = True
        for f in row_filter:
            index = f[0]
            filter_type = f[1]
            filter_value = f[2]
            if filter_type == "in":
                if row[index] in filter_value:
                    pass
                else:
                    return False
            elif filter_type == "not in":
                if row[index] not in filter_value:
                    pass
                else:
                    return False
        return result
    
    def return_list_of_row(self):
        if self.check_values() == 0:
            return []
        
        IF_Frequency_selected = [0]
        SD_LO_Frequency = 0
        SD_LO_Level = 0
        SD_RF_Level = 0

        if self.graph_type_value == "GG":
            self.x_index = frequency_IF_index
            self.x_unit_index = unit_IF_index
            self.y_index = conversion_loss
            self.y_unit_index = None
            self.row_data_filter = [(n_LO_index, "in", [1, -1]), (m_RF_index, "in", [1, -1])]
        
        data_table, dummy, dummy, dummy, dummy, dummy, dummy = order_and_group_data(data_file_name = self.data_file_name_value, 
                       graph_type = self.graph_type_value, 
                       SD_LO_Frequency = SD_LO_Frequency,
                       SD_LO_Level = SD_LO_Level,
                       SD_RF_Level = SD_RF_Level,
                       SD_IF_Min_Level = None,
                       IF_Frequency_selected = IF_Frequency_selected, 
                       savefile = False)
        return data_table

    
    def OnPlotGraph(self, event):
        result = [0]
        if self.check_values() == 0:
            return 0
        graph_title = self.graph_title.GetValue()
        graph_x_label = self.graph_x_label.GetValue()
        #graph_x_label_auto = self.graph_x_label_auto.GetValue()
        graph_x_min = self.graph_x_min.GetValue()
        if check_value_min_max(graph_x_min, "Graph X min", minimum = None) == 0:
            return None
        else:
            graph_x_min = eval(self.graph_x_min.GetValue())
        #graph_x_min_auto = self.graph_x_min_auto.GetValue()
        
        graph_x_max = self.graph_x_max.GetValue()
        if check_value_min_max(graph_x_max, "Graph X max", minimum = None) == 0:
            return None
        else:
            graph_x_max = eval(self.graph_x_max.GetValue())
        #graph_x_max_auto = self.graph_x_max_auto.GetValue()
        graph_x_step = self.graph_x_step.GetValue()
        if check_value_min_max(graph_x_step, "Graph X step", minimum = 0) == 0:
            return None
        else:
            graph_x_step = eval(self.graph_x_step.GetValue())
        #graph_x_step_auto = self.graph_x_step_auto.GetValue()
        graph_x_unit = unit.return_unit(self.graph_x_unit.GetValue()) or unit.MHz
        
        graph_x = Graph_Axis_Range(graph_x_min, graph_x_max, graph_x_step, graph_x_unit, graph_x_label)
        
        
        
        #graph_y_label_auto = self.graph_y_label_auto.GetValue()
        
        if check_steps_count("X steps", minimum = graph_x_min, maximum = graph_x_max, steps=graph_x_step, counter = 50) == 0:
            return 0
        
        graph_y_label = self.graph_y_label.GetValue()
        
        graph_y_min = self.graph_y_min.GetValue()
        if check_value_min_max(graph_y_min, "Graph Y min", minimum = None) == 0:
            return None
        else:
            graph_y_min = eval(self.graph_y_min.GetValue())
        #graph_y_min_auto = self.graph_y_min_auto.GetValue()
        graph_y_max = self.graph_y_max.GetValue()
        if check_value_min_max(graph_y_max, "Graph Y max", minimum = None) == 0:
            return None
        else:
            graph_y_max = eval(self.graph_y_max.GetValue())
        #graph_y_max_auto = self.graph_y_max_auto.GetValue()
        graph_y_step = self.graph_y_step.GetValue()
        if check_value_min_max(graph_y_step, "Graph Y step", minimum = 0) == 0:
            return None
        else:
            graph_y_step = eval(self.graph_y_step.GetValue())
        #graph_y_step_auto = self.graph_y_step_auto.GetValue()
        
        graph_y_unit = unit.return_unit(self.graph_y_unit.GetValue()) or unit.MHz
        
        graph_y = Graph_Axis_Range(graph_y_min, graph_y_max, graph_y_step, graph_y_unit, graph_y_label)
        
        graph_z = Graph_Axis_Range(0, 0, 0, unit.MHz, "")
        
        IF_Frequency_selected = [0]
        SD_LO_Frequency = 0
        SD_LO_Level = 0
        SD_RF_Level = 0

        current_font_style = self.Parent.GrandParent.get_selected_settings()

        result_folder = plot_spurius_graph(self.data_file_name_value, 
                       self.graph_type_value, 
                       graph_title, 
                       graph_x,
                       graph_y,
                       graph_z,
                       SD_LO_Frequency = SD_LO_Frequency,
                       SD_LO_Level = SD_LO_Level,
                       SD_RF_Level = SD_RF_Level,
                       IF_Frequency_selected = 0,
                       font_style = current_font_style)
            
        try:
            last_svg = ""
            for svg_file in buildfitsfileslist(result_folder):
                last_svg = svg_file
                execute = [inkscape_exec, "-f", svg_file, '-M',  svg_file[:-4] + '.emf']
                print("saving " + svg_file[:-4] + '.emf')
                subprocess.call(execute)
        except:
            print("Error saving " + last_svg)
        try:
            if self.graph_type_value != "SD":
                webbrowser.open(result_folder)
        except:
            pass
        #self.instrument_label.SetLabel(response)
        
        #webbrowser.open('/home/test/test_folder')


class TabPanelSAB(InstrumentPanelClass):
    """
    Tab for Power Meter
    """
    
    def __init__(self, parent, attenutation = True, switches = True):
        
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #power_meter_state = "ON"
        #self.SAB_state, self.sizer_SAB_state = return_checkbox_labeled(self, "State")

        if attenutation:
            self.SAB_attenuation_min, dummy, self.SAB_attenuation_max, dummy, self.SAB_attenuation_step, dummy, dummy, dummy, self.sizer_SAB_attenuation = return_min_max_step_labeled(self, "Attenuation", unit = False)
            self.SAB_attenuation_delay, dummy, dummy, self.sizer_SAB_attenuation_delay, dummy, dummy = return_textbox_labeled(self, "Attenuation Delay")
        
        if switches:
            #power_meter_misure_delay = 1 #seconds
            self.SAB_switch01_delay, dummy, dummy, self.sizer_SAB_switch01_delay, dummy, dummy = return_textbox_labeled(self, "Switch 1 delay (s)")
            
            self.SAB_switch02_delay, dummy, dummy, self.sizer_SAB_switch02_delay, dummy, dummy = return_textbox_labeled(self, "Switch 2 delay (s)")
            
            self.SAB_switch03_delay, dummy, dummy, self.sizer_SAB_switch03_delay, dummy, dummy = return_textbox_labeled(self, "Switch 3 delay (s)")

        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_enable_status_sizer, 0, wx.ALL, 5)
        if attenutation:
            sizer.Add(self.sizer_SAB_attenuation, 0, wx.ALL, 5)
            sizer.Add(self.sizer_SAB_attenuation_delay, 0, wx.ALL, 5)
        if switches:
            sizer.Add(self.sizer_SAB_switch01_delay, 0, wx.ALL, 5)
            sizer.Add(self.sizer_SAB_switch02_delay, 0, wx.ALL, 5)
            sizer.Add(self.sizer_SAB_switch03_delay, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
        

class TabPanelTSC(InstrumentPanelClass):
    """
    Tab for Phase Noise Test TSC5120A/TSC5115A
    """
    
    def __init__(self, parent):
        
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #power_meter_state = "ON"
        #self.TSC_state, self.sizer_TSC_state = return_checkbox_labeled(self, "State")

        self.TSC_collecting_delay, dummy, dummy, self.sizer_TSC_collecting_delay, dummy, dummy = return_textbox_labeled(self, "Collecting time (m)")
        
        self.TSC_plot_adev, self.sizer_TSC_plot_adev = return_checkbox_labeled(self, "Plot Allan Deviation")
        
        self.result_file_name, self.result_file_name_button, dummy, self.sizer_result_file_name = return_file_browse(self, "Output Path")
        self.result_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_Out)
        
        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_enable_status_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_TSC_collecting_delay, 0, wx.ALL, 5)
        sizer.Add(self.sizer_TSC_plot_adev, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
        
        self.SetSizer(sizer)
        
    def File_browser_Out(self, event):
        #dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*", wx.SAVE)
        dlg = wx.DirDialog(self, "Choose a directory:",style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.result_file_name.SetValue(path)
        else:
            self.result_file_name.SetValue("")
        dlg.Destroy()

class TabPanelPowerMeter(InstrumentPanelClass):
    """
    Tab for Power Meter
    """
    
    def __init__(self, parent):
        
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        
        #power_meter_state = "ON"
        #self.power_meter_state, self.sizer_power_meter_state = return_checkbox_labeled(self, "State")

        #power_meter_misure_number = 1
        self.power_meter_misure_number, self.sizer_power_meter_misure_number = return_spinctrl(self, "Measures")
        
        #power_meter_misure_delay = 1 #seconds
        self.power_meter_misure_delay, dummy, dummy, self.sizer_power_meter_misure_delay, dummy, dummy = return_textbox_labeled(self, "Measure delay (s)")

        self.power_meter_make_zero, self.sizer_power_meter_make_zero = return_checkbox_labeled(self, "Make Zero")

        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_enable_status_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_power_meter_misure_number, 0, wx.ALL, 5)
        sizer.Add(self.sizer_power_meter_misure_delay, 0, wx.ALL, 5)
        sizer.Add(self.sizer_power_meter_make_zero, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)