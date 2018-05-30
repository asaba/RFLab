'''
Created on 26/dic/2015

@author: sabah
'''

# import images
from taskframe import TaskFrame
import wx
import os

from guitabs_instruments import TabPanelPowerMeter
from guitabs_setup import TabPanelContinousPowerMeterSetup
from measure_scripts.ContinousMeasurePM import unit, continous_measure_PM
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, check_value_is_IP, create_instrument


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
        self.tabPowerMeter = TabPanelPowerMeter(self)
        self.tabCountinousPMSetup = TabPanelContinousPowerMeterSetup(self)
        self.AddPage(self.tabPowerMeter, "Power Meter")
        self.AddPage(self.tabCountinousPMSetup, "Continous PM Measure Setting")


########################################################################
class CalContinousMeasurePMFrame(TaskFrame):
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
        params = ["tabPowerMeter.instrument_txt_IP",
                  "tabPowerMeter.instrument_txt_Port",
                  "tabPowerMeter.instrument_txt_Timeout",
                  "tabPowerMeter.combobox_instrtype",
                  "tabCountinousPMSetup.result_file_name"]

        TaskFrame.framesavesettings(self, filename, params=params)

    def OnStart(self, event):
        TaskFrame.OnStart(self, event)

        PM_IP = self.notebook.tabPowerMeter.instrument_txt_IP.GetValue()
        if check_value_is_IP(PM_IP, "PM IP") == 0:
            return None

        PM_Port = self.notebook.tabPowerMeter.instrument_txt_Port.GetValue()
        if check_value_min_max(PM_Port, "PM Port", minimum=0) == 0:
            return None

        PM_Timeout = self.notebook.tabPowerMeter.instrument_txt_Timeout.GetValue()
        if check_value_min_max(PM_Timeout, "PM Timeout", minimum=0) == 0:
            return None

        PM_instrType = self.notebook.tabPowerMeter.combobox_instrtype.GetValue()


        power_meter_misure_number = self.notebook.tabPowerMeter.power_meter_misure_number.GetValue()
        if power_meter_misure_number>0:
            pm_misure_number = power_meter_misure_number
        else:
            dlg = wx.MessageDialog(None, "PM number of measures is invalid", 'Error PM',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0

        power_meter_misure_delay = self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue()
        if check_value_min_max(power_meter_misure_delay, "Measures delay", minimum=0) == 0:
            return None
        else:
            pm_misure_delay = eval(self.notebook.tabPowerMeter.power_meter_misure_delay.GetValue())

        result_file_name = self.notebook.tabCountinousPMSetup.result_file_name.GetValue()

        try:
            PM = create_instrument(PM_IP, PM_Port, eval(PM_Timeout),
                                       PM_instrType, TEST_MODE=self.runmodeitem.IsChecked())
        except:
            dlg = wx.MessageDialog(None, "PM comunication error", 'Error PM',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0


        self.savesettings(result_file_name)

        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum=100,
                                   style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        # dialog =None
        continous_measure_PM(PM,
                           pm_misure_number,
                           pm_misure_delay,
                           result_file_name,
                           createprogressdialog=dialog)

        dialog.Destroy()


# ---------011-------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalContinousMeasurePMFrame()
    app.MainLoop()
