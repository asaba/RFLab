'''
Created on 26/dic/2015

@author: sabah
'''

#import images
if "flib" in globals():
    from flib import wx
else:
    import wx

from Spuriusgui import SpuriusFrame
from CalCablegui import CalCableFrame
from CalDummyCablegui import CalDummyCableFrame
from ContinousMeasuregui import CalContinousMeasureFrame
from IP1Calcgui import IP1CalcFrame
from PlotAllanDevgui import PlotAllanDevFrame


class MainFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Frame.__init__(self, parent, wx.ID_ANY,
                          "Microware Lab Measure",
                          size=(350,300)
                          )
        self.panel = wx.Panel(self)
        #check if calibration cable module is present
        self.btn_cal_cable = wx.Button(self.panel, 0, 'Calibrate Cable')
        self.btn_cal_cable.Bind(wx.EVT_BUTTON, self.OnCalCable)
        
        self.btn_cal_dummy_cable = wx.Button(self.panel, 0, 'Create Dummy Cable Calibration')
        self.btn_cal_dummy_cable.Bind(wx.EVT_BUTTON, self.OnCalDummyCable)
        
        #check if spurius calculation is present
        self.btn_calc_spurius = wx.Button(self.panel, 0, 'Calculate Spurius')
        self.btn_calc_spurius.Bind(wx.EVT_BUTTON, self.OnCalcSpurius)
        
        self.btn_calc_IP1 = wx.Button(self.panel, 0, 'Calculate IP1')
        self.btn_calc_IP1.Bind(wx.EVT_BUTTON, self.OnCalcIP1)
        
        self.btn_continous_measure = wx.Button(self.panel, 0, 'Countinous Measure')
        self.btn_continous_measure.Bind(wx.EVT_BUTTON, self.OnCalcContinousMeasure)
        
        self.btn_calc_adev = wx.Button(self.panel, 0, 'Calculate Allan Deviation')
        self.btn_calc_adev.Bind(wx.EVT_BUTTON, self.OnCalcAdev)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.btn_cal_cable, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_cal_dummy_cable, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_calc_spurius, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_calc_IP1, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_continous_measure, 0, wx.ALL|wx.EXPAND, 5)
        sizer.Add(self.btn_calc_adev, 0, wx.ALL|wx.EXPAND, 5)
        self.panel.SetSizer(sizer)
        self.Layout()
 
        self.Show()
    
    
    def OnCalcContinousMeasure(self, event):
        calcontinousmeasureapp = wx.App()
        frame = CalContinousMeasureFrame()
        calcontinousmeasureapp.MainLoop()
    
    def OnCalCable(self, event):
        calcableapp = wx.App()
        frame = CalCableFrame()
        calcableapp.MainLoop()
        #Check all values

    def OnCalDummyCable(self, event):
        caldummycableapp = wx.App()
        frame = CalDummyCableFrame()
        caldummycableapp.MainLoop()
        #Check all values
    
    def OnCalcSpurius(self, event):
        calcspuriusapp = wx.App()
        frame = SpuriusFrame()
        calcspuriusapp.MainLoop()
        
    def OnCalcIP1(self, event):
        calcIP1app = wx.App()
        frame = IP1CalcFrame()
        calcIP1app.MainLoop()
        
    def OnCalcAdev(self, event):
        calcAdevapp = wx.App()
        frame = PlotAllanDevFrame()
        calcAdevapp.MainLoop()
 
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = MainFrame(None)
    app.MainLoop()