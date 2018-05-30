'''
Created on 26/dic/2015

@author: sabah

Version 3.0
Update: 12/12/2016
'''

# import images
if "flib" in globals():
    from flib import wx
else:
    import wx

from Spuriusgui import SpuriusFrame
from CalCablegui import CalCableFrame
from copy_CalCablegui import CalCableFrame as CalCableFramePM
from ContinousMeasuregui import CalContinousMeasureFrame
from ContinousMeasurePMgui import CalContinousMeasurePMFrame
from PlotAllanDevgui import PlotAllanDevFrame
from PM5gui import CalPM5Frame
from Plotsgui import PlotsFrame
import sys
from utility import VERSION


class MainFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Frame.__init__(self, parent, wx.ID_ANY,
                          "Microware Lab Measure v {version}".format(version=VERSION),
                          size=(380, 360)
                          )
        self.panel = wx.Panel(self)
        # check if calibration cable module is present
        self.btn_cal_cable = wx.Button(self.panel, 0, 'Calibrate Cable')
        self.btn_cal_cable.Bind(wx.EVT_BUTTON, self.OnCalCable)

        self.btn_cal_cable_pm = wx.Button(self.panel, 0, 'Calibrate Cable PM')
        self.btn_cal_cable_pm.Bind(wx.EVT_BUTTON, self.OnCalCablePM)

        # self.btn_cal_dummy_cable = wx.Button(self.panel, 0, 'Create Dummy Cable Calibration')
        # self.btn_cal_dummy_cable.Bind(wx.EVT_BUTTON, self.OnCalDummyCable)

        # check if spurius calculation is present
        self.btn_calc_spurius = wx.Button(self.panel, 0, 'Calculate Spurius')
        self.btn_calc_spurius.Bind(wx.EVT_BUTTON, self.OnCalcSpurius)

        # self.btn_calc_IP1 = wx.Button(self.panel, 0, 'Calculate IP1')
        # self.btn_calc_IP1.Bind(wx.EVT_BUTTON, self.OnCalcIP1)

        self.btn_continous_measure = wx.Button(self.panel, 0, 'Countinous Measure')
        self.btn_continous_measure.Bind(wx.EVT_BUTTON, self.OnCalcContinousMeasure)

        self.btn_continous_measure = wx.Button(self.panel, 0, 'Countinous Measure PM')
        self.btn_continous_measure.Bind(wx.EVT_BUTTON, self.OnCalcContinousMeasurePM)

        self.btn_calc_adev = wx.Button(self.panel, 0, 'Calculate Allan Deviation')
        self.btn_calc_adev.Bind(wx.EVT_BUTTON, self.OnCalcAdev)

        self.btn_calc_pm5 = wx.Button(self.panel, 0, 'mm-submm power meter Measure')
        self.btn_calc_pm5.Bind(wx.EVT_BUTTON, self.OnCalcPM5)

        self.btn_plots = wx.Button(self.panel, 0, 'Graphs')
        self.btn_plots.Bind(wx.EVT_BUTTON, self.OnPlots)

        self.btn_exit = wx.Button(self.panel, 0, 'Exit')
        self.btn_exit.Bind(wx.EVT_BUTTON, self.OnExit)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.btn_cal_cable, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.btn_cal_cable_pm, 0, wx.ALL | wx.EXPAND, 5)
        # sizer.Add(self.btn_cal_dummy_cable, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_calc_spurius, 0, wx.ALL | wx.EXPAND, 5)
        # sizer.Add(self.btn_calc_IP1, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_continous_measure, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.btn_calc_adev, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.btn_calc_pm5, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.btn_plots, 0, wx.ALL | wx.EXPAND, 5)
        sizer.Add(self.btn_exit, 0, wx.ALL | wx.EXPAND, 5)
        self.panel.SetSizer(sizer)
        self.Layout()

        self.Show()

    def OnCalcContinousMeasure(self, event):
        calcontinousmeasureapp = wx.App()
        frame = CalContinousMeasureFrame()
        calcontinousmeasureapp.MainLoop()

    def OnCalcContinousMeasurePM(self, event):
        calcontinousmeasurepmapp = wx.App()
        frame = CalContinousMeasurePMFrame()
        calcontinousmeasurepmapp.MainLoop()

    def OnCalCable(self, event):
        calcableapp = wx.App()
        frame = CalCableFrame()
        calcableapp.MainLoop()
        # Check all values

    def OnCalCablePM(self, event):
        calcableapppm = wx.App()
        frame = CalCableFramePM()
        calcableapppm.MainLoop()
        # Check all values

    def OnCalcSpurius(self, event):
        calcspuriusapp = wx.App()
        frame = SpuriusFrame()
        calcspuriusapp.MainLoop()

    def OnCalcAdev(self, event):
        calcAdevapp = wx.App()
        frame = PlotAllanDevFrame()
        calcAdevapp.MainLoop()

    def OnCalcPM5(self, event):
        calcPM5app = wx.App()
        frame = CalPM5Frame()
        calcPM5app.MainLoop()

    def OnPlots(self, event):
        plotsapp = wx.App()
        frame = PlotsFrame()
        plotsapp.MainLoop()

    def OnExit(self, event):
        sys.exit()


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None)
    app.MainLoop()
