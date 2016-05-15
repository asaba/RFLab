'''
Created on 26/dic/2015

@author: sabah
'''

#import images
import wx
import os

from guitabs import TabPanelFSV, TabPanelPowerMeter, TabPanelSMB, TabPanelSpuriusSetup, TabPanelCalCableSetup, TabPanelCalDummyCableSetup, TabPanelSAB
from measure_scripts.CalibrazioneDummyCable import unit, create_calibration_cable
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK
from utility import writelineonfilesettings, return_now_postfix

TEST_MODE = False

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
class CalDummyCableFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Create Dummy Cable Calibration",
                          size=(800,650)
                          )
        
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        self.fitem = fileMenu.Append(wx.ID_OPEN, 'Load settings', 'Load settings')
        self.fitem2 = fileMenu.Append(wx.ID_SAVEAS, 'Save settings', 'Save settings')
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
                exec("{param}.SetValue({value})".format(param = parameter, value = value))
                        
    def savesettings(self, filepointer):
        
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.frequency_min_unit")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.frequency_min")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.frequency_max_unit")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.frequency_max")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.frequency_step_unit")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.frequency_step")
        #self.writelinesettings(f, "self.notebook.tabCalDummyCableSetting.level_min")
        #self.writelinesettings(f, "self.notebook.tabCalDummyCableSetting.level_max")
        #self.writelinesettings(f, "self.notebook.tabCalDummyCableSetting.level_step")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.output_frequency_unit")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.output_level")
        self.writelinesettings(filepointer, "self.notebook.tabCalDummyCableSetting.result_file_name")
                        
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
        
        if TEST_MODE:
            dlg = wx.MessageDialog(None, "Test mode", 'Test mode. Instruments comunication disabled', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            
        #Check all values "Minimum Frequency"
        frequency_min = self.notebook.tabCalDummyCableSetting.frequency_min.GetValue() 
        if check_value_min_max(frequency_min, "Minimum Frequency", minimum = 0) == 0:
            return None
        else:
            frequency_min = eval(self.notebook.tabCalDummyCableSetting.frequency_min.GetValue())
        
        #"Minimum Frequency Unit"
        frequency_min_unit = unit.return_unit(self.notebook.tabCalDummyCableSetting.frequency_min_unit.GetValue())
        if check_value_not_none(frequency_min_unit, "Minimum Frequency Unit") == 0:
            return None
        
        #"Maximum Frequency"
        frequency_max = self.notebook.tabCalDummyCableSetting.frequency_max.GetValue()
        if check_value_min_max(frequency_max, "Maximum Frequency", minimum = 0) == 0:
            return None
        else:
            frequency_max = eval(self.notebook.tabCalDummyCableSetting.frequency_max.GetValue())
        
        #"Maximum Frequency Unit"
        frequency_max_unit = unit.return_unit(self.notebook.tabCalDummyCableSetting.frequency_max_unit.GetValue())
        if check_value_not_none(frequency_max_unit, "Maximum Frequency Unit") == 0:
            return None
        
        #"Frequency Step"
        frequency_step = self.notebook.tabCalDummyCableSetting.frequency_step.GetValue()
        if check_value_min_max(frequency_step, "Frequency Step", minimum = 0) == 0:
            return None
        else:
            frequency_step = eval(self.notebook.tabCalDummyCableSetting.frequency_step.GetValue())
        
        #"Frequency Step Unit"
        frequency_step_unit = unit.return_unit(self.notebook.tabCalDummyCableSetting.frequency_step_unit.GetValue())
        if check_value_not_none(frequency_step_unit, "Frequency Step Unit") == 0:
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
        
        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        result = create_calibration_cable(frequency_min_unit, frequency_min, frequency_max_unit, frequency_max, frequency_step_unit, frequency_step, output_level, output_frequency_unit, result_file_name, createprogressdialog = dialog)
        
        dialog.Destroy()
        filesettingname = result_file_name + "_caldummycable_" + return_now_postfix() + ".cfg"
        f = open(filesettingname, "w")
        self.savesettings(f)
        f.close()
        #if result == 0:
        #    resultError()
        #else:
        #    resultOK()
 
#---------011-------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalDummyCableFrame()
    app.MainLoop()