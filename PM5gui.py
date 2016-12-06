'''
Created on 26/dic/2015

@author: sabah
'''

# import images
from taskframe import TaskFrame
import wx
import os

from guitabs_instruments import TabPanelSMB, TabPanelPM5
from guitabs_setup import TabPanelPM5Setup
from measure_scripts.Cal100GHz import unit, measure_100GHz_cal, SMB_RF, PM5
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, \
    check_value_is_IP, create_instrument, \
    create_USB_instrument
from utility import writelineonfilesettings, return_now_postfix, \
    Generic_Range
from measure_scripts.scriptutility import Frequency_Range


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

        # Create and add the second tab
        self.tabRF = TabPanelSMB(self)
        self.AddPage(self.tabRF, "Radio Frequency")

        self.tabPM5 = TabPanelPM5(self)
        self.AddPage(self.tabPM5, "mm-submm Power Meter")

        self.tabPM5Setting = TabPanelPM5Setup(self)
        self.AddPage(self.tabPM5Setting, "Sweep")


########################################################################
class CalPM5Frame(TaskFrame):
    """
    Frame that holds all other widgets
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                           "PM5",
                           size=(800, 650)
                           )

    def savesettings(self, filename):
        params = ["tabRF.instrument_enable_status",
                  "tabRF.instrument_txt_IP",
                  "tabRF.instrument_txt_Port",
                  "tabRF.instrument_txt_Timeout",
                  "tabRF.combobox_instrtype",
                  "tabRF.synthetizer_frequency_min",
                  "tabRF.synthetizer_frequency_max",
                  "tabRF.synthetizer_frequency_step",
                  "tabRF.synthetizer_frequency_unit",
                  "tabRF.synthetizer_level_min",
                  "tabRF.synthetizer_level_max",
                  "tabRF.synthetizer_level_step",
                  "tabPM5.instrument_combobox_com_port",
                  "tabPM5.instrument_txt_timeout",
                  "tabPM5.instrument_combobox_baud",
                  "tabPM5.pm5_misure_number",
                  "tabPM5.pm5_misure_delay",
                  "tabPM5.instrument_enable_status",
                  "tabPM5Setting.calibration_file_LO",
                  "tabPM5Setting.calibration_file_LO_enable",
                  "tabPM5Setting.result_file_name"]

        TaskFrame.framesavesettings(self, filename, params=params)

    def OnStart(self, event):

        TaskFrame.OnStart(self, event)

        synthetizer_LO_state = self.notebook.tabRF.synthetizer_state.GetValue()

        synthetizer_IP = self.notebook.tabRF.instrument_txt_IP.GetValue()
        if check_value_is_IP(synthetizer_IP, "Synthetizer IP") == 0:
            return None

        synthetizer_Port = self.notebook.tabRF.instrument_txt_Port.GetValue()
        if check_value_min_max(synthetizer_Port, "Synthetizer Port", minimum=0) == 0:
            return None

        synthetizer_Timeout = self.notebook.tabRF.instrument_txt_Timeout.GetValue()
        if check_value_min_max(synthetizer_Timeout, "Synthetizer Timeout", minimum=0) == 0:
            return None

        syntetizer_instrType = self.notebook.tabRF.combobox_instrtype.GetValue()

        # synthetizer_frequency_min_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_min_unit.GetValue())
        # if check_value_not_none(synthetizer_frequency_min_unit, "Minimum Frequency Unit") == 0:
        #    return None
        synthetizer_frequency_min = self.notebook.tabRF.synthetizer_frequency_min.GetValue()
        if check_value_min_max(synthetizer_frequency_min, "Minimum Frequency", minimum=0) == 0:
            return None
        else:
            synthetizer_frequency_min = eval(self.notebook.tabRF.synthetizer_frequency_min.GetValue())
        # synthetizer_frequency_max_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_max_unit.GetValue())
        # if check_value_not_none(synthetizer_frequency_max_unit, "Maximum Frequency Unit") == 0:
        #    return None
        synthetizer_frequency_max = self.notebook.tabRF.synthetizer_frequency_max.GetValue()
        if check_value_min_max(synthetizer_frequency_max, "Maximum Frequency", minimum=0) == 0:
            return None
        else:
            synthetizer_frequency_max = eval(self.notebook.tabRF.synthetizer_frequency_max.GetValue())
        # synthetizer_frequency_step_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_step_unit.GetValue())
        # if check_value_not_none(synthetizer_frequency_step_unit, "Frequency Step Unit") == 0:
        #    return None
        synthetizer_frequency_step = self.notebook.tabRF.synthetizer_frequency_step.GetValue()
        if check_value_min_max(synthetizer_frequency_step, "Frequency Step", minimum=0) == 0:
            return None
        else:
            synthetizer_frequency_step = eval(self.notebook.tabRF.synthetizer_frequency_step.GetValue())
        synthetizer_frequency_unit = unit.return_unit(self.notebook.tabRF.synthetizer_frequency_unit.GetValue())
        if check_value_not_none(synthetizer_frequency_unit, "Frequency Unit") == 0:
            return None

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
        if check_value_min_max(pm5_Timeout, "PM5 Timeout", minimum=0) == 0:
            return None

        pm5_BaudRate = self.notebook.tabPM5.instrument_combobox_baud.GetValue()
        if check_value_min_max(pm5_BaudRate, "COM Baud Rate", minimum=0) == 0:
            return None

        pm5_misure_number = self.notebook.tabPM5.pm5_misure_number.GetValue()

        pm5_misure_delay = self.notebook.tabPM5.pm5_misure_delay.GetValue()  # seconds
        if check_value_min_max(pm5_misure_delay, "Measure Delay", minimum=0) == 0:
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
                SMB_LO = create_instrument(synthetizer_IP, synthetizer_Port, eval(synthetizer_Timeout),
                                           syntetizer_instrType, TEST_MODE=self.runmodeitem.IsChecked())
            else:
                SMB_LO = create_instrument(synthetizer_IP, synthetizer_Port, eval(synthetizer_Timeout),
                                           syntetizer_instrType, TEST_MODE=True)
        except:
            dlg = wx.MessageDialog(None, "LO synthetizer comunication error", 'Error LO synthetizer',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0

        try:
            if pm5_state:
                PM5 = create_USB_instrument(pm5_com_port, pm5_Timeout, pm5_BaudRate,
                                            TEST_MODE=self.runmodeitem.IsChecked(), instrument_class="PM5")
            else:
                PM5 = create_USB_instrument(pm5_com_port, pm5_Timeout, pm5_BaudRate, TEST_MODE=True,
                                            instrument_class="PM5")
        except:
            dlg = wx.MessageDialog(None, "PM5 comunication error", 'Error mm-submm power meter', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0

            # dlg.ShowModal()
            # return 0

        synthetizer_frequency = Frequency_Range(synthetizer_frequency_min, synthetizer_frequency_max,
                                                synthetizer_frequency_step, synthetizer_frequency_unit)
        synthetizer_frequency.to_base()
        synthetizer_level = Generic_Range(synthetizer_level_min, synthetizer_level_max, synthetizer_level_step)

        self.savesettings(result_file_name)

        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum=100,
                                   style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)
        # dialog =None
        measure_100GHz_cal(SMB_LO,
                           PM5,
                           synthetizer_frequency,
                           synthetizer_level,
                           calibration_file_LO,
                           pm5_misure_number,
                           pm5_misure_delay,
                           result_file_name,
                           createprogressdialog=dialog)

        dialog.Destroy()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalPM5Frame()
    app.MainLoop()
