'''
Created on 11/giu/2016

@author: sabah
'''
import wx
import os
from utility import writelineonfilesettings, return_now_postfix

class TaskFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self, NotebookDemo, frametitle, size = (800, 650), start_button = True):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          frametitle,
                          size=size
                          )
        
        self.menubar = wx.MenuBar()
        self.fileMenu = wx.Menu()
        
        self.fitem = self.fileMenu.Append(wx.ID_OPEN, 'Load settings', 'Load settings')
        self.fitem2 = self.fileMenu.Append(wx.ID_SAVEAS, 'Save settings', 'Save settings')
        self.runmodeitem = self.fileMenu.AppendCheckItem(7890, "Testing Mode", "Enable testing mode")
        self.menubar.Append(self.fileMenu, '&File')
        self.SetMenuBar(self.menubar)
        
        self.Bind(wx.EVT_MENU, self.OnLoadSettings, self.fitem)
        self.Bind(wx.EVT_MENU, self.OnSaveSettings, self.fitem2)
        #self.Bind(wx.EVT_MENU, self.OnCheckRunMode, self.runmodeitem)
        self.panel = wx.Panel(self)
        if start_button:
            
            self.btn_execute = wx.Button(self.panel, 0, 'Start')
            self.btn_execute.Bind(wx.EVT_BUTTON, self.OnStart)
        
        self.notebook = NotebookDemo(self.panel)
        #notebook2 = NotebookDemo(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
        #sizer.Add(notebook2, 0, wx.ALL|wx.EXPAND, 5)
        if start_button:
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
                        
    def framesavesettings(self, result_file_name, params):
        
        setting_file_path = os.path.join(result_file_name, "_".join(["Config", return_now_postfix()]))
        if not os.path.exists(setting_file_path):
            try:
                os.makedirs(setting_file_path)
            except:
                print("Error creating " + setting_file_path)
                return 0
        
        filesettingname = os.path.join(setting_file_path, "config.cfg")
        f = open(filesettingname, "w")
        for p in params:
            self.writelinesettings(f, "self.notebook." + p)
        #self.savesettings(f)
        f.close()
        
        
        
    
    
    def OnSaveSettings(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.cfg", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            f = dlg.GetPath()
            #f = open(path, "w")
            self.savesettings(f)
            #f.close()
                        
    def writelinesettings(self, f, parameter):
        value = None
        exec("value = {param}.GetValue()".format(param = parameter))
        writelineonfilesettings(f, parameter, value)
    
    def OnStart(self, event):
                
        if self.runmodeitem.IsChecked():
            dlg = wx.MessageDialog(None, 'Test mode. Instruments comunication disabled', "Test mode",  wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
        