'''
Created on 26/dic/2015

@author: sabah
'''

#import images
from taskframe import TaskFrame
import wx
import os

from guitabs_instruments import TabPanelPowerMeter, TabPanelSMB, TabPanelSAB
from guitabs_setup import TabPanelCalCableSetup
from measure_scripts.CalibrazioneCavo import unit, measure_calibration_cable, SMB_RF, NRP2, SAB
from measure_scripts.scriptutility import Frequency_Range
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument, info_message
import webbrowser



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
        self.tabRF = TabPanelSMB(self, range_power = False)
        self.AddPage(self.tabRF, "Radio Frequency")
 
        self.tabPowerMeter = TabPanelPowerMeter(self)
        self.AddPage(self.tabPowerMeter, "Power Meter")
        
        self.tabSAB = TabPanelSAB(self, attenutation = False, switches = True)
        self.AddPage(self.tabSAB, "SwitchAttBox")
        
        self.tabCalCableSetting = TabPanelCalCableSetup(self)
        self.AddPage(self.tabCalCableSetting, "Calibrate Cable")
 
########################################################################
class CalCableFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                          "Calibrate Cable",
                          size=(800,650)
                          )
        
    def savesettings(self, filename):
        
        params = ["tabRF.instrument_enable_status",
        "tabRF.instrument_txt_IP",
        "tabRF.instrument_txt_Port",
        "tabRF.instrument_txt_Timeout",
        "tabRF.combobox_instrtype",
        "tabRF.synthetizer_frequency_min",
        "tabRF.synthetizer_frequency_max",
        "tabRF.synthetizer_frequency_step",
        "tabRF.synthetizer_frequency_unit",
        "tabRF.synthetizer_level_fixed",
        "tabPowerMeter.instrument_enable_status",
        "tabPowerMeter.instrument_txt_IP",
        "tabPowerMeter.instrument_txt_Port",
        "tabPowerMeter.instrument_txt_Timeout",
        "tabPowerMeter.combobox_instrtype",
        "tabPowerMeter.power_meter_make_zero",
        "tabPowerMeter.power_meter_misure_number",
        "tabPowerMeter.power_meter_misure_delay",
        "tabSAB.instrument_enable_status",
        "tabSAB.instrument_txt_IP",
        "tabSAB.instrument_txt_Port",
        "tabSAB.instrument_txt_Timeout",
        "tabSAB.combobox_instrtype",
        "tabSAB.SAB_switch01_delay",
        "tabSAB.SAB_switch02_delay",
        "tabSAB.SAB_switch03_delay",
        "tabCalCableSetting.result_file_name", 
        "tabCalCableSetting.output_level",
        "tabCalCableSetting.create_dummycable_cb"]
        
        TaskFrame.framesavesettings(self, filename, params = params)         
    
    def OnStart(self, event):
                
        TaskFrame.OnStart(self, event)
        
        create_dummy_cable = self.notebook.tabCalCableSetting.create_dummycable_cb.GetValue()
        
        if create_dummy_cable:
            info_message("Dummy cable creation mode. \n No instrument used.", "Dummy Cable Mode")
        
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
        
        syntetizer_enable_state = self.notebook.tabRF.instrument_enable_status.GetValue()
        
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
        if check_value_min_max(synthetizer_frequency_step, "Frequency Step", minimum = 0) == 0:
            return None
        else:
            synthetizer_frequency_step = eval(self.notebook.tabRF.synthetizer_frequency_step.GetValue())
        synthetizer_frequency_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_unit.GetValue())
        if check_value_not_none(synthetizer_frequency_unit, "Frequency Unit") == 0:
            return None
        
        
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
    
        power_meter_enable_state = self.notebook.tabPowerMeter.instrument_enable_status.GetValue()

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
        
        SAB_enable_state = self.notebook.tabSAB.instrument_enable_status.GetValue()
        
        SAB_instrType = self.notebook.tabSAB.combobox_instrtype.GetValue()
        
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
        result_file_name = self.notebook.tabCalCableSetting.result_file_name.GetValue()
        dummy_cable_power_level = self.notebook.tabCalCableSetting.output_level.GetValue()
        
        if create_dummy_cable:
            if check_value_not_none(dummy_cable_power_level, "Power Level (Dummy Cable)") == 0:
                return None

        try:
            SMB_RF = create_instrument(synthetizer_IP, synthetizer_Port, eval(synthetizer_Timeout), syntetizer_instrType, TEST_MODE = self.runmodeitem.IsChecked(), enable_state = syntetizer_enable_state and not create_dummy_cable)
        except:
            dlg = wx.MessageDialog(None, "Synthetizer comunication error", 'Error Synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            NRP2 = create_instrument(power_meter_IP, power_meter_Port, eval(power_meter_Timeout), power_meter_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "NRP2", enable_state = power_meter_enable_state and not create_dummy_cable)
        except:
            dlg = wx.MessageDialog(None, "Power meter comunication error", 'Error Power meter', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            SAB = create_instrument(SAB_IP, SAB_Port, eval(SAB_Timeout), SAB_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "SAB", enable_state = SAB_enable_state and not create_dummy_cable)
        except:
            dlg = wx.MessageDialog(None, "SwitchAttBox comunication error", 'Error SwitchAttBox', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
          
        self.savesettings(result_file_name)
        
        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        synthetizer_frequency = Frequency_Range(synthetizer_frequency_min, synthetizer_frequency_max, synthetizer_frequency_step, synthetizer_frequency_unit)
        synthetizer_frequency.to_base()
        
        calibration_file_result = measure_calibration_cable(SMB_RF, 
                                  NRP2, 
                                  SAB, 
                                  synthetizer_frequency, 
                                  synthetizer_level_fixed, 
                                  power_meter_make_zero, 
                                  power_meter_make_zero_delay, 
                                  power_meter_misure_number, 
                                  power_meter_misure_delay, 
                                  SAB_switch01_delay, 
                                  SAB_switch02_delay, 
                                  result_file_name, 
                                  dummy_cable_power_level,
                                  create_dummy_cable,
                                  createprogressdialog = dialog)
 
        dialog.Destroy()
        
        try:
            webbrowser.open(os.path.dirname(calibration_file_result))
        except:
            pass
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalCableFrame()
    app.MainLoop()