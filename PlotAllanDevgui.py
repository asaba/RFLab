'''
Created on 26/dic/2015

@author: sabah
'''

#import images
import wx
import os

from guitabs import TabPanelTSC
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
class PlotAllanDevFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Calibrate Cable",
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
    
    
    #def OnCheckRunMode(self, event):
    #    if self.runmodeitem.IsChecked():
    #        TEST_MODE = True
    #        #self.runmodeitem.Check()
    #    else:
    #        TEST_MODE = False
    
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
        self.writelinesettings(filepointer, "self.notebook.tabTSC.TSC_state")
        self.writelinesettings(filepointer, "self.notebook.tabTSC.instrument_txt_IP")
        self.writelinesettings(filepointer, "self.notebook.tabTSC.instrument_txt_Port")
        self.writelinesettings(filepointer, "self.notebook.tabTSC.instrument_txt_Timeout")
        self.writelinesettings(filepointer, "self.notebook.tabTSC.TSC_collecting_delay")
        self.writelinesettings(filepointer, "self.notebook.tabTSC.TSC_plot_adev")
        self.writelinesettings(filepointer, "self.notebook.tabTSC.result_file_name")         
    
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
            dlg = wx.MessageDialog(None, 'Test mode. Instruments comunication disabled',"Test mode",  wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
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
        
        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
                style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        
        TSC_measure(TSC, TSC_collecting_delay, result_file_name, TSC_plot_adev, createprogressdialog = dialog)
 
        dialog.Destroy()
        filesettingname = result_file_name + "_calcable_" + return_now_postfix() + ".cfg"
        f = open(filesettingname, "w")
        self.savesettings(f)
        f.close()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = PlotAllanDevFrame()
    app.MainLoop()