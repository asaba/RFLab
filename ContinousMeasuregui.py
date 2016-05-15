'''
Created on 26/dic/2015

@author: sabah
'''

#import images
import wx
import os

from guitabs import TabPanelContinousVoltageSetup, TabPanelSourceMeter
from measure_scripts.CalibrazioneDummyCable import unit, create_calibration_cable
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
        self.tabSourceMeter = TabPanelSourceMeter(self)
        self.tabCountinousVoltageSetup = TabPanelContinousVoltageSetup(self)
        self.AddPage(self.tabSourceMeter, "Source Meter")
        self.AddPage(self.tabCountinousVoltageSetup, "Continous Voltage Measure Setting")
 
########################################################################
class CalContinousMeasureFrame(wx.Frame):
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
                exec("{param}.SetValue({value})".format(param = parameter, value = value))
                        
    def savesettings(self, filepointer):
        self.writelinesettings(filepointer, "self.notebook.tabSourceMeter.instrument_txt_IP")
        self.writelinesettings(filepointer, "self.notebook.tabSourceMeter.instrument_txt_Port")
        self.writelinesettings(filepointer, "self.notebook.tabSourceMeter.instrument_txt_Timeout")
        
        self.writelinesettings(filepointer, "self.notebook.tabCountinousVoltageSetup.result_file_name")
                        
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
            dlg = wx.MessageDialog(None, "Test mode", 'Test mode. Instruments comunication disabled', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        
        result_file_name = self.notebook.tabCountinousVoltageSetup.result_file_name.GetValue()
        
        

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
    frame = CalContinousMeasureFrame()
    app.MainLoop()