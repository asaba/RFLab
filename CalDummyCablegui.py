'''
Created on 26/dic/2015

@author: sabah
'''

#import images
from taskframe import TaskFrame

import wx
import os

from guitabs import TabPanelFSV, TabPanelPowerMeter, TabPanelSpuriusSetup, TabPanelCalCableSetup, TabPanelCalDummyCableSetup
from measure_scripts.CalibrazioneDummyCable import unit, create_calibration_cable
from measure_scripts.scriptutility import Frequency_Range
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK
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
        self.tabCalDummyCableSetting = TabPanelCalDummyCableSetup(self)
        self.AddPage(self.tabCalDummyCableSetting, "Create Calibrated Dummy Cable")
 
########################################################################
class CalDummyCableFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                          "Create Dummy Cable Calibration",
                          size=(800,650)
                          )
        
    def savesettings(self, filename):
        
        params = ["tabCalDummyCableSetting.frequency_min",
                  "tabCalDummyCableSetting.frequency_max",
                  "tabCalDummyCableSetting.frequency_step",
                  "tabCalDummyCableSetting.frequency_unit",
                  "tabCalDummyCableSetting.output_frequency_unit",
                  "tabCalDummyCableSetting.output_level",
                  "tabCalDummyCableSetting.result_file_name"]
        
        TaskFrame.framesavesettings(self, filename, params = params)
                        
    def OnStart(self, event):
        
        TaskFrame.OnStart(self, event)
            
        #Check all values "Minimum Frequency"
        frequency_min = self.notebook.tabCalDummyCableSetting.frequency_min.GetValue() 
        if check_value_min_max(frequency_min, "Minimum Frequency", minimum = 0) == 0:
            return None
        else:
            frequency_min = eval(self.notebook.tabCalDummyCableSetting.frequency_min.GetValue())
        
        #"Minimum Frequency Unit"
        #frequency_min_unit = unit.return_unit(self.notebook.tabCalDummyCableSetting.frequency_min_unit.GetValue())
        #if check_value_not_none(frequency_min_unit, "Minimum Frequency Unit") == 0:
        #    return None
        
        #"Maximum Frequency"
        frequency_max = self.notebook.tabCalDummyCableSetting.frequency_max.GetValue()
        if check_value_min_max(frequency_max, "Maximum Frequency", minimum = 0) == 0:
            return None
        else:
            frequency_max = eval(self.notebook.tabCalDummyCableSetting.frequency_max.GetValue())
        
        #"Maximum Frequency Unit"
        #frequency_max_unit = unit.return_unit(self.notebook.tabCalDummyCableSetting.frequency_max_unit.GetValue())
        #if check_value_not_none(frequency_max_unit, "Maximum Frequency Unit") == 0:
        #    return None
        
        #"Frequency Step"
        frequency_step = self.notebook.tabCalDummyCableSetting.frequency_step.GetValue()
        if check_value_min_max(frequency_step, "Frequency Step", minimum = 0) == 0:
            return None
        else:
            frequency_step = eval(self.notebook.tabCalDummyCableSetting.frequency_step.GetValue())
        
        #"Frequency Step Unit"
        frequency_unit = unit.return_unit(self.notebook.tabCalDummyCableSetting.frequency_unit.GetValue())
        if check_value_not_none(frequency_unit, "Frequency Unit") == 0:
            return None
        
        #"Output Frequency unit"
        output_frequency_unit = unit.return_unit(self.notebook.tabCalDummyCableSetting.output_frequency_unit.GetValue())
        if check_value_not_none(output_frequency_unit, "Output Frequency unit") == 0:
            return None
        
        #"Output Power Level"
        try:
            output_level = eval(self.notebook.tabCalDummyCableSetting.output_level.GetValue())
        except:
            output_level = 0
        
        
        result_file_name = self.notebook.tabCalDummyCableSetting.result_file_name.GetValue()
        
        frequency = Frequency_Range(frequency_min, frequency_max, frequency_step, frequency_unit)
        frequency.to_base()
        
        self.savesettings(result_file_name)
        
        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        result = create_calibration_cable(frequency, 
                                          output_level, 
                                          output_frequency_unit, 
                                          result_file_name, 
                                          createprogressdialog = dialog)
        
        dialog.Destroy()

 
#---------011-------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalDummyCableFrame()
    app.MainLoop()