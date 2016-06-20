'''
Created on 26/dic/2015

@author: sabah
'''

#import images
from taskframe import TaskFrame

import wx
import os

from guitabs_instruments import TabPanelTSC
from measure_scripts.CalculateAllanDeviation import unit, TSC_measure
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, check_value_is_IP, create_instrument
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
        self.tabTSC = TabPanelTSC(self)
        self.AddPage(self.tabTSC, "TSC5115A Phase noise test")
 
########################################################################
class PlotAllanDevFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                          "Calculate Allan Deviation",
                          size=(800,650)
                          )
        
                        
    def savesettings(self, filename):
        
        params = ["tabTSC.instrument_enable_status",
        "tabTSC.instrument_txt_IP",
        "tabTSC.instrument_txt_Port",
        "tabTSC.instrument_txt_Timeout",
        "tabTSC.combobox_instrtype",
        "tabTSC.TSC_collecting_delay",
        "tabTSC.TSC_plot_adev",
        "tabTSC.result_file_name"]    
        
        TaskFrame.framesavesettings(self, filename, params = params)     
    
    
    def OnStart(self, event):
                
        TaskFrame.OnStart(self, event)
        
        #Check all values
        TSC_IP = self.notebook.tabTSC.instrument_txt_IP.GetValue()
        if check_value_is_IP(TSC_IP, "TSC IP") == 0:
            return None
        
        TSC_Port = self.notebook.tabTSC.instrument_txt_Port.GetValue()
        if check_value_min_max(TSC_Port, "TSC Port", minimum = 0) == 0:
            return None
        
        TSC_Timeout = self.notebook.tabTSC.instrument_txt_Timeout.GetValue()
        if check_value_min_max(TSC_Timeout, "TSC Timeout", minimum = 0) == 0:
            return None

        TSC_instrType = self.notebook.tabTSC.combobox_instrtype.GetValue()
        

        TSC_collecting_delay = self.notebook.tabTSC.TSC_collecting_delay.GetValue()
        if check_value_min_max(TSC_collecting_delay, "Collecting time", minimum = 0) == 0:
            return None
        else:
            TSC_collecting_delay = eval(self.notebook.tabTSC.TSC_collecting_delay.GetValue())
        
        TSC_plot_adev = self.notebook.tabTSC.TSC_plot_adev.GetValue()
        
        result_file_name = self.notebook.tabTSC.result_file_name.GetValue()
        
        try:
            TSC = create_instrument(TSC_IP, TSC_Port, eval(TSC_Timeout), TSC_instrType, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class = "TSC")
        except:
            dlg = wx.MessageDialog(None, "TSC comunication error", 'Error TSC', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        self.savesettings(result_file_name)
        
        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        TSC_measure(TSC, TSC_collecting_delay, result_file_name, TSC_plot_adev, createprogressdialog = dialog)
 
        dialog.Destroy()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = PlotAllanDevFrame()
    app.MainLoop()