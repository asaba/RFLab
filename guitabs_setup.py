'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os

from guiobjects import return_textbox_labeled, return_comboBox_unit, return_file_browse, return_min_max_step_labeled, \
    return_spinctrl_min_max
from utilitygui import browse_file

from measure_scripts.csvutility import *

fig1 = None


class SetupPanelClass(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.result_file_name, self.result_file_name_button, dummy, self.sizer_result_file_name = return_file_browse(
            self, "Output File")
        self.result_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_Out)

    def File_browser_Out(self, event):
        browse_file(self, self.result_file_name, wildcard="*", mode=wx.FD_SAVE)
        # dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*", wx.SAVE)
        # if dlg.ShowModal() == wx.ID_OK:
        #    path = dlg.GetPath()
        #    self.result_file_name.SetValue(path)
        # else:
        #    self.result_file_name.SetValue("")
        # dlg.Destroy()


class TabPanelContinousVoltageSetup(SetupPanelClass):
    """
    Tab for Continous Voltage Measure
    """

    def __init__(self, parent):
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Calibration Cable parameter

        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)

        self.SetSizer(sizer)


class TabPanelContinousPowerMeterSetup(SetupPanelClass):
    """
    Tab for Continous Voltage Measure
    """

    def __init__(self, parent):
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Calibration Cable parameter

        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)

        self.SetSizer(sizer)

class TabPanelCalDummyCableSetup(SetupPanelClass):
    """
    Tab for Dummy Cable Calibration parameters
    """

    def __init__(self, parent):
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        # Calibration Cable parameter
        # self.frequency_min, self.frequency_min_unit, self.frequency_max, self.frequency_max_unit, self.frequency_step, self.frequency_step_unit, dummy, dummy, self.sizer_frequency = return_min_max_step_labeled(self, "Frequency", unit = True)
        self.frequency_min, dummy, self.frequency_max, dummy, self.frequency_step, dummy, self.frequency_unit, dummy, self.sizer_frequency = return_min_max_step_labeled(
            self, "Frequency", unit=False, single_unit=True)

        # synthetizer_LO_level_min = 6 #dBm
        self.output_level, dummy, dummy, self.sizer_output_level, dummy, dummy = return_textbox_labeled(self,
                                                                                                        "Output Power Level")

        self.output_frequency_unit, self.sizer_output_frequency_unit = return_comboBox_unit(self,
                                                                                            "Output Frequency unit")

        sizer.Add(self.sizer_frequency, 0, wx.ALL, 5)
        sizer.Add(self.sizer_output_level, 0, wx.ALL, 5)
        sizer.Add(self.sizer_output_frequency_unit, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)

        self.SetSizer(sizer)


class TabPanelCalCableSetup(SetupPanelClass):
    """
    Tab for Cable Calibration parameters
    """

    def __init__(self, parent):
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.output_level, dummy, self.create_dummycable_cb, self.sizer_output_level, dummy, dummy = return_textbox_labeled(
            self, "Output Power Level (Dummy Cable)", enabled=True, enable_text="Create Dummy Cable")

        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_output_level, 0, wx.ALL, 5)

        self.SetSizer(sizer)


class TabPanelIP1CalcSetup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """

    def __init__(self, parent):
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # IP1 calculation variables

        self.calibration_file_RF, self.calibration_file_RF_button, self.calibration_file_RF_enable, self.sizer_calibration_file_RF = return_file_browse(
            self, "Radio Frequency Cable Calibration File", enabled=True)
        self.calibration_file_RF_button.Bind(wx.EVT_BUTTON, self.File_browser_RF)

        sizer.Add(self.sizer_calibration_file_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def File_browser_RF(self, event):
        browse_file(self, self.calibration_file_RF)


class TabPanelSpuriusSetup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """

    def __init__(self, parent):
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # spurius calculation variables

        # m_max_RF = 7
        # self.m_max_RF, self.sizer_m_max_RF = return_spinctrl(self, "Max m for RF")
        self.m_min_RF, self.m_max_RF, self.m_step_RF, self.sizer_m_RF = return_spinctrl_min_max(self,
                                                                                                "m for RF (min/max/step)")
        # n_max_LO = 7
        # self.n_max_LO, self.sizer_n_max_LO = return_spinctrl(self, "Max n for LO")
        self.n_min_LO, self.n_max_LO, self.n_step_LO, self.sizer_n_LO = return_spinctrl_min_max(self,
                                                                                                "n for LO (min/max/step)")

        # IF_high = 3000
        self.IF_low, self.IF_low_unit, dummy, self.sizer_IF_low, dummy, dummy = return_textbox_labeled(self,
                                                                                                       "Min Spurius Frequency",
                                                                                                       unit=True)

        # IF_high = 3000
        self.IF_high, self.IF_high_unit, dummy, self.sizer_IF_high, dummy, dummy = return_textbox_labeled(self,
                                                                                                          "Max Spurius Frequency",
                                                                                                          unit=True)

        # spurius_IF_unit = unit.MHz
        self.spurius_IF_unit, self.sizer_spurius_IF_unit = return_comboBox_unit(self, "Spurius Frequency unit")

        # calibration_file_LO = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_LO, self.calibration_file_LO_button, self.calibration_file_LO_enable, self.sizer_calibration_file_LO = return_file_browse(
            self, "Local Ocillator Cable Calibration File", enabled=True)
        self.calibration_file_LO_button.Bind(wx.EVT_BUTTON, self.File_browser_LO)

        # calibration_file_RF = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_RF, self.calibration_file_RF_button, self.calibration_file_RF_enable, self.sizer_calibration_file_RF = return_file_browse(
            self, "Radio Frequency Cable Calibration File", enabled=True)
        self.calibration_file_RF_button.Bind(wx.EVT_BUTTON, self.File_browser_RF)

        # calibration_file_IF = ""
        self.calibration_file_IF, self.calibration_file_IF_button, self.calibration_file_IF_enable, self.sizer_calibration_file_IF = return_file_browse(
            self, "Output Frequency Cable Calibration File", enabled=True)
        self.calibration_file_IF_button.Bind(wx.EVT_BUTTON, self.File_browser_IF)

        sizer.Add(self.sizer_m_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_n_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_IF_low, 0, wx.ALL, 5)
        sizer.Add(self.sizer_IF_high, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_RF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_calibration_file_IF, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spurius_IF_unit, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def File_browser_LO(self, event):
        browse_file(self, self.calibration_file_LO)

    def File_browser_RF(self, event):
        browse_file(self, self.calibration_file_RF)

    def File_browser_IF(self, event):
        browse_file(self, self.calibration_file_IF)


class TabPanelPM5Setup(SetupPanelClass):
    """
    Tab for Spurius parameters
    """

    def __init__(self, parent):
        SetupPanelClass.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # calibration_file_LO = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal.csv"
        self.calibration_file_LO, self.calibration_file_LO_button, self.calibration_file_LO_enable, self.sizer_calibration_file_LO = return_file_browse(
            self, "Local Ocillator Cable Calibration File", enabled=True)
        self.calibration_file_LO_button.Bind(wx.EVT_BUTTON, self.File_browser_LO)

        sizer.Add(self.sizer_calibration_file_LO, 0, wx.ALL, 5)
        sizer.Add(self.sizer_result_file_name, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def File_browser_LO(self, event):
        browse_file(self, self.calibration_file_LO)
