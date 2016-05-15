'''
Created on 26/dic/2015

@author: sabah
'''

#import images
import wx
import os
from guitabs import TabPanelFSV, TabPanelPowerMeter, TabPanelSMB, TabPanelSpuriusSetup
from measure_scripts.Spurius import unit, measure_LNA_spurius, SMB_LO, SMB_RF, NRP2, FSV
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument
from utility import writelineonfilesettings, return_now_postfix
import pyvisa

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
 
        ## Show how to put an image on one of the notebook tabs,
        ## first make the image list:
        #il = wx.ImageList(16, 16)
        #idx1 = il.Add(images.Smiles.GetBitmap())
        #self.AssignImageList(il)
 
        ## now put an image on the first tab we just created:
        #self.SetPageImage(0, idx1)
 
        # Create and add the second tab
        self.tabRF = TabPanelSMB(self)
        self.AddPage(self.tabRF, "Radio Frequency")
        
        self.tabFSV = TabPanelFSV(self)
        self.AddPage(self.tabFSV, "Spectrum Analyser")
 
        self.tabPowerMeter = TabPanelPowerMeter(self)
        self.AddPage(self.tabPowerMeter, "Power Meter")
        
        self.tabSpuriusSetting = TabPanelSpuriusSetup(self)
        self.AddPage(self.tabSpuriusSetting, "Spurius Calculation")
        # Create and add the third tab
        #self.AddPage(TabPanel(self), "TabThree")
 
        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
#    def OnPageChanged(self, event):
#        old = event.GetOldSelection()
#        new = event.GetSelection()
#        sel = self.GetSelection()
#        print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
#        event.Skip()
 
