'''
Created on 26/dic/2015

@author: sabah
'''

#import images

from taskframe import TaskFrame

import wx
import os
from guitabs_instruments import TabPanelFSV, TabPanelSMB
from guitabs_setup import TabPanelSpuriusSetup
from measure_scripts.Spurius import unit, measure_LNA_spurius, SMB_LO, SMB_RF, NRP2, FSV
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument
from utility import writelineonfilesettings, return_now_postfix,\
    Generic_Range
import pyvisa
import webbrowser
from measure_scripts.scriptutility import Frequency_Range

########################################################################
class NotebookDemo(wx.Notebook):
    """
    Notebook class
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
                             wx.BK_DEFAULT
                             #wx.BK_TOP 
                             #wx.BK_BOTTOM
                             #wx.BK_LEFT
                             #wx.BK_RIGHT
                             )
 
        # Create the first tab and add it to the notebook
        self.tabLO = TabPanelSMB(self)
        #tabOne.SetBackgroundColour("Gray")
        self.AddPage(self.tabLO, "Local oscillator")
 
        # Create and add the second tab
        self.tabRF = TabPanelSMB(self)
        self.AddPage(self.tabRF, "Radio Frequency")
        
        self.tabFSV = TabPanelFSV(self)
        self.AddPage(self.tabFSV, "Spectrum Analyser")
        
        self.tabSpuriusSetting = TabPanelSpuriusSetup(self)
        self.AddPage(self.tabSpuriusSetting, "Spurius Calculation")
        
        
        
 
 
########################################################################
class SpuriusFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                          "Spurius Calculation",
                          size=(800,800)
                          )
 
    def savesettings(self, filepointer):
        params = ["tabLO.instrument_enable_status",
        "tabLO.instrument_txt_IP",
        "tabLO.instrument_txt_Port",
        "tabLO.instrument_txt_Timeout",
        "tabLO.combobox_instrtype",
        "tabLO.synthetizer_frequency_min",
        "tabLO.synthetizer_frequency_max",
        "tabLO.synthetizer_frequency_step",
        "tabLO.synthetizer_frequency_unit",
        "tabLO.synthetizer_level_min",
        "tabLO.synthetizer_level_max",
        "tabLO.synthetizer_level_step",
        "tabRF.instrument_enable_status",
        "tabRF.instrument_txt_IP",
        "tabRF.instrument_txt_Port",
        "tabRF.instrument_txt_Timeout",
        "tabRF.combobox_instrtype",
        "tabRF.synthetizer_frequency_min",
        "tabRF.synthetizer_frequency_max",
        "tabRF.synthetizer_frequency_step",
        "tabRF.synthetizer_frequency_unit",
        "tabRF.synthetizer_level_min",
        "tabRF.synthetizer_level_max",
        "tabRF.synthetizer_level_step",
        "tabFSV.instrument_txt_IP",
        "tabFSV.instrument_txt_Port",
        "tabFSV.instrument_txt_Timeout",
        "tabFSV.combobox_instrtype",
        "tabFSV.instrument_enable_status",
        "tabFSV.spectrum_analyzer_sweep_points",
        "tabFSV.spectrum_analyzer_resolution_bandwidth",
        "tabFSV.spectrum_analyzer_resolution_bandwidth_unit",
        "tabFSV.spectrum_analyzer_video_bandwidth",
        "tabFSV.spectrum_analyzer_video_bandwidth_unit",
        "tabFSV.spectrum_analyzer_frequency_span",
        "tabFSV.spectrum_analyzer_frequency_span_unit",
        "tabFSV.gainAmplifier",
        "tabFSV.spectrum_analyzer_IF_atten_enable",
        "tabFSV.spectrum_analyzer_IF_atten",
        "tabFSV.spectrum_analyzer_IF_relative_level_enable",
        "tabFSV.spectrum_analyzer_IF_relative_level",
        "tabFSV.threshold_power",
        "tabFSV.spectrum_analyzer_frequency_marker_unit",
        "tabFSV.FSV_delay",
        "tabFSV.spectrum_analyzer_central_frequency",
        "tabFSV.spectrum_analyzer_central_frequency_unit",
        "tabSpuriusSetting.m_min_RF",
        "tabSpuriusSetting.m_max_RF",
        "tabSpuriusSetting.m_step_RF",
        "tabSpuriusSetting.n_min_LO",
        "tabSpuriusSetting.n_max_LO",
        "tabSpuriusSetting.n_step_LO",
        "tabSpuriusSetting.IF_low",
        "tabSpuriusSetting.IF_low_unit",
        "tabSpuriusSetting.IF_high",
        "tabSpuriusSetting.IF_high_unit",
        "tabSpuriusSetting.spurius_IF_unit",
        "tabSpuriusSetting.calibration_file_LO",
        "tabSpuriusSetting.calibration_file_LO_enable",
        "tabSpuriusSetting.calibration_file_RF",
        "tabSpuriusSetting.calibration_file_RF_enable",
        "tabSpuriusSetting.calibration_file_IF",
        "tabSpuriusSetting.calibration_file_IF_enable",
        "tabSpuriusSetting.result_file_name"]
        
        TaskFrame.framesavesettings(self, filepointer, params = params)
        

    def OnStart(self, event):
        
        TaskFrame.OnStart(self, event)
        #load values
         
        synthetizer_LO_IP = self.notebook.tabLO.instrument_txt_IP.GetValue()
        if check_value_is_IP(synthetizer_LO_IP, "LO Synthetizer IP") == 0:
            return None
        
        synthetizer_LO_Port = self.notebook.tabLO.instrument_txt_Port.GetValue()
        if check_value_min_max(synthetizer_LO_Port, "LO Synthetizer Port", minimum = 0) == 0:
            return None
        
        synthetizer_LO_Timeout = self.notebook.tabLO.instrument_txt_Timeout.GetValue()
        if check_value_min_max(synthetizer_LO_Timeout, "LO Synthetizer Timeout", minimum = 0) == 0:
            return None
        
        synthetizer_LO_instrType = self.notebook.tabLO.combobox_instrtype.GetValue()
        
        synthetizer_LO_state = self.notebook.tabLO.instrument_enable_status.GetValue()
        
        #synthetizer_LO_frequency_min_unit = unit.return_unit(self.notebook.tabLO.synthetizer_frequency_min_unit.GetValue())
        #if check_value_not_none(synthetizer_LO_frequency_min_unit, "Minimum LO Frequency Unit") == 0:
        #    return None
        
        if synthetizer_LO_state:
            
            synthetizer_LO_frequency_min = self.notebook.tabLO.synthetizer_frequency_min.GetValue()
            if check_value_min_max(synthetizer_LO_frequency_min, "Minimum LO Frequency", minimum = 0) == 0:
                return None
            else:
                synthetizer_LO_frequency_min = eval(self.notebook.tabLO.synthetizer_frequency_min.GetValue())
            
            
            #synthetizer_LO_frequency_max_unit = unit.return_unit(self.notebook.tabLO.synthetizer_frequency_max_unit.GetValue())
            #if check_value_not_none(synthetizer_LO_frequency_max_unit, "Maximum LO Frequency Unit") == 0:
            #    return None
            
            synthetizer_LO_frequency_max = self.notebook.tabLO.synthetizer_frequency_max.GetValue()
            if check_value_min_max(synthetizer_LO_frequency_max, "Maximum LO Frequency", minimum = 0) == 0:
                return None
            else:
                synthetizer_LO_frequency_max = eval(self.notebook.tabLO.synthetizer_frequency_max.GetValue())
                
            #synthetizer_LO_frequency_step_unit = unit.return_unit(self.notebook.tabLO.synthetizer_frequency_step_unit.GetValue())
            #if check_value_not_none(synthetizer_LO_frequency_step_unit, "LO Step Frequency Unit") == 0:
            #    return None
            
            synthetizer_LO_frequency_unit = unit.return_unit(self.notebook.tabLO.synthetizer_frequency_unit.GetValue())
            if check_value_not_none(synthetizer_LO_frequency_unit, "LO Frequency Unit") == 0:
                return None
            
            synthetizer_LO_frequency_step = self.notebook.tabLO.synthetizer_frequency_step.GetValue()
            if check_value_min_max(synthetizer_LO_frequency_step, "LO Step Frequency", minimum = 0) == 0:
                return None
            else:
                synthetizer_LO_frequency_step = eval(self.notebook.tabLO.synthetizer_frequency_step.GetValue())
                
                
            try:
                synthetizer_LO_level_min = eval(self.notebook.tabLO.synthetizer_level_min.GetValue())
            except:
                synthetizer_LO_level_min = 0
                
            try:
                synthetizer_LO_level_max = eval(self.notebook.tabLO.synthetizer_level_max.GetValue())
            except:
                synthetizer_LO_level_max = 0
            
            synthetizer_LO_level_step = self.notebook.tabLO.synthetizer_level_step.GetValue()
            if check_value_min_max(synthetizer_LO_level_step, "LO Level Step", minimum = 0) == 0:
                return None
            else:
                synthetizer_LO_level_step = eval(self.notebook.tabLO.synthetizer_level_step.GetValue())
                
            synthetizer_LO_frequency = Frequency_Range(synthetizer_LO_frequency_min, synthetizer_LO_frequency_max, synthetizer_LO_frequency_step, synthetizer_LO_frequency_unit)
            synthetizer_LO_frequency.to_base()
            synthetizer_LO_level = Generic_Range(synthetizer_LO_level_min, synthetizer_LO_level_max, synthetizer_LO_level_step)
        else:
            synthetizer_LO_frequency = Frequency_Range(0, 0, 1, unit.Hz)
            synthetizer_LO_frequency.to_base()
            synthetizer_LO_level = Generic_Range(0, 0, 1)
            
        synthetizer_RF_IP = self.notebook.tabRF.instrument_txt_IP.GetValue()
        if check_value_is_IP(synthetizer_RF_IP, "RF Synthetizer IP") == 0:
            return None
        
        synthetizer_RF_Port = self.notebook.tabRF.instrument_txt_Port.GetValue()
        if check_value_min_max(synthetizer_RF_Port, "RF Synthetizer Port", minimum = 0) == 0:
            return None
        
        synthetizer_RF_Timeout = self.notebook.tabRF.instrument_txt_Timeout.GetValue()
        if check_value_min_max(synthetizer_RF_Timeout, "RF Synthetizer Timeout", minimum = 0) == 0:
            return None
        
        synthetizer_RF_instrType = self.notebook.tabRF.combobox_instrtype.GetValue()
        
        synthetizer_RF_state = self.notebook.tabRF.instrument_enable_status.GetValue()
        #synthetizer_RF_frequency_min_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_min_unit.GetValue())
        #if check_value_not_none(synthetizer_RF_frequency_min_unit, "Minimum RF Frequency Unit") == 0:
        #    return None
        if synthetizer_RF_state:
            synthetizer_RF_frequency_min = self.notebook.tabRF.synthetizer_frequency_min.GetValue()
            if check_value_min_max(synthetizer_RF_frequency_min, "Minimum RF Frequency", minimum = 0) == 0:
                return None
            else:
                synthetizer_RF_frequency_min = eval(self.notebook.tabRF.synthetizer_frequency_min.GetValue())
            
            
            #synthetizer_RF_frequency_max_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_max_unit.GetValue())
            #if check_value_not_none(synthetizer_RF_frequency_max_unit, "Maximum RF Frequency Unit") == 0:
            #    return None
            
            synthetizer_RF_frequency_max = self.notebook.tabRF.synthetizer_frequency_max.GetValue()
            if check_value_min_max(synthetizer_RF_frequency_max, "Maximum RF Frequency", minimum = 0) == 0:
                return None
            else:
                synthetizer_RF_frequency_max = eval(self.notebook.tabRF.synthetizer_frequency_max.GetValue())
                
            #synthetizer_RF_frequency_step_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_step_unit.GetValue())
            #if check_value_not_none(synthetizer_RF_frequency_step_unit, "RF Step Frequency Unit") == 0:
            #    return None
            
            synthetizer_RF_frequency_step = self.notebook.tabRF.synthetizer_frequency_step.GetValue()
            if check_value_min_max(synthetizer_RF_frequency_step, "RF Step Frequency", minimum = 0) == 0:
                return None
            else:
                synthetizer_RF_frequency_step = eval(self.notebook.tabRF.synthetizer_frequency_step.GetValue())
                
            synthetizer_RF_frequency_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_unit.GetValue())
            if check_value_not_none(synthetizer_RF_frequency_unit, "RF Frequency Unit") == 0:
                return None
                
            try:
                synthetizer_RF_level_min = eval(self.notebook.tabRF.synthetizer_level_min.GetValue())
            except:
                synthetizer_RF_level_min = 0
                
            try:
                synthetizer_RF_level_max = eval(self.notebook.tabRF.synthetizer_level_max.GetValue())
            except:
                synthetizer_RF_level_max = 0
            
            synthetizer_RF_level_step = self.notebook.tabRF.synthetizer_level_step.GetValue()
            if check_value_min_max(synthetizer_RF_level_step, "RF Level Step", minimum = 0) == 0:
                return None
            else:
                synthetizer_RF_level_step = eval(self.notebook.tabRF.synthetizer_level_step.GetValue())
                
            synthetizer_RF_frequency = Frequency_Range(synthetizer_RF_frequency_min, synthetizer_RF_frequency_max, synthetizer_RF_frequency_step, synthetizer_RF_frequency_unit)
            synthetizer_RF_frequency.to_base()
            synthetizer_RF_level = Generic_Range(synthetizer_RF_level_min, synthetizer_RF_level_max, synthetizer_RF_level_step)
        else:
            synthetizer_RF_frequency = Frequency_Range(0, 0, 1, unit.Hz)
            synthetizer_RF_frequency.to_base()
            synthetizer_RF_level = Generic_Range(0, 0, 1)
                
        spectrum_analyzer_IP = self.notebook.tabFSV.instrument_txt_IP.GetValue()
        if check_value_is_IP(spectrum_analyzer_IP, "LO Synthetizer IP") == 0:
            return None
        
        spectrum_analyzer_Port = self.notebook.tabFSV.instrument_txt_Port.GetValue()
        if check_value_min_max(spectrum_analyzer_Port, "LO Synthetizer Port", minimum = 0) == 0:
            return None
        
        spectrum_analyzer_Timeout = self.notebook.tabFSV.instrument_txt_Timeout.GetValue()
        if check_value_min_max(spectrum_analyzer_Timeout, "LO Synthetizer Timeout", minimum = 0) == 0:
            return None
        
        spectrum_analyzer_instrType = self.notebook.tabFSV.combobox_instrtype.GetValue()
        
        spectrum_analyzer_state = self.notebook.tabFSV.instrument_enable_status.GetValue()
        
        if spectrum_analyzer_state:
            spectrum_analyzer_sweep_points = self.notebook.tabFSV.spectrum_analyzer_sweep_points.GetValue()
            if check_value_min_max(spectrum_analyzer_sweep_points, "Sweep points", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_sweep_points = eval(self.notebook.tabFSV.spectrum_analyzer_sweep_points.GetValue())
            
            
            spectrum_analyzer_resolution_bandwidth = self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth.GetValue()
            if check_value_min_max(spectrum_analyzer_resolution_bandwidth, "Resolution Bandwidth", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_resolution_bandwidth = eval(self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth.GetValue())
            
            spectrum_analyzer_resolution_bandwidth_unit = unit.return_unit(self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_resolution_bandwidth_unit, "Resolution Bandwidth Unit") == 0:
                return None
            
            spectrum_analyzer_video_bandwidth = self.notebook.tabFSV.spectrum_analyzer_video_bandwidth.GetValue()
            if check_value_min_max(spectrum_analyzer_video_bandwidth, "Video Bandwidth", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_video_bandwidth = eval(self.notebook.tabFSV.spectrum_analyzer_video_bandwidth.GetValue())
            
            spectrum_analyzer_video_bandwidth_unit = unit.return_unit(self.notebook.tabFSV.spectrum_analyzer_video_bandwidth_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_video_bandwidth_unit, "Video Bandwidth Unit") == 0:
                return None
            
            spectrum_analyzer_frequency_span = self.notebook.tabFSV.spectrum_analyzer_frequency_span.GetValue()
            if check_value_min_max(spectrum_analyzer_frequency_span, "Frequency Span", minimum = 0) == 0:
                return None
            else:
                spectrum_analyzer_frequency_span = eval(self.notebook.tabFSV.spectrum_analyzer_frequency_span.GetValue())
            
            spectrum_analyzer_frequency_span_unit = unit.return_unit(self.notebook.tabFSV.spectrum_analyzer_frequency_span_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_frequency_span_unit, "Frequency Span Unit") == 0:
                return None
            
            ##spectrum_analyzer_harmonic_number = spectrum_analyzer_harmonic_number
            #spectrum_analyzer_attenuation = self.notebook.tabFSV.spectrum_analyzer_attenuation.GetValue()
            #if check_value_not_none(spectrum_analyzer_attenuation, "Attenuation") == 0:
            #    return None
            
            gainAmplifier = self.notebook.tabFSV.gainAmplifier.GetValue() #dB
            if check_value_not_none(gainAmplifier, "Gain Amplifier") == 0:
                return None
            
            spectrum_analyzer_IF_atten_enable = self.notebook.tabFSV.spectrum_analyzer_IF_atten_enable.GetValue()
            spectrum_analyzer_IF_atten = self.notebook.tabFSV.spectrum_analyzer_IF_atten.GetValue()
            if check_value_not_none(spectrum_analyzer_IF_atten, "Attenuation") == 0:
                return None
            
            spectrum_analyzer_IF_relative_level = self.notebook.tabFSV.spectrum_analyzer_IF_relative_level.GetValue()
            if check_value_not_none(spectrum_analyzer_IF_relative_level, "Relative Power Level") == 0:
                return None
            
            spectrum_analyzer_IF_relative_level_enable = self.notebook.tabFSV.spectrum_analyzer_IF_relative_level_enable.GetValue()
            
            
            threshold_power = self.notebook.tabFSV.threshold_power.GetValue() #dB 
            if check_value_not_none(threshold_power, "Threshold Power Level") == 0:
                return None
            
            spectrum_analyzer_frequency_marker_unit = unit.return_unit(self.notebook.tabFSV.spectrum_analyzer_frequency_marker_unit.GetValue())
            #to check
            if check_value_not_none(spectrum_analyzer_frequency_marker_unit, "Marker Frequency Unit") == 0:
                return None
            
            FSV_delay = self.notebook.tabFSV.FSV_delay.GetValue()
            if check_value_min_max(FSV_delay, "FSV measure delay", minimum = 0) == 0:
                return None
            else:
                FSV_delay = eval(self.notebook.tabFSV.FSV_delay.GetValue()) 
            
        m_min_RF = self.notebook.tabSpuriusSetting.m_min_RF.GetValue()
        m_max_RF = self.notebook.tabSpuriusSetting.m_max_RF.GetValue()
        m_step_RF = self.notebook.tabSpuriusSetting.m_step_RF.GetValue()
        n_min_LO = self.notebook.tabSpuriusSetting.n_min_LO.GetValue()
        n_max_LO = self.notebook.tabSpuriusSetting.n_max_LO.GetValue()
        n_step_LO = self.notebook.tabSpuriusSetting.n_step_LO.GetValue()

        IF_low = self.notebook.tabSpuriusSetting.IF_low.GetValue()
        if check_value_min_max(IF_low, "Low Frequency", minimum = 0) == 0:
            return None
        else:
            IF_low = eval(self.notebook.tabSpuriusSetting.IF_low.GetValue())
        
        IF_low_unit = unit.return_unit(self.notebook.tabSpuriusSetting.IF_low_unit.GetValue())
        if check_value_not_none(IF_low_unit, "Low Frequency Unit") == 0:
            return None


        IF_high = self.notebook.tabSpuriusSetting.IF_high.GetValue()
        if check_value_min_max(IF_high, "High Frequency", minimum = 0) == 0:
            return None
        else:
            IF_high = eval(self.notebook.tabSpuriusSetting.IF_high.GetValue())
        
        IF_high_unit = unit.return_unit(self.notebook.tabSpuriusSetting.IF_high_unit.GetValue())
        if check_value_not_none(IF_high_unit, "High Frequency Unit") == 0:
            return None
        
        spurius_IF_unit = unit.return_unit(self.notebook.tabSpuriusSetting.spurius_IF_unit.GetValue())
        if check_value_not_none(spurius_IF_unit, "Spurius IF Unit") == 0:
            return None
        
        calibration_file_LO = self.notebook.tabSpuriusSetting.calibration_file_LO.GetValue()
        calibration_file_LO_enable = self.notebook.tabSpuriusSetting.calibration_file_LO_enable.GetValue()
        if calibration_file_LO_enable:
            if check_value_is_valid_file(calibration_file_LO, "LO Calibration file") == 0:
                return None
        
        calibration_file_RF = self.notebook.tabSpuriusSetting.calibration_file_RF.GetValue()
        calibration_file_RF_enable = self.notebook.tabSpuriusSetting.calibration_file_RF_enable.GetValue()
        if calibration_file_RF_enable:
            if check_value_is_valid_file(calibration_file_LO, "LO Calibration file") == 0:
                return None
        
        calibration_file_IF = self.notebook.tabSpuriusSetting.calibration_file_IF.GetValue()
        calibration_file_IF_enable = self.notebook.tabSpuriusSetting.calibration_file_IF_enable.GetValue()
        if calibration_file_IF_enable:
            if check_value_is_valid_file(calibration_file_LO, "LO Calibration file") == 0:
                return None
        
        result_file_name = self.notebook.tabSpuriusSetting.result_file_name.GetValue()

        try:
            SMB_LO = create_instrument(synthetizer_LO_IP, synthetizer_LO_Port, eval(synthetizer_LO_Timeout), synthetizer_LO_instrType, TEST_MODE = self.runmodeitem.IsChecked(), enable_state = synthetizer_LO_state)
        except:
            dlg = wx.MessageDialog(None, "LO synthetizer comunication error", 'Error LO synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            SMB_RF = create_instrument(synthetizer_RF_IP, synthetizer_RF_Port, eval(synthetizer_RF_Timeout), synthetizer_RF_instrType, TEST_MODE = self.runmodeitem.IsChecked(), enable_state = synthetizer_RF_state)
        except:
            dlg = wx.MessageDialog(None, "RF synthetizer comunication error", 'Error RF synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            FSV = create_instrument(spectrum_analyzer_IP, spectrum_analyzer_Port, eval(spectrum_analyzer_Timeout), spectrum_analyzer_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "FSV", enable_state = spectrum_analyzer_state)
        except:
            dlg = wx.MessageDialog(None, "Spectrum analiser comunication error", 'Error Spectrum analiser', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        if synthetizer_LO_state:
            n_LO = Generic_Range(n_min_LO, n_max_LO, n_step_LO)
        else:
            n_LO = Generic_Range(0, 0, 1)
        if synthetizer_RF_state:
            m_RF = Generic_Range(m_min_RF, m_max_RF, m_step_RF)
        else:
            m_RF = Generic_Range(0, 0, 1)
        

        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        self.savesettings(result_file_name)
        
        spurius_filename = measure_LNA_spurius(SMB_LO, 
                            SMB_RF, 
                            FSV, 
                            synthetizer_LO_state, 
                            synthetizer_LO_frequency, 
                            synthetizer_LO_level, 
                            synthetizer_RF_state, 
                            synthetizer_RF_frequency, 
                            synthetizer_RF_level, 
                            spectrum_analyzer_state, 
                            spectrum_analyzer_sweep_points, 
                            spectrum_analyzer_resolution_bandwidth, 
                            spectrum_analyzer_resolution_bandwidth_unit, 
                            spectrum_analyzer_video_bandwidth, 
                            spectrum_analyzer_video_bandwidth_unit, 
                            spectrum_analyzer_frequency_span, 
                            spectrum_analyzer_frequency_span_unit, 
                            #spectrum_analyzer_attenuation, 
                            gainAmplifier, 
                            spectrum_analyzer_IF_atten_enable, 
                            spectrum_analyzer_IF_atten, 
                            spectrum_analyzer_IF_relative_level, 
                            spectrum_analyzer_IF_relative_level_enable, 
                            threshold_power, 
                            spectrum_analyzer_frequency_marker_unit, 
                            FSV_delay, 
                            m_RF,
                            n_LO,
                            IF_low, 
                            IF_low_unit, 
                            IF_high, 
                            IF_high_unit, 
                            spurius_IF_unit, 
                            calibration_file_LO, 
                            calibration_file_LO_enable,
                            calibration_file_RF, 
                            calibration_file_RF_enable,
                            calibration_file_IF, 
                            calibration_file_IF_enable,
                            result_file_name, 
                            createprogressdialog = dialog)
 
        dialog.Destroy()
        
        try:
            webbrowser.open(os.path.dirname(spurius_filename))
        except:
            pass
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = SpuriusFrame()
    app.MainLoop()