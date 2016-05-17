'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os

from guiobjects import return_checkbox_labeled, return_spinctrl, return_textbox_labeled, return_comboBox_unit, return_file_browse, return_instrument, return_test_instrument, return_simple_button, return_min_max_step_labeled
from utilitygui import check_instrument_comunication
from utilitygui import check_value_is_valid_file, check_value_min_max
from measure_scripts.plotIP1graph import calculate_all_IP1


class InstrumentPanelClass(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.instrument_txt_IP, self.instrument_txt_Port, self.instrument_txt_Timeout, self.combobox_instrtype, self.instrument_sizer = return_instrument(self)
        self.instrument_test_button, self.instrument_label, self.instrument_test_sizer  = return_test_instrument(self)
        self.instrument_test_button.Bind(wx.EVT_BUTTON, self.OnTestInstrument)
    
    def OnTestInstrument(self, event):
        dummy, response = check_instrument_comunication(self.instrument_txt_IP.GetValue(), self.instrument_txt_Port.GetValue(), eval(self.instrument_txt_Timeout.GetValue()), self.combobox_instrtype.GetValue())
        self.instrument_label.SetLabel(response)

class SetupPanelClass(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.result_file_name, self.result_file_name_button, self.sizer_result_file_name = return_file_browse(self, "Output File")
        self.result_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_Out)
    
    def File_browser_Out(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.result_file_name.SetValue(path)
        else:
            self.result_file_name.SetValue("")
        dlg.Destroy()
        
class PlotGraphPanelClass(wx.Panel):
    
    #input Data File
    #Graph Title
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_file_name, self.data_file_name_button, self.sizer_data_file_name = return_file_browse(self, "Data File")
        self.data_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_DataFile)
        
        #Graph Title
        self.graph_title, dummy, dummy, self.sizer_graph_title, dummy, dummy = return_textbox_labeled(self, "Graph title")
        
    
    def File_browser_DataFile(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.data_file_name.SetValue(path)
        else:
            self.data_file_name.SetValue("")
        
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
        
        self.frequency_min, self.frequency_min_unit, self.frequency_max, self.frequency_max_unit, self.frequency_step, self.frequency_step_unit, self.sizer_frequency = return_min_max_step_labeled(self, "Frequency", unit = True)
        
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
        
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
        

class TabPanelIP1CalcSetup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #IP1 calculation variables

        self.calibration_file_RF, self.calibration_file_RF_button, self.sizer_calibration_file_RF = return_file_browse(self, "Radio Frequency Cable Calibration File")
        self.calibration_file_RF_button.Bind(wx.EVT_BUTTON, self.File_browser_RF)
        

        sizer.Add(self.sizer_calibration_file_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
        
    def File_browser_RF(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.calibration_file_RF.SetValue(path)
        else:
            self.calibration_file_RF.SetValue("")
        

class TabPanelSpuriusSetup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """
    
    def __init__(self, parent):
        
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #spurius calculation variables

        #m_max_RF = 7
        self.m_max_RF, self.sizer_m_max_RF = return_spinctrl(self, "Max m for RF")
        
        #n_max_LO = 7
        self.n_max_LO, self.sizer_n_max_LO = return_spinctrl(self, "Max n for LO")
        
        #IF_high = 3000
        self.IF_high, self.IF_high_unit, dummy, self.sizer_IF_high, dummy, dummy = return_textbox_labeled(self, "Max Spurius Frequency", unit = True)
        
        #spurius_IF_unit = unit.MHz
        self.spurius_IF_unit, self.sizer_spurius_IF_unit = return_comboBox_unit(self, "Spurius Frequency unit")
        
        #calibration_file_LO = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_LO, self.calibration_file_LO_button, self.sizer_calibration_file_LO = return_file_browse(self, "Local Ocillator Cable Calibration File")
        self.calibration_file_LO_button.Bind(wx.EVT_BUTTON, self.File_browser_LO)
        
        #calibration_file_RF = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_RF, self.calibration_file_RF_button, self.sizer_calibration_file_RF = return_file_browse(self, "Radio Frequency Cable Calibration File")
        self.calibration_file_RF_button.Bind(wx.EVT_BUTTON, self.File_browser_RF)

        #calibration_file_IF = ""
        self.calibration_file_IF, self.calibration_file_IF_button, self.sizer_calibration_file_IF = return_file_browse(self, "Output Frequency Cable Calibration File")
        self.calibration_file_IF_button.Bind(wx.EVT_BUTTON, self.File_browser_IF)
        

        sizer.Add(self.sizer_m_max_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_n_max_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_IF_high, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_IF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spurius_IF_unit, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
    
    def File_browser_LO(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #mypath = os.path.basename(path)
            self.calibration_file_LO.SetValue(path)
        else:
            self.calibration_file_LO.SetValue("")
        
    def File_browser_RF(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.calibration_file_RF.SetValue(path)
        else:
            self.calibration_file_RF.SetValue("")
        
        
    def File_browser_IF(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.csv", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.calibration_file_IF.SetValue(path)
        else:
            self.calibration_file_IF.SetValue("")
        

class TabPanelFSV(InstrumentPanelClass):
    """
    Tab for FSV
    """
    
    def __init__(self, parent):
        
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #spectrum_analyzer_state = "ON"
        self.spectrum_analyzer_state, self.sizer_spectrum_analyzer_state = return_checkbox_labeled(self, "State")
        
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
        
        #FSV_delay = 1
        self.FSV_delay, dummy, dummy, self.sizer_FSV_delay, dummy, dummy = return_textbox_labeled(self, "Measure delay (s)")

        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_state, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_sweep_points, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_resolution_bandwidth, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_video_bandwidth, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_frequency_span, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_frequency_marker_unit, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_spectrum_analyzer_attenuation, 0, wx.ALL, 5)
        sizer.Add(self.sizer_gainAmplifier, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_IF_atten, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spectrum_analyzer_IF_relative_level, 0, wx.ALL, 5)
        sizer.Add(self.sizer_threshold_power, 0, wx.ALL, 5)
        sizer.Add(self.sizer_FSV_delay, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)


########################################################################
class TabPanelSMB(InstrumentPanelClass):
    """
    This will be the first notebook tab
    """
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """"""
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #synthetizer_LO_state = "ON"
        self.synthetizer_state, self.sizer_synthetizer_state = return_checkbox_labeled(self, "State")
        
        #synthetizer_LO_frequency_min = 4600
        ##self.synthetizer_frequency_min, self.synthetizer_frequency_min_unit, dummy, self.sizer_synthetizer_frequency_min, dummy, dummy = return_textbox_labeled(self, "Minimum Frequency", unit= True)

        #synthetizer_LO_frequency_max = 5000
        ##self.synthetizer_frequency_max, self.synthetizer_frequency_max_unit, dummy, self.sizer_synthetizer_frequency_max, dummy, dummy = return_textbox_labeled(self, "Maximum Frequency", unit= True)
        
        #synthetizer_LO_frequency_step = 200
        ##self.synthetizer_frequency_step, self.synthetizer_frequency_step_unit, dummy, self.sizer_synthetizer_frequency_step, dummy, dummy = return_textbox_labeled(self, "Frequency Step", unit= True)
        
        self.synthetizer_frequency_min, self.synthetizer_frequency_min_unit, self.synthetizer_frequency_max, self.synthetizer_frequency_max_unit, self.synthetizer_frequency_step, self.synthetizer_frequency_step_unit, self.sizer_synthetizer_frequency = return_min_max_step_labeled(self, "Frequency", unit = True)
        
        
        #synthetizer_LO_level_min = 6 #dBm
        #self.synthetizer_level_min, dummy, dummy, self.sizer_synthetizer_level_min, dummy, dummy = return_textbox_labeled(self, "Minimum Power Level")
        
        
        #synthetizer_LO_level_max = 15
        #self.synthetizer_level_max, dummy, dummy, self.sizer_synthetizer_level_max, dummy, dummy = return_textbox_labeled(self, "Mamimum Power Level")
        
        #synthetizer_LO_level_step = 3
        #self.synthetizer_level_step, dummy, dummy, self.sizer_synthetizer_level_step, dummy, dummy = return_textbox_labeled(self, "Power Level Step")
        
        self.synthetizer_level_min, dummy, self.synthetizer_level_max, dummy, self.synthetizer_level_step, dummy, self.sizer_synthetizer_level = return_min_max_step_labeled(self, "Level", unit = False)
        
        self.synthetizer_level_fixed, dummy, dummy, self.sizer_synthetizer_level_fixed, dummy, dummy = return_textbox_labeled(self, "Fixed Power Level")
        
        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_synthetizer_state, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_synthetizer_frequency_min, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_synthetizer_frequency_max, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_synthetizer_frequency_step, 0, wx.ALL, 5)
        sizer.Add(self.sizer_synthetizer_frequency, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_synthetizer_level_min, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_synthetizer_level_max, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_synthetizer_level_step, 0, wx.ALL, 5)
        sizer.Add(self.sizer_synthetizer_level, 0, wx.ALL, 5)
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
    Tab for Plot IP1 Graph
    """
    
    def __init__(self, parent):
        
        PlotGraphPanelClass.__init__(self, parent=parent)

        #Axes X Label
        #Axes X min
        #Axes X max
        #Axes X step
        #Axes Y Label
        #Axes Y min
        #Axes Y max
        #Axes Y step
        

        #power_meter_misure_number = 1
        self.graph_x_label, dummy, dummy, self.sizer_graph_x_label, dummy, dummy = return_textbox_labeled(self, "X Axes label")
        
        self.graph_x_min, dummy, dummy, self.sizer_graph_x_min, dummy, dummy = return_textbox_labeled(self, "X Axes min")
        
        self.graph_x_max, dummy, dummy, self.sizer_graph_x_max, dummy, dummy = return_textbox_labeled(self, "X Axes max")
        
        self.graph_x_step, dummy, dummy, self.sizer_graph_x_step, dummy, dummy = return_textbox_labeled(self, "X Axes step")
        
        self.graph_y_label, dummy, dummy, self.sizer_graph_y_label, dummy, dummy = return_textbox_labeled(self, "Y Axes label")
        
        self.graph_y_min, dummy, dummy, self.sizer_graph_y_min, dummy, dummy = return_textbox_labeled(self, "Y Axes min")
        
        self.graph_y_max, dummy, dummy, self.sizer_graph_y_max, dummy, dummy = return_textbox_labeled(self, "Y Axes max")
        
        self.graph_y_step, dummy, dummy, self.sizer_graph_y_step, dummy, dummy = return_textbox_labeled(self, "Y Axes step")
        
        self.graph_animated, self.sizer_graph_animated = return_checkbox_labeled(self, "Animate Graph")
        


class TabPanelIP1PlotGraph(XYPlotGraphPanelClass):
    """
    Tab for Plot IP1 Graph
    """
    
    def __init__(self, parent):
        
        XYPlotGraphPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.plot_button, self.sizer_plot_button = return_simple_button(self, "Plot Graph", "Start")
        self.plot_button.Bind(wx.EVT_BUTTON, self.OnPlotGraph)
        #input Data File
        #Graph Title

        self.graph_x_label.ChangeValue("Input Power (dBm)")
        self.graph_x_min.ChangeValue("-40")
        self.graph_x_max.ChangeValue("10")
        self.graph_x_step.ChangeValue("5")
        self.graph_y_label.ChangeValue("Output Power (dBm)")
        self.graph_y_min.ChangeValue("-30")
        self.graph_y_max.ChangeValue("20")
        self.graph_y_step.ChangeValue("5")

        sizer.Add(self.sizer_data_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_title, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_min, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_max, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_step, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_min, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_max, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_step, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_animated, 0, wx.ALL, 5)
        sizer.Add(self.sizer_plot_button, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)
    
    def OnPlotGraph(self, event):
        data_file_name = self.data_file_name.GetValue()
        if check_value_is_valid_file(data_file_name, "Data IP1 file") == 0:
            return None
        
        graph_title = self.graph_title.GetValue()
        graph_x_label = self.graph_x_label.GetValue()
        graph_x_min = self.graph_x_min.GetValue()
        if check_value_min_max(graph_x_min, "Graph X min", minimum = None) == 0:
            return None
        else:
            graph_x_min = eval(self.graph_x_min.GetValue())
        
        graph_x_max = self.graph_x_max.GetValue()
        if check_value_min_max(graph_x_max, "Graph X max", minimum = None) == 0:
            return None
        else:
            graph_x_max = eval(self.graph_x_max.GetValue())
        graph_x_step = self.graph_x_step.GetValue()
        if check_value_min_max(graph_x_step, "Graph X step", minimum = 0) == 0:
            return None
        else:
            graph_x_step = eval(self.graph_x_step.GetValue())
        graph_y_label = self.graph_y_label.GetValue()
        
        graph_y_min = self.graph_y_min.GetValue()
        if check_value_min_max(graph_y_min, "Graph Y min", minimum = None) == 0:
            return None
        else:
            graph_y_min = eval(self.graph_y_min.GetValue())
        graph_y_max = self.graph_y_max.GetValue()
        if check_value_min_max(graph_y_max, "Graph Y max", minimum = None) == 0:
            return None
        else:
            graph_y_max = eval(self.graph_y_max.GetValue())
        graph_y_step = self.graph_y_step.GetValue()
        if check_value_min_max(graph_y_step, "Graph Y step", minimum = 0) == 0:
            return None
        else:
            graph_y_step = eval(self.graph_y_step.GetValue())
            
        graph_animated = self.graph_animated.GetValue()
        
        calculate_all_IP1(data_file_name, graph_title, graph_x_label, graph_x_min, graph_x_max, graph_x_step, graph_y_label, graph_y_min, graph_y_max, graph_y_step, graph_animated)
        #self.instrument_label.SetLabel(response)


class TabPanelSAB(InstrumentPanelClass):
    """
    Tab for Power Meter
    """
    
    def __init__(self, parent):
        
        InstrumentPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        #power_meter_state = "ON"
        self.SAB_state, self.sizer_SAB_state = return_checkbox_labeled(self, "State")

        #power_meter_misure_number = 1
        #self.SAB_attenuation_min, dummy, dummy, self.sizer_SAB_attenuation_min, dummy, dummy = return_textbox_labeled(self, "Minimun Attenuation Value")
        
        #self.SAB_attenuation_max, dummy, dummy, self.sizer_SAB_attenuation_max, dummy, dummy = return_textbox_labeled(self, "Maximum Attenuation Value")
        
        #self.SAB_attenuation_step, dummy, dummy, self.sizer_SAB_attenuation_step, dummy, dummy = return_textbox_labeled(self, "Attenuation Step")
        
        self.SAB_attenuation_min, dummy, self.SAB_attenuation_max, dummy, self.SAB_attenuation_step, dummy, self.sizer_SAB_attenuation = return_min_max_step_labeled(self, "Attenuation", unit = False)
        
        self.SAB_attenuation_delay, dummy, dummy, self.sizer_SAB_attenuation_delay, dummy, dummy = return_textbox_labeled(self, "Attenuation Delay")
        
        #power_meter_misure_delay = 1 #seconds
        self.SAB_switch01_delay, dummy, dummy, self.sizer_SAB_switch01_delay, dummy, dummy = return_textbox_labeled(self, "Switch 1 delay (s)")
        
        self.SAB_switch02_delay, dummy, dummy, self.sizer_SAB_switch02_delay, dummy, dummy = return_textbox_labeled(self, "Switch 2 delay (s)")
        
        self.SAB_switch03_delay, dummy, dummy, self.sizer_SAB_switch03_delay, dummy, dummy = return_textbox_labeled(self, "Switch 3 delay (s)")

        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_SAB_state, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_SAB_attenuation_min, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_SAB_attenuation_max, 0, wx.ALL, 5)
        #sizer.Add(self.sizer_SAB_attenuation_step, 0, wx.ALL, 5)
        sizer.Add(self.sizer_SAB_attenuation, 0, wx.ALL, 5)
        sizer.Add(self.sizer_SAB_attenuation_delay, 0, wx.ALL, 5)
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
        self.TSC_state, self.sizer_TSC_state = return_checkbox_labeled(self, "State")

        self.TSC_collecting_delay, dummy, dummy, self.sizer_TSC_collecting_delay, dummy, dummy = return_textbox_labeled(self, "Collecting time (m)")
        
        self.TSC_plot_adev, self.sizer_TSC_plot_adev = return_checkbox_labeled(self, "Plot Allan Deviation")
        
        self.result_file_name, self.result_file_name_button, self.sizer_result_file_name = return_file_browse(self, "Output Path")
        self.result_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_Out)
        
        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_TSC_state, 0, wx.ALL, 5)
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
        self.power_meter_state, self.sizer_power_meter_state = return_checkbox_labeled(self, "State")

        #power_meter_misure_number = 1
        self.power_meter_misure_number, self.sizer_power_meter_misure_number = return_spinctrl(self, "Measures")
        
        #power_meter_misure_delay = 1 #seconds
        self.power_meter_misure_delay, dummy, dummy, self.sizer_power_meter_misure_delay, dummy, dummy = return_textbox_labeled(self, "Measure delay (s)")

        self.power_meter_make_zero, self.sizer_power_meter_make_zero = return_checkbox_labeled(self, "Make Zero")

        sizer.Add(self.instrument_sizer, 0, wx.ALL, 5)
        sizer.Add(self.instrument_test_sizer, 0, wx.ALL, 5)
        sizer.Add(self.sizer_power_meter_state, 0, wx.ALL, 5)
        sizer.Add(self.sizer_power_meter_misure_number, 0, wx.ALL, 5)
        sizer.Add(self.sizer_power_meter_misure_delay, 0, wx.ALL, 5)
        sizer.Add(self.sizer_power_meter_make_zero, 0, wx.ALL, 5)
 
        self.SetSizer(sizer)