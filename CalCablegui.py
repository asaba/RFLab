'''
Created on 26/dic/2015

@author: sabah
'''

# import images
from taskframe import TaskFrame
import wx
import os

from guitabs_instruments import TabPanelFSV, TabPanelSMB, TabPanelSAB
from guitabs_setup import TabPanelCalCableSetup
from measure_scripts.CalibrazioneCavo import unit, measure_calibration_cable, SMB_RF
from measure_scripts.scriptutility import Frequency_Range
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, \
    check_value_is_IP, create_instrument, info_message
import webbrowser


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
        self.tabRF = TabPanelSMB(self, range_power=False)
        self.AddPage(self.tabRF, "Radio Frequency")

        self.tabFSV = TabPanelFSV(self)
        self.AddPage(self.tabFSV, "Spectrum Analyser")

        self.tabCalCableSetting = TabPanelCalCableSetup(self)
        self.AddPage(self.tabCalCableSetting, "Calibrate Cable")


########################################################################
class CalCableFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                           "Calibrate Cable",
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
                  "tabRF.synthetizer_level_fixed",
                  "tabFSV.instrument_txt_IP",
                  "tabFSV.instrument_txt_Port",
                  "tabFSV.instrument_txt_Timeout",
                  "tabFSV.combobox_instrtype",
                  "tabFSV.instrument_enable_status",
                  "tabFSV.spectrum_analyzer_sweep_points",
                  "tabFSV.spectrum_analyzer_resolution_bandwidth",
                  "tabFSV.spectrum_analyzer_resolution_bandwidth_unit",
                  "tabFSV.spectrum_analyzer_video_bandwidth",
                  "tabFSV.spectrum_analyzer_video_bandwidth_unit",
                  "tabFSV.spectrum_analyzer_frequency_span",
                  "tabFSV.spectrum_analyzer_frequency_span_unit",
                  "tabFSV.gainAmplifier",
                  "tabFSV.spectrum_analyzer_IF_atten_enable",
                  "tabFSV.spectrum_analyzer_IF_atten",
                  "tabFSV.spectrum_analyzer_IF_relative_level_enable",
                  "tabFSV.spectrum_analyzer_IF_relative_level",
                  "tabFSV.threshold_power",
                  "tabFSV.spectrum_analyzer_frequency_marker_unit",
                  "tabFSV.FSV_delay",
                  "tabFSV.spectrum_analyzer_central_frequency",
                  "tabFSV.spectrum_analyzer_central_frequency_unit",
                  "tabCalCableSetting.result_file_name",
                  "tabCalCableSetting.output_level",
                  "tabCalCableSetting.create_dummycable_cb"]

        TaskFrame.framesavesettings(self, filename, params=params)

    def OnStart(self, event):

        TaskFrame.OnStart(self, event)

        create_dummy_cable = self.notebook.tabCalCableSetting.create_dummycable_cb.GetValue()

        if create_dummy_cable:
            info_message("Dummy cable creation mode. \n No instrument used.", "Dummy Cable Mode")

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

        syntetizer_enable_state = self.notebook.tabRF.instrument_enable_status.GetValue()

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
            synthetizer_level_fixed = eval(self.notebook.tabRF.synthetizer_level_fixed.GetValue())
        except:
            synthetizer_level_fixed = 0

        spectrum_analyzer_IP = self.notebook.tabFSV.instrument_txt_IP.GetValue()
        if check_value_is_IP(spectrum_analyzer_IP, "LO Synthetizer IP") == 0:
            return None

        spectrum_analyzer_Port = self.notebook.tabFSV.instrument_txt_Port.GetValue()
        if check_value_min_max(spectrum_analyzer_Port, "LO Synthetizer Port", minimum=0) == 0:
            return None

        spectrum_analyzer_Timeout = self.notebook.tabFSV.instrument_txt_Timeout.GetValue()
        if check_value_min_max(spectrum_analyzer_Timeout, "LO Synthetizer Timeout", minimum=0) == 0:
            return None

        spectrum_analyzer_instrType = self.notebook.tabFSV.combobox_instrtype.GetValue()

        spectrum_analyzer_state = self.notebook.tabFSV.instrument_enable_status.GetValue()

        if spectrum_analyzer_state:
            spectrum_analyzer_sweep_points = self.notebook.tabFSV.spectrum_analyzer_sweep_points.GetValue()
            if check_value_min_max(spectrum_analyzer_sweep_points, "Sweep points", minimum=0) == 0:
                return None
            else:
                spectrum_analyzer_sweep_points = eval(self.notebook.tabFSV.spectrum_analyzer_sweep_points.GetValue())

            spectrum_analyzer_resolution_bandwidth = self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth.GetValue()
            if check_value_min_max(spectrum_analyzer_resolution_bandwidth, "Resolution Bandwidth", minimum=0) == 0:
                return None
            else:
                spectrum_analyzer_resolution_bandwidth = eval(
                    self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth.GetValue())

            spectrum_analyzer_resolution_bandwidth_unit = unit.return_unit(
                self.notebook.tabFSV.spectrum_analyzer_resolution_bandwidth_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_resolution_bandwidth_unit, "Resolution Bandwidth Unit") == 0:
                return None

            spectrum_analyzer_video_bandwidth = self.notebook.tabFSV.spectrum_analyzer_video_bandwidth.GetValue()
            if check_value_min_max(spectrum_analyzer_video_bandwidth, "Video Bandwidth", minimum=0) == 0:
                return None
            else:
                spectrum_analyzer_video_bandwidth = eval(
                    self.notebook.tabFSV.spectrum_analyzer_video_bandwidth.GetValue())

            spectrum_analyzer_video_bandwidth_unit = unit.return_unit(
                self.notebook.tabFSV.spectrum_analyzer_video_bandwidth_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_video_bandwidth_unit, "Video Bandwidth Unit") == 0:
                return None

            spectrum_analyzer_frequency_span = self.notebook.tabFSV.spectrum_analyzer_frequency_span.GetValue()
            if check_value_min_max(spectrum_analyzer_frequency_span, "Frequency Span", minimum=0) == 0:
                return None
            else:
                spectrum_analyzer_frequency_span = eval(
                    self.notebook.tabFSV.spectrum_analyzer_frequency_span.GetValue())

            spectrum_analyzer_frequency_span_unit = unit.return_unit(
                self.notebook.tabFSV.spectrum_analyzer_frequency_span_unit.GetValue())
            if check_value_not_none(spectrum_analyzer_frequency_span_unit, "Frequency Span Unit") == 0:
                return None

            ##spectrum_analyzer_harmonic_number = spectrum_analyzer_harmonic_number
            # spectrum_analyzer_attenuation = self.notebook.tabFSV.spectrum_analyzer_attenuation.GetValue()
            # if check_value_not_none(spectrum_analyzer_attenuation, "Attenuation") == 0:
            #    return None

            gainAmplifier = self.notebook.tabFSV.gainAmplifier.GetValue()  # dB
            if check_value_not_none(gainAmplifier, "Gain Amplifier") == 0:
                return None

            spectrum_analyzer_IF_atten_enable = self.notebook.tabFSV.spectrum_analyzer_IF_atten_enable.GetValue()
            spectrum_analyzer_IF_atten = self.notebook.tabFSV.spectrum_analyzer_IF_atten.GetValue()
            if check_value_not_none(spectrum_analyzer_IF_atten, "Attenuation") == 0:
                return None

            spectrum_analyzer_IF_relative_level = self.notebook.tabFSV.spectrum_analyzer_IF_relative_level.GetValue()
            if check_value_not_none(spectrum_analyzer_IF_relative_level, "Relative Power Level") == 0:
                return None

            spectrum_analyzer_IF_relative_level_enable = self.notebook.tabFSV.spectrum_analyzer_IF_relative_level_enable.GetValue()

            threshold_power = self.notebook.tabFSV.threshold_power.GetValue()  # dB
            if check_value_not_none(threshold_power, "Threshold Power Level") == 0:
                return None

            spectrum_analyzer_frequency_marker_unit = unit.return_unit(
                self.notebook.tabFSV.spectrum_analyzer_frequency_marker_unit.GetValue())
            # to check
            if check_value_not_none(spectrum_analyzer_frequency_marker_unit, "Marker Frequency Unit") == 0:
                return None

            FSV_delay = self.notebook.tabFSV.FSV_delay.GetValue()
            if check_value_min_max(FSV_delay, "FSV measure delay", minimum=0) == 0:
                return None
            else:
                FSV_delay = eval(self.notebook.tabFSV.FSV_delay.GetValue())

        result_file_name = self.notebook.tabCalCableSetting.result_file_name.GetValue()
        dummy_cable_power_level = self.notebook.tabCalCableSetting.output_level.GetValue()

        if create_dummy_cable:
            if check_value_not_none(dummy_cable_power_level, "Power Level (Dummy Cable)") == 0:
                return None

        try:
            SMB_RF = create_instrument(synthetizer_IP, synthetizer_Port, eval(synthetizer_Timeout),
                                       syntetizer_instrType, TEST_MODE=self.runmodeitem.IsChecked(),
                                       enable_state=syntetizer_enable_state and not create_dummy_cable)
        except:
            dlg = wx.MessageDialog(None, "Synthetizer comunication error", 'Error Synthetizer', wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0

        try:
            FSV = create_instrument(spectrum_analyzer_IP, spectrum_analyzer_Port, eval(spectrum_analyzer_Timeout),
                                    spectrum_analyzer_instrType, TEST_MODE=self.runmodeitem.IsChecked(),
                                    instrument_class="FSV", enable_state=spectrum_analyzer_state)
        except:
            dlg = wx.MessageDialog(None, "Spectrum analiser comunication error", 'Error Spectrum analiser',
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            return 0

        self.savesettings(result_file_name)

        dialog = wx.ProgressDialog("Progress", "Time remaining", maximum=100,
                                   style=wx.PD_CAN_ABORT | wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME)

        synthetizer_frequency = Frequency_Range(synthetizer_frequency_min, synthetizer_frequency_max,
                                                synthetizer_frequency_step, synthetizer_frequency_unit)
        synthetizer_frequency.to_base()

        calibration_file_result = measure_calibration_cable(SMB_RF,
                                                            FSV,
                                                            synthetizer_frequency,
                                                            synthetizer_level_fixed,
                                                            spectrum_analyzer_state,
                                                            spectrum_analyzer_sweep_points,
                                                            spectrum_analyzer_resolution_bandwidth,
                                                            spectrum_analyzer_resolution_bandwidth_unit,
                                                            spectrum_analyzer_video_bandwidth,
                                                            spectrum_analyzer_video_bandwidth_unit,
                                                            spectrum_analyzer_frequency_span,
                                                            spectrum_analyzer_frequency_span_unit,
                                                            # spectrum_analyzer_attenuation,
                                                            gainAmplifier,
                                                            spectrum_analyzer_IF_atten_enable,
                                                            spectrum_analyzer_IF_atten,
                                                            spectrum_analyzer_IF_relative_level,
                                                            spectrum_analyzer_IF_relative_level_enable,
                                                            threshold_power,
                                                            spectrum_analyzer_frequency_marker_unit,
                                                            FSV_delay,
                                                            result_file_name,
                                                            dummy_cable_power_level,
                                                            create_dummy_cable,
                                                            createprogressdialog=dialog)

        dialog.Destroy()

        try:
            webbrowser.open(os.path.dirname(calibration_file_result))
        except:
            pass


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = CalCableFrame()
    app.MainLoop()
