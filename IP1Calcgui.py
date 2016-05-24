'''
Created on 09/may/2016

@author: sabah
'''

#import images
import wx
import os

from guitabs import TabPanelFSV, TabPanelPowerMeter, TabPanelSMB, TabPanelSpuriusSetup, TabPanelIP1CalcSetup, TabPanelSAB, TabPanelIP1PlotGraph
from measure_scripts.IP1Cal import unit, SMB_RF, NRP2, SAB, measure_IP1
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument
from utility import writelineonfilesettings, return_now_postfix


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

        # Create and add the second tab
        self.tabRF = TabPanelSMB(self)
        self.tabPowerMeter = TabPanelPowerMeter(self)
        self.tabSAB = TabPanelSAB(self)
        self.tabIP1CalcSetting = TabPanelIP1CalcSetup(self)
        self.tabIP1PlotGraph = TabPanelIP1PlotGraph(self)
        
        self.AddPage(self.tabRF, "Radio Frequency")
 
        
        self.AddPage(self.tabPowerMeter, "Power Meter")
        
        
        self.AddPage(self.tabSAB, "SwitchAttBox")
        
        
        self.AddPage(self.tabIP1CalcSetting, "Calculate IP1")
        
        
        self.AddPage(self.tabIP1PlotGraph, "Graph IP1 plot")
 
