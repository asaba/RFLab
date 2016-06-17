'''
Created on 26/dic/2015

@author: sabah
'''

#import images
from taskframe import TaskFrame
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
class PlotsFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """
 
    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                          "Plots",
                          size=(800,650),
                          start_button = False
                          )
                        
    def savesettings(self, filename):
        params = ["tabIP1PlotGraph.graph_title",
        "tabIP1PlotGraph.graph_x_label",
        "tabIP1PlotGraph.graph_x_min",
        "tabIP1PlotGraph.graph_x_max",
        "tabIP1PlotGraph.graph_x_step",
        "tabIP1PlotGraph.graph_y_label",
        "tabIP1PlotGraph.graph_y_min",
        "tabIP1PlotGraph.graph_y_max",
        "tabIP1PlotGraph.graph_y_step",
        "tabIP1PlotGraph.graph_animated",
        "tabIP1PlotGraph.data_file_name", 
        "tabSpuriusPlotGraph.graph_x_label",
        "tabSpuriusPlotGraph.graph_x_min",
        "tabSpuriusPlotGraph.graph_x_max",
        "tabSpuriusPlotGraph.graph_x_step",
        "tabSpuriusPlotGraph.graph_x_unit",
        "tabSpuriusPlotGraph.graph_y_label",
        "tabSpuriusPlotGraph.graph_y_min",
        "tabSpuriusPlotGraph.graph_y_max",
        "tabSpuriusPlotGraph.graph_y_step",
        "tabSpuriusPlotGraph.graph_y_unit",
        "tabSpuriusPlotGraph.data_file_name",
        "tabSpuriusPlotGraph.graph_title",
        "tabSpuriusPlotGraph.graph_type"]
        
        TaskFrame.framesavesettings(self, filename, params = params)      
    
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = PlotsFrame()
    app.MainLoop()