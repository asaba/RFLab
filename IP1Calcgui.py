'''
Created on 09/may/2016

@author: sabah
'''

#import images
from taskframe import TaskFrame
import wx
import os
import webbrowser

from guitabs import TabPanelFSV, TabPanelPowerMeter, TabPanelSMB, TabPanelSpuriusSetup, TabPanelIP1CalcSetup, TabPanelSAB, TabPanelIP1PlotGraph
from measure_scripts.IP1Cal import unit, SMB_RF, NRP2, SAB, measure_IP1
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument, check_steps
from utility import return_now_postfix,\
    Generic_Range
from measure_scripts.scriptutility import Frequency_Range


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
        
        self.AddPage(self.tabRF, "Radio Frequency")
        self.AddPage(self.tabPowerMeter, "Power Meter")
        self.AddPage(self.tabSAB, "SwitchAttBox")
        self.AddPage(self.tabIP1CalcSetting, "Calculate IP1")
 
########################################################################
class IP1CalcFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                          "Calculate IP1",
                          size=(800,650)
                          )

                        
    def savesettings(self, filename):

        params = ["tabRF.synthetizer_state", 
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
                  "tabPowerMeter.instrument_txt_IP",
                  "tabPowerMeter.instrument_txt_Port",
                  "tabPowerMeter.instrument_txt_Timeout",
                  "tabPowerMeter.combobox_instrtype",
                  "tabPowerMeter.power_meter_state",
                  "tabPowerMeter.power_meter_make_zero",
                  "tabPowerMeter.power_meter_misure_number",
                  "tabPowerMeter.power_meter_misure_delay",
                  "tabSAB.instrument_txt_IP",
                  "tabSAB.instrument_txt_Port",
                  "tabSAB.instrument_txt_Timeout",
                  "tabSAB.SAB_state",
                  "tabSAB.SAB_attenuation_min",
                  "tabSAB.SAB_attenuation_max",
                  "tabSAB.SAB_attenuation_step",
                  "tabSAB.SAB_attenuation_delay",
                  "tabIP1CalcSetting.calibration_file_RF",
                  "tabSAB.SAB_switch01_delay",
                  "tabSAB.SAB_switch02_delay",
                  "tabSAB.SAB_switch03_delay",
                  "tabIP1CalcSetting.result_file_name"]
        
        
        TaskFrame.framesavesettings(self, filename, params = params)
    
    def OnStart(self, event):
                
        TaskFrame.OnStart(self, event)
        
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
        
        
        #synthetizer_frequency_min_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_min_unit.GetValue())
        #if check_value_not_none(synthetizer_frequency_min_unit, "Minimum Frequency Unit") == 0:
        #    return None
        synthetizer_frequency_min = self.notebook.tabRF.synthetizer_frequency_min.GetValue()
        if check_value_min_max(synthetizer_frequency_min, "Minimum Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_frequency_min = eval(self.notebook.tabRF.synthetizer_frequency_min.GetValue())
        #synthetizer_frequency_max_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_max_unit.GetValue())
        #if check_value_not_none(synthetizer_frequency_max_unit, "Maximum Frequency Unit") == 0:
        #    return None
        synthetizer_frequency_max = self.notebook.tabRF.synthetizer_frequency_max.GetValue()
        if check_value_min_max(synthetizer_frequency_max, "Maximum Frequency", minimum = 0) == 0:
            return None
        else:
            synthetizer_frequency_max = eval(self.notebook.tabRF.synthetizer_frequency_max.GetValue())
        #synthetizer_frequency_step_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_step_unit.GetValue())
        #if check_value_not_none(synthetizer_frequency_step_unit, "Frequency Step Unit") == 0:
        #    return None
        synthetizer_frequency_step = self.notebook.tabRF.synthetizer_frequency_step.GetValue()
        if check_value_min_max(synthetizer_frequency_step, "Frequency Step") == 0:
            return None
        else:
            synthetizer_frequency_step = eval(self.notebook.tabRF.synthetizer_frequency_step.GetValue())
        synthetizer_frequency_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_unit.GetValue())
        if check_value_not_none(synthetizer_frequency_unit, "Frequency Unit") == 0:
            return None
        
        
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
            synthetizer_level_step = 1
        
        
        
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
            if check_steps(SAB_attenuation_step, "SwitchAttBox attenuation step") == 0:
                return None
        except:
            SAB_attenuation_step = 1
        
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
        
        synthetizer_frequency = Frequency_Range(synthetizer_frequency_min, synthetizer_frequency_max, synthetizer_frequency_step, synthetizer_frequency_unit)
        synthetizer_frequency.to_base()
        synthetizer_level = Generic_Range(synthetizer_level_min, synthetizer_level_max, synthetizer_level_step)
        SAB_attenuation = Generic_Range(SAB_attenuation_min, SAB_attenuation_max, SAB_attenuation_step)
        
        self.savesettings(result_file_name)
        
        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        result_IP1_file_name = measure_IP1(SMB_RF, 
                    NRP2, 
                    SAB, 
                    synthetizer_state, 
                    synthetizer_frequency,
                    synthetizer_level_fixed, 
                    synthetizer_level,
                    power_meter_make_zero, 
                    power_meter_make_zero_delay, 
                    power_meter_misure_number, 
                    power_meter_misure_delay, 
                    SAB_state, 
                    SAB_attenuation, 
                    SAB_attenuation_delay, 
                    SAB_switch01_delay, 
                    SAB_switch02_delay, 
                    calibration_cable_file_name, 
                    result_file_name, 
                    createprogressdialog = dialog)
        
        dialog.Destroy()
        
        try:
            webbrowser.open(os.path.dirname(result_IP1_file_name))
        except:
            pass
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = IP1CalcFrame()
    app.MainLoop()