########################################################################
class IP1CalcFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Calculate IP1",
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
        #self.Bind(wx.EVT_MENU, self.OnCheckRunMode, self.runmodeitem)
        
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
                exec("{param}.SetValue({value})".format(param = parameter, value = value))
                        
    def savesettings(self, filepointer):

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
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.power_meter_make_zero")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.power_meter_misure_number")
        self.writelinesettings(filepointer, "self.notebook.tabPowerMeter.power_meter_misure_delay")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.instrument_txt_IP")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.instrument_txt_Port")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.instrument_txt_Timeout")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_state")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_attenuation_min")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_attenuation_max")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_attenuation_step")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_attenuation_delay")
        self.writelinesettings(filepointer, "self.notebook.tabIP1CalcSetting.calibration_file_RF")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_switch01_delay")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_switch02_delay")
        self.writelinesettings(filepointer, "self.notebook.tabSAB.SAB_switch03_delay")
        self.writelinesettings(filepointer, "self.notebook.tabIP1CalcSetting.result_file_name")         
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_title")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_label")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_min")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_max")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_step")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_label")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_min")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_max")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_step")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_label_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_min_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_max_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_step_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_label_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_min_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_max_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_step_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_animated")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.data_file_name")
    
    
    
    
    def OnSaveSettings(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.cfg", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            f = open(path, "w")
            self.savesettings(f)
            f.close()
                        
    def writelinesettings(self, f, parameter):
        value = None
        exec("value = {param}.GetValue()".format(param = parameter))
        writelineonfilesettings(f, parameter, value)
    
    def OnStart(self, event):
                
        if self.runmodeitem.IsChecked():
            dlg = wx.MessageDialog(None, 'Test mode. Instruments comunication disabled', "Test mode",  wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        #Check all values
        synthetizer_IP = self.notebook.tabRF.instrument_txt_IP.GetValue()
        if check_value_is_IP(synthetizer_IP, "Synthetizer IP") == 0:
            return None
        
        synthetizer_Port = self.notebook.tabRF.instrument_txt_Port.GetValue()
        if check_value_min_max(synthetizer_Port, "Synthetizer Port", minimum = 0) == 0:
            return None
        
        synthetizer_Timeout = self.notebook.tabRF.instrument_txt_Timeout.GetValue()
        if check_value_min_max(synthetizer_Timeout, "Synthetizer Timeout", minimum = 0) == 0:
            return None

        syntetizer_instrType = self.notebook.tabRF.combobox_instrtype.GetValue()
        
        synthetizer_state = self.notebook.tabRF.synthetizer_state.GetValue()
        
        
        synthetizer_frequency_min_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_min_unit.GetValue())
        if check_value_not_none(synthetizer_frequency_min_unit, "Minimum Frequency Unit") == 0:
            return None
        synthetizer_frequency_min = self.notebook.tabRF.synthetizer_frequency_min.GetValue()
        if check_value_min_max(synthetizer_frequency_min, "Minimum Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_frequency_min = eval(self.notebook.tabRF.synthetizer_frequency_min.GetValue())
        synthetizer_frequency_max_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_max_unit.GetValue())
        if check_value_not_none(synthetizer_frequency_max_unit, "Maximum Frequency Unit") == 0:
            return None
        synthetizer_frequency_max = self.notebook.tabRF.synthetizer_frequency_max.GetValue()
        if check_value_min_max(synthetizer_frequency_max, "Maximum Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_frequency_max = eval(self.notebook.tabRF.synthetizer_frequency_max.GetValue())
        synthetizer_frequency_step_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_step_unit.GetValue())
        if check_value_not_none(synthetizer_frequency_step_unit, "Frequency Step Unit") == 0:
            return None
        synthetizer_frequency_step = self.notebook.tabRF.synthetizer_frequency_step.GetValue()
        if check_value_min_max(synthetizer_frequency_step, "Frequency Step") == 0:
            return None
        else:
            synthetizer_frequency_step = eval(self.notebook.tabRF.synthetizer_frequency_step.GetValue())
        
        try:
            synthetizer_level_min = eval(self.notebook.tabRF.synthetizer_level_min.GetValue())
        except:
            synthetizer_level_min = 0
            
        try:
            synthetizer_level_max = eval(self.notebook.tabRF.synthetizer_level_max.GetValue())
        except:
            synthetizer_level_max = 0
            
        try:
            synthetizer_level_step = eval(self.notebook.tabRF.synthetizer_level_step.GetValue())
        except:
            synthetizer_level_step = 0
        
        
        
        try:
            synthetizer_level_fixed = eval(self.notebook.tabRF.synthetizer_level_fixed.GetValue())
        except:
            synthetizer_level_fixed = 0
            
        power_meter_IP = self.notebook.tabPowerMeter.instrument_txt_IP.GetValue()
        if check_value_is_IP(power_meter_IP, "Power meter IP") == 0:
            return None
        
        power_meter_Port = self.notebook.tabPowerMeter.instrument_txt_Port.GetValue()
        if check_value_min_max(power_meter_Port, "Power meter Port", minimum = 0) == 0:
            return None
        
        power_meter_Timeout = self.notebook.tabPowerMeter.instrument_txt_Timeout.GetValue()
        if check_value_min_max(power_meter_Timeout, "Power meter Timeout", minimum = 0) == 0:
            return None
            
        power_meter_instrType = self.notebook.tabPowerMeter.combobox_instrtype.GetValue()
    

        power_meter_make_zero = self.notebook.tabPowerMeter.power_meter_make_zero.GetValue()
        power_meter_make_zero_delay = self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue()
        if check_value_min_max(power_meter_make_zero_delay, "Make Zero Delay", minimum = 0) == 0:
            return None
        else:
            power_meter_make_zero_delay = eval(self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue())


        power_meter_misure_number = self.notebook.tabPowerMeter.power_meter_misure_number.GetValue()
            
        power_meter_misure_delay = self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue() #seconds
        if check_value_min_max(power_meter_misure_delay, "Measure Delay", minimum = 0) == 0:
            return None
        else:
            power_meter_misure_delay = eval(self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue())
        
        SAB_IP = self.notebook.tabSAB.instrument_txt_IP.GetValue()
        if check_value_is_IP(SAB_IP, "SwitchAttBox IP") == 0:
            return None
        
        SAB_Port = self.notebook.tabSAB.instrument_txt_Port.GetValue()
        if check_value_min_max(SAB_Port, "SwitchAttBox Port", minimum = 0) == 0:
            return None
        
        SAB_Timeout = self.notebook.tabSAB.instrument_txt_Timeout.GetValue()
        if check_value_min_max(SAB_Timeout, "SwitchAttBox Timeout", minimum = 0) == 0:
            return None
        
        SAB_instrType = self.notebook.tabSAB.combobox_instrtype.GetValue()
        
        SAB_state = self.notebook.tabSAB.SAB_state.GetValue()
        
        try:
            SAB_attenuation_min = eval(self.notebook.tabSAB.SAB_attenuation_min.GetValue())
        except:
            SAB_attenuation_min = 0
        
        try:
            SAB_attenuation_max = eval(self.notebook.tabSAB.SAB_attenuation_max.GetValue())
        except:
            SAB_attenuation_max = 0
            
        try:
            SAB_attenuation_step = eval(self.notebook.tabSAB.SAB_attenuation_step.GetValue())
        except:
            SAB_attenuation_step = 0
        
        SAB_attenuation_delay = self.notebook.tabSAB.SAB_attenuation_delay.GetValue()
        if check_value_min_max(SAB_attenuation_delay, "Attenuation Delay", minimum = 0) == 0:
            return None
        else:
            SAB_attenuation_delay = eval(self.notebook.tabSAB.SAB_attenuation_delay.GetValue())
        
        SAB_switch01_delay = self.notebook.tabSAB.SAB_switch01_delay.GetValue()
        if check_value_min_max(SAB_switch01_delay, "Switch 1 Delay", minimum = 0) == 0:
            return None
        else:
            SAB_switch01_delay = eval(self.notebook.tabSAB.SAB_switch01_delay.GetValue())
            
        SAB_switch02_delay = self.notebook.tabSAB.SAB_switch02_delay.GetValue()
        if check_value_min_max(SAB_switch02_delay, "Switch 2 Delay", minimum = 0) == 0:
            return None
        else:
            SAB_switch02_delay = eval(self.notebook.tabSAB.SAB_switch02_delay.GetValue())
            
        calibration_cable_file_name = self.notebook.tabIP1CalcSetting.calibration_file_RF.GetValue()
        result_file_name = self.notebook.tabIP1CalcSetting.result_file_name.GetValue()

        try:
            SMB_RF = create_instrument(synthetizer_IP, synthetizer_Port, eval(synthetizer_Timeout), syntetizer_instrType, TEST_MODE = self.runmodeitem.IsChecked())
        except:
            dlg = wx.MessageDialog(None, "Synthetizer comunication error", 'Error Synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            NRP2 = create_instrument(power_meter_IP, power_meter_Port, eval(power_meter_Timeout), power_meter_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "NRP2")
        except:
            dlg = wx.MessageDialog(None, "Power meter comunication error", 'Error Power meter', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            SAB = create_instrument(SAB_IP, SAB_Port, eval(SAB_Timeout), SAB_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "SAB")
        except:
            dlg = wx.MessageDialog(None, "SwitchAttBox comunication error", 'Error SwitchAttBox', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        measure_IP1(SMB_RF, NRP2, SAB, synthetizer_state, synthetizer_frequency_min_unit, synthetizer_frequency_min, synthetizer_frequency_max_unit, synthetizer_frequency_max, synthetizer_frequency_step_unit, synthetizer_frequency_step, synthetizer_level_fixed, synthetizer_level_min, synthetizer_level_max, synthetizer_level_step, power_meter_make_zero, power_meter_make_zero_delay, power_meter_misure_number, power_meter_misure_delay, SAB_state, SAB_attenuation_min, SAB_attenuation_max, SAB_attenuation_step, SAB_attenuation_delay, SAB_switch01_delay, SAB_switch02_delay, calibration_cable_file_name, result_file_name, createprogressdialog = dialog)
        
        dialog.Destroy()
        filesettingname = result_file_name + "_calcable_" + return_now_postfix() + ".cfg"
        f = open(filesettingname, "w")
        self.savesettings(f)
        f.close()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = IP1CalcFrame()
    app.MainLoop()