'''
Created on 26/dic/2015

@author: sabah
'''

#import images
import wx
import os

from guitabs import TabPanelSMB, TabPanelPM5Setup, TabPanelPM5
from measure_scripts.Cal100GHz import unit, measure_100GHz_cal, SMB_RF, PM5
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument,\
    create_USB_instrument
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
        self.AddPage(self.tabRF, "Radio Frequency")
 
        self.tabPM5 = TabPanelPM5(self)
        self.AddPage(self.tabPM5, "mm-submm Power Meter")
        
        self.tabPM5Setting = TabPanelPM5Setup(self)
        self.AddPage(self.tabPM5Setting, "Sweep")
 
########################################################################
class CalPM5Frame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "PM5",
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
        
        self.writelinesettings(filepointer, "self.notebook.tabPM5.instrument_combobox_com_port")
        self.writelinesettings(filepointer, "self.notebook.tabPM5.instrument_txt_timeout")
        self.writelinesettings(filepointer, "self.notebook.tabPM5.instrument_combobox_baud")
        self.writelinesettings(filepointer, "self.notebook.tabPM5.pm5_misure_number")
        self.writelinesettings(filepointer, "self.notebook.tabPM5.pm5_misure_delay")
        self.writelinesettings(filepointer, "self.notebook.tabPM5.pm5_state")
        self.writelinesettings(filepointer, "self.notebook.tabPM5Setting.calibration_file_LO")

        self.writelinesettings(filepointer, "self.notebook.tabPM5Setting.result_file_name")         
    
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
        
        synthetizer_LO_state = self.notebook.tabRF.synthetizer_state.GetValue()
        

        
        
        
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
        if check_value_min_max(synthetizer_frequency_step, "Frequency Step", minimum = 0) == 0:
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
        
        pm5_state = self.notebook.tabPM5.pm5_state.GetValue()

        
        pm5_com_port = self.notebook.tabPM5.instrument_combobox_com_port.GetValue()
        
        pm5_Timeout = self.notebook.tabPM5.instrument_txt_timeout.GetValue()
        if check_value_min_max(pm5_Timeout, "PM5 Timeout", minimum = 0) == 0:
            return None
        
        pm5_BaudRate = self.notebook.tabPM5.instrument_combobox_baud.GetValue()
        if check_value_min_max(pm5_BaudRate, "COM Baud Rate", minimum = 0) == 0:
            return None

        pm5_misure_number = self.notebook.tabPM5.pm5_misure_number.GetValue()
            
        pm5_misure_delay = self.notebook.tabPM5.pm5_misure_delay.GetValue() #seconds
        if check_value_min_max(pm5_misure_delay, "Measure Delay", minimum = 0) == 0:
            return None
        else:
            pm5_misure_delay = eval(self.notebook.tabPM5.pm5_misure_delay.GetValue())
        
        calibration_file_LO = self.notebook.tabPM5Setting.calibration_file_LO.GetValue()
        calibration_file_LO_enable = self.notebook.tabPM5Setting.calibration_file_LO_enable.GetValue()
        if calibration_file_LO_enable:
            if check_value_is_valid_file(calibration_file_LO, "LO Calibration file") == 0:
                return None
        
        result_file_name = self.notebook.tabPM5Setting.result_file_name.GetValue()
        
        try:
            if synthetizer_LO_state:
                SMB_LO = create_instrument(synthetizer_IP, synthetizer_Port, eval(synthetizer_Timeout), syntetizer_instrType, TEST_MODE = self.runmodeitem.IsChecked())
            else:
                SMB_LO = create_instrument(synthetizer_IP, synthetizer_Port, eval(synthetizer_Timeout), syntetizer_instrType, TEST_MODE = True)
        except:
            dlg = wx.MessageDialog(None, "LO synthetizer comunication error", 'Error LO synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
        
        try:
            if pm5_state:
                PM5 = create_USB_instrument(pm5_com_port, pm5_Timeout, pm5_BaudRate, TEST_MODE = self.runmodeitem.IsChecked(), instrument_class="PM5")
            else:
                PM5 = create_USB_instrument(pm5_com_port, pm5_Timeout, pm5_BaudRate, TEST_MODE = True, instrument_class="PM5")
        except:
            dlg = wx.MessageDialog(None, "PM5 comunication error", 'Error mm-submm power meter', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0
            
            #dlg.ShowModal()
            #return 0
        
        
        #dialog = wx.ProgressDialog("Progress", "Time remaining", maximum = 100,
        #        style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        dialog =None
        measure_100GHz_cal(SMB_LO, PM5, synthetizer_frequency_min_unit, synthetizer_frequency_min, synthetizer_frequency_max_unit, synthetizer_frequency_max, synthetizer_frequency_step_unit, synthetizer_frequency_step, synthetizer_level_min, synthetizer_level_max, synthetizer_level_step, calibration_file_LO, pm5_misure_number, pm5_misure_delay, result_file_name, createprogressdialog = dialog)

        #dialog.Destroy()
        filesettingname = result_file_name + "_calcable_" + return_now_postfix() + ".cfg"
        f = open(filesettingname, "w")
        self.savesettings(f)
        f.close()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalPM5Frame()
    app.MainLoop()