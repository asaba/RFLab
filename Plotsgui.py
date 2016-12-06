'''
Created on 26/dic/2015

@author: sabah
'''

# import images
from taskframe import TaskFrame
import wx
import os

from guitabs_plot import TabPanelGenericPlotGraph, TabPanelIP1PlotGraph, TabPanelSpuriusCPlotGraph
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK
from utility import writelineonfilesettings, return_now_postfix, \
    Generic_Range
from measure_scripts.scriptutility import Frequency_Range
from measure_scripts.graphutility import font_styles, fontsizerange


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
        self.tabSpuriusPlotGraph = TabPanelSpuriusCPlotGraph(
            self)  # , example_image_path = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\RFLab\\exampleimages\\vlcsnap-2016-03-10-11h09m18s460.png")
        self.AddPage(self.tabSpuriusPlotGraph, "Graph Spurius plot")

        self.tabGenericPlotGraph = TabPanelGenericPlotGraph(
            self)  # , example_image_path = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\RFLab\\exampleimages\\vlcsnap-2016-03-10-11h09m18s460.png")
        self.AddPage(self.tabGenericPlotGraph, "Graph Generic plot")

        self.tabIP1PlotGraph = TabPanelIP1PlotGraph(
            self)  # , example_image_path = "C:\\Users\\sabah\\Documents\\Aptana Studio 3 Workspace\\RFLab\\exampleimages\\vlcsnap-2016-03-10-11h09m18s460.png")
        self.AddPage(self.tabIP1PlotGraph, "Graph IP1 plot")