#    def OnPageChanging(self, event):
#        old = event.GetOldSelection()
#        new = event.GetSelection()
#        sel = self.GetSelection()
#        print 'OnPageChanging, old:%d, new:%d, sel:%d\n' % (old, new, sel)
#        event.Skip()
 
 
########################################################################
class SpuriusFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Spurius Calculation",
                          size=(800,650)
                          )
        
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        self.fitem = fileMenu.Append(wx.ID_OPEN, 'Load settings', 'Load settings')
        self.fitem2 = fileMenu.Append(wx.ID_SAVEAS, 'Save settings', 'Save settings')
        self.runmodeitem = fileMenu.AppendCheckItem(7890, "Testing Mode", "Enable testing mode")
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnLoadSettings, self.fitem)
        self.Bind(wx.EVT_MENU, self.OnSaveSettings, self.fitem2)

        self.panel = wx.Panel(self)
        self.btn_execute = wx.Button(self.panel, 0, 'Start')
        self.btn_execute.Bind(wx.EVT_BUTTON, self.OnStart)
        
        self.notebook = NotebookDemo(self.panel)
        #notebook2 = NotebookDemo(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        #sizer.Add(notebook2, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_execute, 0, wx.ALL|wx.EXPAND, 5)
        self.panel.SetSizer(sizer)
        self.Layout()
 
        self.Show()
    
    
    def OnLoadSettings(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.cfg", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #mypath = os.path.basename(path)
            f = open(path, "r")
            for line in f:
                parameter = line.split("=")[0].strip()
                value =  line.split("=")[1].strip()
                try:
                    exec("{param}.SetValue({value})".format(param = parameter, value = value))
                except:
                    print("Error loading {param}".format(param = parameter))
                        
    def savesettings(self, filepointer):
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_state")
        self.writelinesettings(filepointer, "self.notebook.tabLO.instrument_txt_IP")
        self.writelinesettings(filepointer, "self.notebook.tabLO.instrument_txt_Port")
        self.writelinesettings(filepointer, "self.notebook.tabLO.instrument_txt_Timeout")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_frequency_min_unit")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_frequency_min")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_frequency_max_unit")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_frequency_max")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_frequency_step_unit")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_frequency_step")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_level_min")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_level_max")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_level_step")
        self.writelinesettings(filepointer, "self.notebook.tabLO.synthetizer_level_fixed")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_state")
        self.writelinesettings(filepointer, "self.notebook.tabRF.instrument_txt_IP")
        self.writelinesettings(filepointer, "self.notebook.tabRF.instrument_txt_Port")
        self.writelinesettings(filepointer, "self.notebook.tabRF.instrument_txt_Timeout")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_frequency_min_unit")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_frequency_min")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_frequency_max_unit")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_frequency_max")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_frequency_step_unit")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_frequency_step")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_level_min")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_level_max")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_level_step")
        self.writelinesettings(filepointer, "self.notebook.tabRF.synthetizer_level_fixed")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.instrument_txt_IP")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.instrument_txt_Port")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.instrument_txt_Timeout")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.power_meter_state")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.power_meter_misure_number")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.power_meter_misure_delay")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.instrument_txt_IP")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.instrument_txt_Port")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.instrument_txt_Timeout")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_state")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_sweep_points")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth_unit")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_video_bandwidth")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_video_bandwidth_unit")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_frequency_span")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_frequency_span_unit")
        #self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_attenuation")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.gainAmplifier")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_IF_atten_enable")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_IF_atten")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_IF_relative_level_enable")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_IF_relative_level")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.threshold_power")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.spectrum_analyzer_frequency_marker_unit")
        self.writelinesettings(filepointer, "self.notebook.tabFSV.FSV_delay")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.m_max_RF")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.n_max_LO")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.IF_high")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.IF_high_unit")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.spurius_IF_unit")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.calibration_file_LO")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.calibration_file_RF")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.calibration_file_IF")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusSetting.result_file_name")

    def OnSaveSettings(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.cfg", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            #mypath = os.path.basename(path)
            f = open(path, "w")
            self.savesettings(f)

            
            f.close()
                        
    def writelinesettings(self, f, parameter):
        value = None
        exec("value = {param}.GetValue()".format(param = parameter))
        writelineonfilesettings(f, parameter, value)
    
    def OnStart(self, event):
        
        
        if self.runmodeitem.IsChecked():
            dlg = wx.MessageDialog(None,'Test mode. Instruments comunication disabled', "Test mode",  wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        #Check all values
        
        
        #load values
         
        synthetizer_LO_IP = self.notebook.tabRF.instrument_txt_IP.GetValue()
        if check_value_is_IP(synthetizer_LO_IP, "LO Synthetizer IP") == 0:
            return None
        
        synthetizer_LO_Port = self.notebook.tabRF.instrument_txt_Port.GetValue()
        if check_value_min_max(synthetizer_LO_Port, "LO Synthetizer Port", minimum = 0) == 0:
            return None
        
        synthetizer_LO_Timeout = self.notebook.tabRF.instrument_txt_Timeout.GetValue()
        if check_value_min_max(synthetizer_LO_Timeout, "LO Synthetizer Timeout", minimum = 0) == 0:
            return None
        
        synthetizer_LO_instrType = self.notebook.tabLO.combobox_instrtype.GetValue()
        
        synthetizer_LO_state = self.notebook.tabLO.synthetizer_state.GetValue()
        
        synthetizer_LO_frequency_min_unit = unit.return_unit(self.notebook.tabLO.synthetizer_frequency_min_unit.GetValue())
        if check_value_not_none(synthetizer_LO_frequency_min_unit, "Minimum LO Frequency Unit") == 0:
            return None
        
        synthetizer_LO_frequency_min = self.notebook.tabLO.synthetizer_frequency_min.GetValue()
        if check_value_min_max(synthetizer_LO_frequency_min, "Minimum LO Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_LO_frequency_min = eval(self.notebook.tabLO.synthetizer_frequency_min.GetValue())
        
        
        synthetizer_LO_frequency_max_unit = unit.return_unit(self.notebook.tabLO.synthetizer_frequency_max_unit.GetValue())
        if check_value_not_none(synthetizer_LO_frequency_max_unit, "Maximum LO Frequency Unit") == 0:
            return None
        
        synthetizer_LO_frequency_max = self.notebook.tabLO.synthetizer_frequency_max.GetValue()
        if check_value_min_max(synthetizer_LO_frequency_max, "Maximum LO Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_LO_frequency_max = eval(self.notebook.tabLO.synthetizer_frequency_max.GetValue())
            
        synthetizer_LO_frequency_step_unit = unit.return_unit(self.notebook.tabLO.synthetizer_frequency_step_unit.GetValue())
        if check_value_not_none(synthetizer_LO_frequency_step_unit, "LO Step Frequency Unit") == 0:
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
        
        synthetizer_RF_state = self.notebook.tabRF.synthetizer_state.GetValue()
        synthetizer_RF_frequency_min_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_min_unit.GetValue())
        if check_value_not_none(synthetizer_RF_frequency_min_unit, "Minimum RF Frequency Unit") == 0:
            return None
        
        synthetizer_RF_frequency_min = self.notebook.tabRF.synthetizer_frequency_min.GetValue()
        if check_value_min_max(synthetizer_RF_frequency_min, "Minimum RF Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_RF_frequency_min = eval(self.notebook.tabRF.synthetizer_frequency_min.GetValue())
        
        
        synthetizer_RF_frequency_max_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_max_unit.GetValue())
        if check_value_not_none(synthetizer_RF_frequency_max_unit, "Maximum RF Frequency Unit") == 0:
            return None
        
        synthetizer_RF_frequency_max = self.notebook.tabRF.synthetizer_frequency_max.GetValue()
        if check_value_min_max(synthetizer_RF_frequency_max, "Maximum RF Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_RF_frequency_max = eval(self.notebook.tabRF.synthetizer_frequency_max.GetValue())
            
        synthetizer_RF_frequency_step_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_step_unit.GetValue())
        if check_value_not_none(synthetizer_RF_frequency_step_unit, "RF Step Frequency Unit") == 0:
            return None
        
        synthetizer_RF_frequency_step = self.notebook.tabRF.synthetizer_frequency_step.GetValue()
        if check_value_min_max(synthetizer_RF_frequency_step, "RF Step Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_RF_frequency_step = eval(self.notebook.tabRF.synthetizer_frequency_step.GetValue())
            
            
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
            
        power_meter_IP = self.notebook.tabRF.instrument_txt_IP.GetValue()
        if check_value_is_IP(power_meter_IP, "LO Synthetizer IP") == 0:
            return None
        
        power_meter_Port = self.notebook.tabRF.instrument_txt_Port.GetValue()
        if check_value_min_max(power_meter_Port, "LO Synthetizer Port", minimum = 0) == 0:
            return None
        
        power_meter_Timeout = self.notebook.tabRF.instrument_txt_Timeout.GetValue()
        if check_value_min_max(power_meter_Timeout, "LO Synthetizer Timeout", minimum = 0) == 0:
            return None
            
        power_meter_instrType = self.notebook.tabPowerMeter.combobox_instrtype.GetValue()
            
        power_meter_state = self.notebook.tabPowerMeter.power_meter_state.GetValue()
        power_meter_misure_number = self.notebook.tabPowerMeter.power_meter_misure_number.GetValue()
        
        
        power_meter_misure_delay = self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue() #seconds
        if check_value_min_max(power_meter_misure_delay, "Measure Delay", minimum = 0) == 0:
            return None
        else:
            power_meter_misure_delay = eval(self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue())
        
        spectrum_analyzer_IP = self.notebook.tabRF.instrument_txt_IP.GetValue()
        if check_value_is_IP(spectrum_analyzer_IP, "LO Synthetizer IP") == 0:
            return None
        
        spectrum_analyzer_Port = self.notebook.tabRF.instrument_txt_Port.GetValue()
        if check_value_min_max(spectrum_analyzer_Port, "LO Synthetizer Port", minimum = 0) == 0:
            return None
        
        spectrum_analyzer_Timeout = self.notebook.tabRF.instrument_txt_Timeout.GetValue()
        if check_value_min_max(spectrum_analyzer_Timeout, "LO Synthetizer Timeout", minimum = 0) == 0:
            return None
        
        spectrum_analyzer_instrType = self.notebook.tabFSV.combobox_instrtype.GetValue()
        
        spectrum_analyzer_state = self.notebook.tabFSV.spectrum_analyzer_state.GetValue()
        
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
        if check_value_not_none(synthetizer_RF_frequency_max_unit, "Marker Frequency Unit") == 0:
            return None
        
        FSV_delay = self.notebook.tabFSV.FSV_delay.GetValue()
        if check_value_min_max(FSV_delay, "FSV measure delay", minimum = 0) == 0:
            return None
        else:
            FSV_delay = eval(self.notebook.tabFSV.FSV_delay.GetValue())
            
        m_max_RF = self.notebook.tabSpuriusSetting.m_max_RF.GetValue()
        n_max_LO = self.notebook.tabSpuriusSetting.n_max_LO.GetValue()
        
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
        if check_value_is_valid_file(calibration_file_LO, "LO Calibration file") == 0:
            return None
        
        calibration_file_RF = self.notebook.tabSpuriusSetting.calibration_file_RF.GetValue()
        if check_value_is_valid_file(calibration_file_LO, "LO Calibration file") == 0:
            return None
        
        calibration_file_IF = self.notebook.tabSpuriusSetting.calibration_file_IF.GetValue()
        if check_value_is_valid_file(calibration_file_LO, "LO Calibration file") == 0:
            return None
        
        result_file_name = self.notebook.tabSpuriusSetting.result_file_name.GetValue()

        try:
            SMB_LO = create_instrument(synthetizer_LO_IP, synthetizer_LO_Port, eval(synthetizer_LO_Timeout), synthetizer_LO_instrType, TEST_MODE = self.runmodeitem.IsChecked())
        except:
            dlg = wx.MessageDialog(None, "LO synthetizer comunication error", 'Error LO synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            SMB_RF = create_instrument(synthetizer_RF_IP, synthetizer_RF_Port, eval(synthetizer_RF_Timeout), synthetizer_RF_instrType, TEST_MODE = self.runmodeitem.IsChecked())
        except:
            dlg = wx.MessageDialog(None, "RF synthetizer comunication error", 'Error RF synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0

        try:
            NRP2 = create_instrument(power_meter_IP, power_meter_Port, eval(power_meter_Timeout), power_meter_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "NRP2")
        except:
            dlg = wx.MessageDialog(None, "Power meter comunication error", 'Error Power meter', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            FSV = create_instrument(spectrum_analyzer_IP, spectrum_analyzer_Port, eval(spectrum_analyzer_Timeout), spectrum_analyzer_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "FSV")
        except:
            dlg = wx.MessageDialog(None, "Spectrum analiser comunication error", 'Error Spectrum analiser', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0

        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

        measure_LNA_spurius(SMB_LO, 
                            SMB_RF, 
                            NRP2, 
                            FSV, 
                            synthetizer_LO_state, 
                            synthetizer_LO_frequency_min_unit, 
                            synthetizer_LO_frequency_min, 
                            synthetizer_LO_frequency_max_unit, 
                            synthetizer_LO_frequency_max, 
                            synthetizer_LO_frequency_step_unit, 
                            synthetizer_LO_frequency_step, 
                            synthetizer_LO_level_min, 
                            synthetizer_LO_level_max, 
                            synthetizer_LO_level_step, 
                            synthetizer_RF_state, 
                            synthetizer_RF_frequency_min_unit, 
                            synthetizer_RF_frequency_min, 
                            synthetizer_RF_frequency_max_unit, 
                            synthetizer_RF_frequency_max, 
                            synthetizer_RF_frequency_step_unit, 
                            synthetizer_RF_frequency_step, 
                            synthetizer_RF_level_min, 
                            synthetizer_RF_level_max, 
                            synthetizer_RF_level_step, 
                            power_meter_state, 
                            power_meter_misure_number, 
                            power_meter_misure_delay, 
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
                            m_max_RF, 
                            n_max_LO, 
                            IF_high, 
                            IF_high_unit, 
                            spurius_IF_unit, 
                            calibration_file_LO, 
                            calibration_file_RF, 
                            calibration_file_IF, 
                            result_file_name, 
                            createprogressdialog = dialog)
 
        dialog.Destroy()
        filesettingname = result_file_name + "_spurius_" + return_now_postfix() + ".cfg"
        f = open(filesettingname, "w")
        self.savesettings(f)
        f.close()
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = SpuriusFrame()
    app.MainLoop()