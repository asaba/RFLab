'''
Created on 26/dic/2015

@author: sabah
'''

#import images
import wx
import os

from guitabs import TabPanelGenericPlotGraph, TabPanelIP1PlotGraph, TabPanelSpuriusCPlotGraph
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK
from utility import writelineonfilesettings, return_now_postfix,\
    Generic_Range
from measure_scripts.scriptutility import Frequency_Range




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
        self.tabSpuriusPlotGraph = TabPanelSpuriusCPlotGraph(self)
        self.AddPage(self.tabSpuriusPlotGraph, "Graph Spurius plot")
        
        self.tabGenericPlotGraph = TabPanelGenericPlotGraph(self)
        self.AddPage(self.tabGenericPlotGraph, "Graph Generic plot")
        
        self.tabIP1PlotGraph = TabPanelIP1PlotGraph(self)
        self.AddPage(self.tabIP1PlotGraph, "Graph IP1 plot")
 
########################################################################
class PlotsFrame(wx.Frame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "Plots",
                          size=(800,650)
                          )
        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        self.fitem = fileMenu.Append(wx.ID_OPEN, 'Load settings', 'Load settings')
        self.fitem2 = fileMenu.Append(wx.ID_SAVEAS, 'Save settings', 'Save settings')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnLoadSettings, self.fitem)
        self.Bind(wx.EVT_MENU, self.OnSaveSettings, self.fitem2)
        #self.Bind(wx.EVT_MENU, self.OnCheckRunMode, self.runmodeitem)
        
        self.panel = wx.Panel(self)
        
        self.notebook = NotebookDemo(self.panel)
        #notebook2 = NotebookDemo(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.ALL|wx.EXPAND, 5)
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
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_title")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_label")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_min")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_max")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_step")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_label")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_min")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_max")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_step")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_label_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_min_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_max_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_x_step_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_label_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_min_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_max_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_y_step_auto")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.graph_animated")
        self.writelinesettings(filepointer, "self.notebook.tabIP1PlotGraph.data_file_name") 
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_label")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_min")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_max")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_step")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_unit")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_label")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_min")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_max")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_step")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_unit")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_label_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_min_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_max_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_x_step_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_label_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_min_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_max_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_y_step_auto")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.data_file_name")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_title")
        self.writelinesettings(filepointer, "self.notebook.tabSpuriusPlotGraph.graph_type")      
    
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
    
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = PlotsFrame()
    app.MainLoop()