########################################################################
class PlotsFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                           "Plots",
                           size=(800, 680),
                           start_button=False
                           )

        self.setupMenu = wx.Menu()
        self.superior_title = wx.Menu()
        self.title = wx.Menu()
        self.legend_title = wx.Menu()
        self.legend_lines = wx.Menu()
        self.axis_legend = wx.Menu()
        self.axis_ticks = wx.Menu()
        self.annotation = wx.Menu()

        self.superior_title_font = wx.Menu()
        self.superior_title_font_size = wx.Menu()
        self.superior_title_font_size_mi = []
        for i in fontsizerange:
            self.superior_title_font_size_mi.append(
                self.superior_title_font_size.AppendRadioItem(8800 + i, str(i), str(i)))
            # self.Bind(wx.EVT_MENU, self.OnCheckSetting, self.superior_title_font_size_mi[-1])
        self.superior_title_font.AppendMenu(8700, "Size", self.superior_title_font_size)
        self.superior_title.AppendMenu(8600, "Font", self.superior_title_font)
        self.setupMenu.AppendMenu(8500, 'Superior Title', self.superior_title)

        self.title_font = wx.Menu()
        self.title_font_size = wx.Menu()
        self.title_font_size_mi = []
        for i in fontsizerange:
            self.title_font_size_mi.append(self.title_font_size.AppendRadioItem(8400 + i, str(i), str(i)))
            # self.Bind(wx.EVT_MENU, self.OnCheckSetting, self.title_font_size_mi[-1])
        self.title_font.AppendMenu(8300, "Size", self.title_font_size)
        self.title.AppendMenu(8200, "Font", self.title_font)
        self.setupMenu.AppendMenu(8100, 'Title', self.title)

        self.legend_title_font = wx.Menu()
        self.legend_title_font_size = wx.Menu()
        self.legend_title_font_size_mi = []
        for i in fontsizerange:
            self.legend_title_font_size_mi.append(self.legend_title_font_size.AppendRadioItem(8000 + i, str(i), str(i)))
            # self.Bind(wx.EVT_MENU, self.OnCheckSetting, self.legend_title_font_size_mi[-1])
        self.legend_title_font.AppendMenu(7900, "Size", self.legend_title_font_size)
        self.legend_title.AppendMenu(7800, "Font", self.legend_title_font)
        self.setupMenu.AppendMenu(7700, 'Legend Title', self.legend_title)

        self.legend_lines_font = wx.Menu()
        self.legend_lines_font_size = wx.Menu()
        self.legend_lines_font_size_mi = []
        for i in fontsizerange:
            self.legend_lines_font_size_mi.append(self.legend_lines_font_size.AppendRadioItem(7600 + i, str(i), str(i)))
            # self.Bind(wx.EVT_MENU, self.OnCheckSetting, self.legend_lines_font_size_mi[-1])
        self.legend_lines_font.AppendMenu(7500, "Size", self.legend_lines_font_size)
        self.legend_lines.AppendMenu(7400, "Font", self.legend_lines_font)
        self.setupMenu.AppendMenu(7300, 'Legend Lines', self.legend_lines)

        self.axis_legend_font = wx.Menu()
        self.axis_legend_font_size = wx.Menu()
        self.axis_legend_font_size_mi = []
        for i in fontsizerange:
            self.axis_legend_font_size_mi.append(self.axis_legend_font_size.AppendRadioItem(7200 + i, str(i), str(i)))
            # self.Bind(wx.EVT_MENU, self.OnCheckSetting, self.axis_legend_font_size_mi[-1])
        self.axis_legend_font.AppendMenu(7100, "Size", self.axis_legend_font_size)
        self.axis_legend.AppendMenu(7000, "Font", self.axis_legend_font)
        self.setupMenu.AppendMenu(6900, 'Axis Legend', self.axis_legend)

        self.axis_ticks_font = wx.Menu()
        self.axis_ticks_font_size = wx.Menu()
        self.axis_ticks_font_size_mi = []
        for i in fontsizerange:
            self.axis_ticks_font_size_mi.append(self.axis_ticks_font_size.AppendRadioItem(6800 + i, str(i), str(i)))
            # self.Bind(wx.EVT_MENU, self.OnCheckSetting, self.axis_ticks_font_size_mi[-1])
        self.axis_ticks_font.AppendMenu(6700, "Size", self.axis_ticks_font_size)
        self.axis_ticks.AppendMenu(6600, "Font", self.axis_ticks_font)
        self.setupMenu.AppendMenu(6500, 'Axis Ticks', self.axis_ticks)

        self.annotation_font = wx.Menu()
        self.annotation_font_size = wx.Menu()
        self.annotation_font_size_mi = []
        for i in range(5, 20):
            self.annotation_font_size_mi.append(self.annotation_font_size.AppendRadioItem(6400 + i, str(i), str(i)))
            # self.Bind(wx.EVT_MENU, self.OnCheckSetting, self.annotation_font_size_mi[-1])
        self.annotation_font.AppendMenu(6300, "Size", self.annotation_font_size)
        self.annotation.AppendMenu(6200, "Font", self.annotation_font)
        self.setupMenu.AppendMenu(6100, 'Points Text', self.annotation)

        self.menubar.Append(self.setupMenu, '&Settings')
        self.SetMenuBar(self.menubar)

        self.set_selected_settings()
        # self.Bind(wx.EVT_MENU, self.OnLoadSettings, self.fitem)
        # self.Bind(wx.EVT_MENU, self.OnSaveSettings, self.fitem2)

    def _select_setting(self, param_name, menu_item_list):

        for fontsizestyle in menu_item_list:
            if fontsizestyle.IsChecked():
                font_styles[param_name]["fontsize"] = fontsizestyle.Text
                break

    def get_selected_settings(self):

        self._select_setting("suptitle", self.superior_title_font_size_mi)

        self._select_setting("title", self.title_font_size_mi)

        self._select_setting("legendtitle", self.legend_title_font_size_mi)

        self._select_setting("legendlines", self.legend_lines_font_size_mi)

        self._select_setting("axislegend", self.axis_legend_font_size_mi)

        self._select_setting("axisticks", self.axis_ticks_font_size_mi)

        self._select_setting("annotation", self.annotation_font_size_mi)

        return font_styles

    def _set_setting(self, param_name, menu_item_list, font_styles_tmp=None):
        for fontsizestyle in menu_item_list:
            if fontsizestyle.Text == font_styles_tmp[param_name]["fontsize"]:
                fontsizestyle.Check()
                break

    def set_selected_settings(self, font_styles_tmp=None):
        if font_styles_tmp is None:
            font_styles_tmp = font_styles

        self._set_setting("suptitle", self.superior_title_font_size_mi, font_styles_tmp)

        self._set_setting("title", self.title_font_size_mi, font_styles_tmp)

        self._set_setting("legendtitle", self.legend_title_font_size_mi, font_styles_tmp)

        self._set_setting("legendlines", self.legend_lines_font_size_mi, font_styles_tmp)

        self._set_setting("axislegend", self.axis_legend_font_size_mi, font_styles_tmp)

        self._set_setting("axisticks", self.axis_ticks_font_size_mi, font_styles_tmp)

        self._set_setting("annotation", self.annotation_font_size_mi, font_styles_tmp)

        return font_styles

    def savesettings(self, filename):
        params = ["tabIP1PlotGraph.graph_title",
                  "tabIP1PlotGraph.graph_x_label",
                  "tabIP1PlotGraph.graph_x_min",
                  "tabIP1PlotGraph.graph_x_max",
                  "tabIP1PlotGraph.graph_x_step",
                  "tabIP1PlotGraph.graph_x_unit",
                  "tabIP1PlotGraph.graph_y_label",
                  "tabIP1PlotGraph.graph_y_min",
                  "tabIP1PlotGraph.graph_y_max",
                  "tabIP1PlotGraph.graph_y_step",
                  "tabIP1PlotGraph.graph_y_unit",
                  "tabIP1PlotGraph.graph_animated",
                  "tabIP1PlotGraph.data_file_name",
                  "tabGenericPlotGraph.graph_x_label",
                  "tabGenericPlotGraph.graph_x_min",
                  "tabGenericPlotGraph.graph_x_max",
                  "tabGenericPlotGraph.graph_x_step",
                  "tabGenericPlotGraph.graph_x_unit",
                  "tabGenericPlotGraph.graph_y_label",
                  "tabGenericPlotGraph.graph_y_min",
                  "tabGenericPlotGraph.graph_y_max",
                  "tabGenericPlotGraph.graph_y_step",
                  "tabGenericPlotGraph.graph_y_unit",
                  "tabGenericPlotGraph.data_file_name",
                  "tabGenericPlotGraph.graph_title",
                  "tabGenericPlotGraph.graph_type",
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
                  "tabSpuriusPlotGraph.graph_z_label",
                  "tabSpuriusPlotGraph.graph_z_min",
                  "tabSpuriusPlotGraph.graph_z_max",
                  "tabSpuriusPlotGraph.graph_z_step",
                  "tabSpuriusPlotGraph.graph_z_unit",
                  "tabSpuriusPlotGraph.data_file_name",
                  "tabSpuriusPlotGraph.graph_title",
                  "tabSpuriusPlotGraph.graph_type"]

        TaskFrame.framesavesettings(self, filename, params=params)

        # ----------------------------------------------------------------------


if __name__ == "__main__":
    app = wx.App()
    frame = PlotsFrame()
    app.MainLoop()
