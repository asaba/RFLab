'''
Created on 26/dic/2015

@author: sabah
'''

# import images
from taskframe import TaskFrame
import wx
import os

from guitabs_instruments import TabPanelSourceMeter
from guitabs_setup import TabPanelContinousVoltageSetup
from measure_scripts.CalibrazioneDummyCable import unit, create_calibration_cable
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK


class NotebookDemo(wx.Notebook):
    """
    Notebook class
    """

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
        wx.BK_DEFAULT
                             # wx.BK_TOP
                             # wx.BK_BOTTOM
                             # wx.BK_LEFT
                             # wx.BK_RIGHT
                             )
        self.tabSourceMeter = TabPanelSourceMeter(self)
        self.tabCountinousVoltageSetup = TabPanelContinousVoltageSetup(self)
        self.AddPage(self.tabSourceMeter, "Source Meter")
        self.AddPage(self.tabCountinousVoltageSetup, "Continous Voltage Measure Setting")


########################################################################
class CalContinousMeasureFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                           "Continous Measure",
                           size=(800, 650)
                           )

    def savesettings(self, filename):
        params = ["tabSourceMeter.instrument_txt_IP",
                  "tabSourceMeter.instrument_txt_Port",
                  "tabSourceMeter.instrument_txt_Timeout",
                  "tabSourceMeter.combobox_instrtype",
                  "tabCountinousVoltageSetup.result_file_name"]

        TaskFrame.framesavesettings(self, filename, params=params)

    def OnStart(self, event):
        TaskFrame.OnStart(self, event)

        result_file_name = self.notebook.tabCountinousVoltageSetup.result_file_name.GetValue()

        # Insert function

        self.savesettings(result_file_name)


# ---------011-------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalContinousMeasureFrame()
    app.MainLoop()
