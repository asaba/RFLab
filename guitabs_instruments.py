'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os

from guiobjects import return_file_browse, return_instrument, return_test_instrument, return_min_max_step_labeled, return_usb_instrument, return_checkbox_labeled, return_comboBox_unit, return_textbox_labeled, return_spinctrl
from utilitygui import check_value_min_max, check_value_not_none, check_value_is_IP, create_instrument, check_instrument_comunication, check_USB_instrument_comunication
from measure_scripts.plotIP1graph import unit
from measure_scripts.csvutility import *
import matplotlib.pyplot as plt
from measure_scripts.graphutility import Graph_Axis_Range
import serial.tools.list_ports
from utility import return_max_min_from_data_table_row
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