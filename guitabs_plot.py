'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os

from guiobjects import return_checkbox_labeled, return_spinctrl, return_textbox_labeled, return_comboBox_unit, \
    return_file_browse, return_simple_button, return_test_instrument, return_simple_button, return_min_max_step_labeled, \
    return_spinctrl_min_max, return_comboBox, return_checkbox_list
from utilitygui import check_value_is_valid_file, check_value_min_max, check_value_not_none, resultError, resultOK, \
    check_value_is_IP, create_instrument, browse_file, check_steps_count, error_message, check_instrument_comunication, \
    check_USB_instrument_comunication
from measure_scripts.plotIP1graph import calculate_all_IP1, unit, openSpuriusfile
from measure_scripts.plotSpuriusCGraph import plot_spurius_graph, order_and_group_data
from measure_scripts.csvutility import *
from measure_scripts.graphutility import Graph_Axis_Range, graph_types, generic_graph_types, opentouchstonefile
from measure_scripts.csvutility import frequency_RF_index
import webbrowser
import subprocess
# from Imagegui import ImageFrame
from utility import inkscape_exec, buildfitsfileslist, return_max_min_from_data_table_row, \
    human_readable_frequency_unit, SplineError, PointNotFound

fig1 = None


class PlotGraphPanelClass(wx.Panel):
    # input Data File
    # Graph Title

    def __init__(self, parent, input_file_wildcard="CSV files (*.csv)|*.csv|Excel file (*.xlsx)|*.xlsx"):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.data_file_name, self.data_file_name_button, dummy, self.sizer_data_file_name = return_file_browse(self,
                                                                                                               "Data File")
        self.wildcard = input_file_wildcard
        self.data_file_name_button.Bind(wx.EVT_BUTTON, self.File_browser_DataFile)

        # Graph Title
        self.graph_title, dummy, dummy, self.sizer_graph_title, dummy, dummy = return_textbox_labeled(self,
                                                                                                      "Graph title")

    def File_browser_DataFile(self, event):
        browse_file(self, self.data_file_name, wildcard=self.wildcard)


class XYPlotGraphPanelClass(PlotGraphPanelClass):
    """
    Tab for Plot XY Graph ex. IP1, Spurius, ...
    """

    def __init__(self, parent, animated=False, z_axes=False,
                 input_file_wildcard="CSV files (*.csv)|*.csv|Excel file (*.xlsx)|*.xlsx"):

        self.x_index = 0
        self.y_index = 0
        self.z_index = 0
        self.row_data_filter = []

        PlotGraphPanelClass.__init__(self, parent=parent, input_file_wildcard=input_file_wildcard)

        self.graph_x_label, dummy, dummy, self.sizer_graph_x_label, dummy, dummy = return_textbox_labeled(self,
                                                                                                          "X Axes Label")
        self.graph_x_min, dummy, self.graph_x_max, dummy, self.graph_x_step, dummy, self.graph_x_unit, self.grap_x_calc_button, self.sizer_graph_x = return_min_max_step_labeled(
            self, "X Axes", unit=False, single_unit=True, button_text="Calculate")

        self.grap_x_calc_button.param_to_calc = {"combobox": "self.graph_x_unit",
                                                 "index": "self.x_index",
                                                 "textbox_min": "self.graph_x_min",
                                                 "textbox_max": "self.graph_x_max",
                                                 "textbox_step": "self.graph_x_step",
                                                 "filter": "self.row_data_filter",
                                                 "unit_index": "self.x_unit_index"}

        self.grap_x_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)

        self.graph_y_label, dummy, dummy, self.sizer_graph_y_label, dummy, dummy = return_textbox_labeled(self,
                                                                                                          "Y Axes label",
                                                                                                          enabled=False,
                                                                                                          enable_text="Auto")
        self.graph_y_min, dummy, self.graph_y_max, dummy, self.graph_y_step, dummy, self.graph_y_unit, self.grap_y_calc_button, self.sizer_graph_y = return_min_max_step_labeled(
            self, "Y Axes", unit=False, single_unit=True, button_text="Calculate")

        self.grap_y_calc_button.param_to_calc = {"combobox": "self.graph_y_unit",
                                                 "index": "self.y_index",
                                                 "textbox_min": "self.graph_y_min",
                                                 "textbox_max": "self.graph_y_max",
                                                 "textbox_step": "self.graph_y_step",
                                                 "filter": "self.row_data_filter",
                                                 "unit_index": "self.y_unit_index"}

        self.grap_y_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)

        self.z_axes = False
        if z_axes:
            self.z_axes = True
            self.graph_z_label, dummy, dummy, self.sizer_graph_z_label, dummy, dummy = return_textbox_labeled(self,
                                                                                                              "Z Axes label",
                                                                                                              enabled=False,
                                                                                                              enable_text="Auto")
            self.graph_z_min, dummy, self.graph_z_max, dummy, self.graph_z_step, dummy, self.graph_z_unit, self.grap_z_calc_button, self.sizer_graph_z = return_min_max_step_labeled(
                self, "Z Axes", unit=False, single_unit=True, button_text="Calculate")

            self.grap_z_calc_button.param_to_calc = {"combobox": "self.graph_z_unit",
                                                     "index": "self.z_index",
                                                     "textbox_min": "self.graph_z_min",
                                                     "textbox_max": "self.graph_z_max",
                                                     "textbox_step": "self.graph_z_step",
                                                     "filter": "self.row_data_filter",
                                                     "unit_index": "self.z_unit_index"}
            self.grap_z_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        if animated:
            self.graph_animated, self.sizer_graph_animated = return_checkbox_labeled(self, "Animate Graph")

    def OnCalcAuto(self, event):

        button = event.GetEventObject()

        param_to_calc = button.param_to_calc  # {"type": "max", "index" : "self.x_index", "textbox" : "self.graph_y_max", "unit_index" : "self.x_unit_index",}

        m = []
        tmp_unit = unit.return_unit_str(unit.dBm)
        for row in self.return_list_of_row():
            for d in row:
                if self.check_filter(d, eval(param_to_calc["filter"])):
                    m.append(d[eval(param_to_calc["index"])])
                    if eval(param_to_calc["unit_index"]) is not None:
                        tmp_unit = unit.return_unit_str(d[eval(param_to_calc["unit_index"])])
        if len(m) > 0:
            mx = max(m)
            mn = min(m)
            step = abs(mx - mn) / 10
            eval(param_to_calc["textbox_max"]).ChangeValue(str(max(m)))
            eval(param_to_calc["textbox_min"]).ChangeValue(str(min(m)))
            eval(param_to_calc["textbox_step"]).ChangeValue(str(step))
            eval(param_to_calc["combobox"]).SetValue(tmp_unit)

    def check_filter(self, row, row_filter):
        result = True
        for f in row_filter:
            index = f[0]
            filter_type = f[1]
            filter_value = f[2]
            if str(filter_type) == "in":
                if row[index] in filter_value:
                    pass
                else:
                    return False
            elif str(filter_type) == "not in":
                if row[index] not in filter_value:
                    pass
                else:
                    return False
        return result

    def return_list_of_row(self):
        if self.check_values() == 0:
            return []

        IF_Frequency_selected = [0]
        SD_LO_Frequency = 0
        SD_LO_Level = 0
        SD_RF_Level = 0
        graph_z_min = 0

        if str(self.graph_type_value) == "LO":
            self.x_index = frequency_IF_index
            self.x_unit_index = unit_IF_index
            self.y_index = conversion_loss
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            self.row_data_filter = [(n_LO_index, "in", [1, -1]), (m_RF_index, "in", [1, -1])]
        elif str(self.graph_type_value) == "RF":
            self.x_index = power_RF_index
            self.x_unit_index = None
            self.y_index = power_IF_index
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            self.row_data_filter = [(n_LO_index, "in", [1, -1]), (m_RF_index, "in", [1, -1])]
        elif str(self.graph_type_value) == "IP1":
            self.x_index = power_RF_index
            self.x_unit_index = None
            self.y_index = power_IF_index
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            self.row_data_filter = [(m_RF_index, "not in", [0])]
        elif str(self.graph_type_value) == "SP":
            self.x_index = power_RF_index
            self.x_unit_index = None
            self.y_index = power_IF_index
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            dlg = wx.TextEntryDialog(self, "Insert Spurius Frequencies (MHz) - comma separated")
            dlg.ShowModal()
            result = dlg.GetValue()
            dlg.Destroy()
            IF_Frequency_selected = eval("[" + result + "]")
            IF_Frequency_selected = [unit.convertion_to_base(x, unit.MHz) for x in IF_Frequency_selected]
            self.row_data_filter = [(n_LO_index, "not in", [1, -1]), (m_RF_index, "not in", [1, -1])]
        elif str(self.graph_type_value) == "SD":
            self.x_index = frequency_IF_index
            self.x_unit_index = unit_IF_index
            self.y_index = power_IF_index
            self.y_unit_index = None
            self.z_index = power_IF_index
            self.z_unit_index = None
            graph_z_min = self.graph_z_min.GetValue()
            if check_value_min_max(graph_z_min, "Graph Z min", minimum=None) == 0:
                error_message("Insert lower value of Z axis", 'Error on Z min')
                return []
            else:
                graph_z_min = eval(self.graph_z_min.GetValue())
            dlg = wx.TextEntryDialog(self, "Insert LO Frequency (MHz)")
            dlg.ShowModal()
            SD_LO_Frequency = dlg.GetValue()
            dlg.Destroy()
            SD_LO_Frequency = unit.convertion_to_base(SD_LO_Frequency, unit.MHz)
            dlg = wx.TextEntryDialog(self, "Insert LO Level (dBm)")
            dlg.ShowModal()
            SD_LO_Level = dlg.GetValue()
            dlg.Destroy()
            SD_LO_Level = eval(SD_LO_Level)
            dlg = wx.TextEntryDialog(self, "Insert RF Level (dBm)")
            dlg.ShowModal()
            SD_RF_Level = dlg.GetValue()
            dlg.Destroy()
            SD_RF_Level = eval(SD_RF_Level)
            self.row_data_filter = [(n_LO_index, "not in", [1, -1]), (m_RF_index, "not in", [1, -1])]

        elif str(self.graph_type_value) == "GG":
            # sort_data = [0, 1]
            # group_level_01 = []
            self.x_index = 1
            self.x_unit_index = None
            self.y_index = 2
            self.y_unit_index = None
            self.row_data_filter = [(0, "not in", [0])]
        elif str(self.graph_type_value) == "NN":
            # sort_data = [0, 1]
            # group_level_01 = []
            self.x_index = 1
            self.x_unit_index = None
            self.y_index = 2
            self.y_unit_index = None
            self.row_data_filter = [(0, "not in", [0])]
            # file_table_result, list_of_s_param = opentouchstonefile(self.data_file_name_value, filter_label=None)
            # dlg = wx.TextEntryDialog(self, "Insert s params - comma separated (ex. S12DB, S11A)", defaultValue=str(list_of_s_param)[1:-1].replace("'", ""))
            # dlg.ShowModal()
            # result = dlg.GetValue()
            # dlg.Destroy()
            # IF_Frequency_selected = [r.strip() for r in result.split(",")]
            IF_Frequency_selected = self.return_checked_ports()

        data_table, dummy, dummy, dummy, dummy, dummy, dummy = order_and_group_data(
            data_file_name=self.data_file_name_value,
            graph_type=self.graph_type_value,
            SD_LO_Frequency=SD_LO_Frequency,
            SD_LO_Level=SD_LO_Level,
            SD_RF_Level=SD_RF_Level,
            SD_IF_Min_Level=graph_z_min,
            IF_Frequency_selected=IF_Frequency_selected,
            savefile=False)
        return data_table

    def check_and_return_Axis_ranges(self):
        graph_x_label = self.graph_x_label.GetValue()
        # graph_x_label_auto = self.graph_x_label_auto.GetValue()
        graph_x_min = self.graph_x_min.GetValue()
        if check_value_min_max(graph_x_min, "Graph X min", minimum=None) == 0:
            return None, None, None
        else:
            graph_x_min = eval(self.graph_x_min.GetValue())
        # graph_x_min_auto = self.graph_x_min_auto.GetValue()

        graph_x_max = self.graph_x_max.GetValue()
        if check_value_min_max(graph_x_max, "Graph X max", minimum=None) == 0:
            return None, None, None
        else:
            graph_x_max = eval(self.graph_x_max.GetValue())
        # graph_x_max_auto = self.graph_x_max_auto.GetValue()
        graph_x_step = self.graph_x_step.GetValue()
        if check_value_min_max(graph_x_step, "Graph X step", minimum=0) == 0:
            return None, None, None
        else:
            graph_x_step = eval(self.graph_x_step.GetValue())
        # graph_x_step_auto = self.graph_x_step_auto.GetValue()
        graph_x_unit = unit.return_unit(self.graph_x_unit.GetValue()) or unit.MHz

        if check_steps_count("X steps", minimum=graph_x_min, maximum=graph_x_max, steps=graph_x_step, counter=50) == 0:
            return None, None, None

        graph_x = Graph_Axis_Range(graph_x_min, graph_x_max, graph_x_step, graph_x_unit, graph_x_label)
        graph_x.to_base()

        graph_y_label = self.graph_y_label.GetValue()
        # graph_x_label_auto = self.graph_x_label_auto.GetValue()
        graph_y_min = self.graph_y_min.GetValue()
        if check_value_min_max(graph_y_min, "Graph Y min", minimum=None) == 0:
            return None, None, None
        else:
            graph_y_min = eval(self.graph_y_min.GetValue())
        # graph_x_min_auto = self.graph_x_min_auto.GetValue()

        graph_y_max = self.graph_y_max.GetValue()
        if check_value_min_max(graph_y_max, "Graph Y max", minimum=None) == 0:
            return None, None, None
        else:
            graph_y_max = eval(self.graph_y_max.GetValue())
        # graph_x_max_auto = self.graph_x_max_auto.GetValue()
        graph_y_step = self.graph_y_step.GetValue()
        if check_value_min_max(graph_y_step, "Graph Y step", minimum=0) == 0:
            return None, None, None
        else:
            graph_y_step = eval(self.graph_y_step.GetValue())
        # graph_x_step_auto = self.graph_x_step_auto.GetValue()
        graph_y_unit = unit.return_unit(self.graph_y_unit.GetValue()) or unit.MHz

        if check_steps_count("Y steps", minimum=graph_y_min, maximum=graph_y_max, steps=graph_y_step, counter=50) == 0:
            return None, None, None

        graph_y = Graph_Axis_Range(graph_y_min, graph_y_max, graph_y_step, graph_y_unit, graph_y_label)
        graph_y.to_base()
        graph_z = None
        if self.z_axes:
            graph_z_label = self.graph_z_label.GetValue()
            # graph_x_label_auto = self.graph_x_label_auto.GetValue()
            graph_z_min = self.graph_z_min.GetValue()
            if check_value_min_max(graph_z_min, "Graph Z min", minimum=None) == 0:
                return None, None, None
            else:
                graph_z_min = eval(self.graph_z_min.GetValue())
            # graph_x_min_auto = self.graph_x_min_auto.GetValue()

            graph_z_max = self.graph_z_max.GetValue()
            if check_value_min_max(graph_z_max, "Graph Z max", minimum=None) == 0:
                return None, None, None
            else:
                graph_z_max = eval(self.graph_z_max.GetValue())
            # graph_x_max_auto = self.graph_x_max_auto.GetValue()
            graph_z_step = self.graph_z_step.GetValue()
            if check_value_min_max(graph_z_step, "Graph Z step", minimum=0) == 0:
                return None, None, None
            else:
                graph_z_step = eval(self.graph_z_step.GetValue())
            # graph_x_step_auto = self.graph_x_step_auto.GetValue()
            graph_z_unit = unit.return_unit(self.graph_z_unit.GetValue()) or unit.MHz

            if check_steps_count("Z steps", minimum=graph_z_min, maximum=graph_z_max, steps=graph_z_step,
                                 counter=50) == 0:
                return None, None, None

            graph_z = Graph_Axis_Range(graph_z_min, graph_z_max, graph_z_step, graph_z_unit, graph_z_label)
            graph_z.to_base()
        return graph_x, graph_y, graph_z


class TabPanelIP1PlotGraph(XYPlotGraphPanelClass):
    """
    Tab for Plot IP1 Graph
    """

    def __init__(self, parent):  # , example_image_path = None):

        XYPlotGraphPanelClass.__init__(self, parent=parent, animated=True)  # , example_image_path = None)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.plot_button, self.sizer_plot_button = return_simple_button(self, "Plot Graph", "Start")
        self.plot_button.Bind(wx.EVT_BUTTON, self.OnPlotGraph)

        self.spurious_freq_checkboxlist, self.spurious_freq_checkboxlist_fill_button, self.sizer_spurious_freq_checkboxlist = return_checkbox_list(
            self,
            label="Spurious Frequencies ({unit})".format(unit=unit.return_unit_str(human_readable_frequency_unit)))
        self.spurious_freq_checkboxlist_fill_button.Bind(wx.EVT_BUTTON, self.FillSpuriousFreqList)
        # input Data File
        # Graph Title

        self.graph_x_label.ChangeValue("Input Power (dBm)")
        self.graph_y_label.ChangeValue("Output Power (dBm)")

        # sizer.Add(self.sizer_image_example, 0, wx.ALL, 5)
        sizer.Add(self.sizer_data_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_spurious_freq_checkboxlist, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_title, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_animated, 0, wx.ALL, 5)
        sizer.Add(self.sizer_plot_button, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def FillSpuriousFreqList(self, event):
        self.data_file_name_value = self.data_file_name.GetValue()

        if check_value_is_valid_file(self.data_file_name_value, "IP1 data file") == 0:
            return 0

        file_table_result, unit_value, data_file_directory = openSpuriusfile(self.data_file_name_value)

        freq = []
        for row in file_table_result:
            freq.append(unit.convertion_from_base(row[frequency_RF_index], human_readable_frequency_unit))

        freq = list(set(freq))

        freq.sort()

        self.spurious_freq_checkboxlist.Clear()

        for f in freq:
            self.spurious_freq_checkboxlist.Append(str(f))

    def return_checked_ports(self):
        return [i for i in self.spurious_freq_checkboxlist.GetCheckedStrings()]

    def check_values(self):
        self.data_file_name_value = self.data_file_name.GetValue()

        if check_value_is_valid_file(self.data_file_name_value, "Data Harmonic file") == 0:
            return 0

        self.graph_type_value = "IP1"
        # if self.graph_type_value in graph_types.keys():
        #    self.graph_type_value = graph_types[self.graph_type_value]
        # else:
        #    error_message("Graph type not selected", "Graph type error")
        #    return 0

    def OnPlotGraph(self, event):
        data_file_name = self.data_file_name.GetValue()
        if check_value_is_valid_file(data_file_name, "Data IP1 file") == 0:
            return None

        graph_title = self.graph_title.GetValue()

        graph_x, graph_y, dummy = self.check_and_return_Axis_ranges()
        if graph_x is None or graph_y is None:
            return None

        graph_animated = self.graph_animated.GetValue()

        # dlg = wx.TextEntryDialog(self, "Insert Spurius Frequencies (MHz) - comma separated")
        # dlg.ShowModal()
        # result = dlg.GetValue()
        # dlg.Destroy()
        # IF_Frequency_selected = eval("[" + result + "]")
        # IF_Frequency_selected = [unit.convertion_to_base(x, unit.MHz) for x in IF_Frequency_selected]
        IF_Frequency_selected = [unit.convertion_to_base(x, human_readable_frequency_unit) for x in
                                 self.return_checked_ports()]
        # IF_Frequency_selected = self.return_checked_ports()



        current_font_style = self.Parent.GrandParent.get_selected_settings()

        try:
            calculate_all_IP1(data_file_name,
                              graph_title,
                              graph_x,
                              graph_y,
                              IF_Frequency_selected,
                              graph_animated,
                              font_style=current_font_style)
            # self.instrument_label.SetLabel(response)
        except SplineError:
            error_message("Impossible to build spline", "Spline Error")
        except PointNotFound:
            error_message("IP1 point not found", "IP1 error")

        try:
            last_svg = ""
            result_folder = os.path.dirname(data_file_name)
            for svg_file in buildfitsfileslist(result_folder):
                last_svg = svg_file
                execute = [inkscape_exec, "-f", svg_file, '-M', svg_file[:-4] + '.emf']
                print("saving " + svg_file[:-4] + '.emf')
                subprocess.call(execute)
        except:
            print("Error saving " + last_svg)


class TabPanelSpuriusCPlotGraph(XYPlotGraphPanelClass):
    """
    Tab for Plot IP1 Graph
    """

    def __init__(self, parent):  # , example_image_path = None):

        XYPlotGraphPanelClass.__init__(self, parent=parent, animated=False, z_axes=True)  # , example_image_path = None)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.graph_type, self.sizer_graph_type = return_comboBox(self, "Graph type", choices_list=graph_types.keys())

        self.plot_button, self.sizer_plot_button = return_simple_button(self, "Plot Graph", "Start")
        self.plot_button.Bind(wx.EVT_BUTTON, self.OnPlotGraph)

        # self.grap_x_max_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        # input Data File
        # Graph Title


        self.graph_x_label.ChangeValue("IF Frequency ({unit})")
        self.graph_y_label.ChangeValue("IF Power Loss ({unit})")

        # sizer.Add(self.sizer_image_example, 0, wx.ALL, 5)
        sizer.Add(self.sizer_data_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_type, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_title, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_z_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_z, 0, wx.ALL, 5)
        # sizer.Add(self.sizer_graph_animated, 0, wx.ALL, 5)
        sizer.Add(self.sizer_plot_button, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def check_values(self):
        self.data_file_name_value = self.data_file_name.GetValue()

        if check_value_is_valid_file(self.data_file_name_value, "Data Spurius file") == 0:
            return 0

        self.graph_type_value = self.graph_type.GetValue()
        if self.graph_type_value in graph_types.keys():
            self.graph_type_value = graph_types[self.graph_type_value]
        else:
            error_message("Graph type not selected", "Graph type error")
            return 0

    def OnPlotGraph(self, event):
        result = [0]
        if self.check_values() == 0:
            return 0
        graph_title = self.graph_title.GetValue()
        graph_x, graph_y, graph_z = self.check_and_return_Axis_ranges()
        if graph_x is None or graph_y is None:
            return None

        if str(self.graph_type_value) == "SD":
            if graph_z is None:
                return None
        else:
            graph_z = Graph_Axis_Range(0, 0, 0, unit.Hz, "")

        IF_Frequency_selected = [0]
        SD_LO_Frequency = 0
        SD_LO_Level = 0
        SD_RF_Level = 0
        if str(self.graph_type_value) == "SP":
            dlg = wx.TextEntryDialog(self, "Insert Spurius Frequencies (MHz) - comma separated")
            dlg.ShowModal()
            result = dlg.GetValue()
            dlg.Destroy()
            IF_Frequency_selected = eval("[" + result + "]")
            IF_Frequency_selected = [unit.convertion_to_base(x, unit.MHz) for x in IF_Frequency_selected]
        elif str(self.graph_type_value) == "SD":
            dlg = wx.TextEntryDialog(self, "Insert LO Frequency (MHz)")
            dlg.ShowModal()
            SD_LO_Frequency = dlg.GetValue()
            dlg.Destroy()
            dlg = wx.TextEntryDialog(self, "Insert LO Level (dBm)")
            dlg.ShowModal()
            SD_LO_Level = dlg.GetValue()
            dlg.Destroy()
            dlg = wx.TextEntryDialog(self, "Insert RF Level (dBm)")
            dlg.ShowModal()
            SD_RF_Level = dlg.GetValue()
            dlg.Destroy()
            SD_LO_Frequency = unit.convertion_to_base(SD_LO_Frequency, unit.MHz)
            SD_LO_Level = eval(SD_LO_Level)
            SD_RF_Level = eval(SD_RF_Level)

        current_font_style = self.Parent.GrandParent.get_selected_settings()

        for frequency_IF_filter in IF_Frequency_selected:
            result_folder = plot_spurius_graph(self.data_file_name_value,
                                               self.graph_type_value,
                                               graph_title,
                                               graph_x,
                                               graph_y,
                                               graph_z,
                                               SD_LO_Frequency=SD_LO_Frequency,
                                               SD_LO_Level=SD_LO_Level,
                                               SD_RF_Level=SD_RF_Level,
                                               IF_Frequency_selected=frequency_IF_filter,
                                               font_style=current_font_style)

        try:
            last_svg = ""
            for svg_file in buildfitsfileslist(result_folder):
                last_svg = svg_file
                execute = [inkscape_exec, "-f", svg_file, '-M', svg_file[:-4] + '.emf']
                print("saving " + svg_file[:-4] + '.emf')
                subprocess.call(execute)
        except:
            print("Error saving " + last_svg)
        try:
            if str(self.graph_type_value) != "SD":
                webbrowser.open(result_folder)
        except:
            pass
            # self.instrument_label.SetLabel(response)

            # webbrowser.open('/home/test/test_folder')


class TabPanelGenericPlotGraph(XYPlotGraphPanelClass):
    """
    Tab for Plot IP1 Graph
    """

    def __init__(self, parent):  # , example_image_path = None):

        XYPlotGraphPanelClass.__init__(self, parent=parent, animated=False, z_axes=False,
                                       input_file_wildcard="*.txt; *.s?p")  # , example_image_path = None)
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.graph_type, self.sizer_graph_type = return_comboBox(self, "Graph type",
                                                                 choices_list=generic_graph_types.keys())

        self.plot_button, self.sizer_plot_button = return_simple_button(self, "Plot Graph", "Start")
        self.plot_button.Bind(wx.EVT_BUTTON, self.OnPlotGraph)

        self.ports_checkboxlist, self.ports_checkboxlist_fill_button, self.sizer_ports_checkboxlist = return_checkbox_list(
            self, label="Ports to plot")
        self.ports_checkboxlist_fill_button.Bind(wx.EVT_BUTTON, self.FillPortsList)

        # self.graph_image_example_button, self.sizer_image_example = return_simple_button(self, "Show Example", "Show")
        # self.graph_image_example_button.Bind(wx.EVT_BUTTON, self.Open_Example_Image)


        self.grap_y_calc_button.param_to_calc = {"combobox": "self.graph_y_unit",
                                                 "index": "self.y_index",
                                                 "textbox_min": "self.graph_y_min",
                                                 "textbox_max": "self.graph_y_max",
                                                 "textbox_step": "self.graph_y_step",
                                                 "filter": "self.row_data_filter",
                                                 "unit_index": "self.y_unit_index"}
        self.grap_x_calc_button.param_to_calc = {"combobox": "self.graph_x_unit",
                                                 "index": "self.x_index",
                                                 "textbox_min": "self.graph_x_min",
                                                 "textbox_max": "self.graph_x_max",
                                                 "textbox_step": "self.graph_x_step",
                                                 "filter": "self.row_data_filter",
                                                 "unit_index": "self.x_unit_index"}
        # self.grap_z_calc_button.param_to_calc = {"combobox": "self.graph_z_unit", "index" : "self.z_index", "textbox_min" : "self.graph_z_min", "textbox_max" : "self.graph_z_max", "filter" : "self.row_data_filter", "unit_index" : "self.z_unit_index"}
        # self.grap_x_max_calc_button.param_to_calc = {"combobox": "self.graph_x_unit", "type": "max", "index" : "self.x_index", "textbox" : "self.graph_x_max", "filter" : "self.row_data_filter", "unit_index" : "self.x_unit_index"}


        self.grap_y_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        self.grap_x_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        # self.grap_z_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        # self.grap_x_max_calc_button.Bind(wx.EVT_BUTTON, self.OnCalcAuto)
        # input Data File
        # Graph Title


        self.graph_x_label.ChangeValue("IF Frequency ({unit})")
        self.graph_y_label.ChangeValue("IF Power Loss (dBm)")

        # sizer.Add(self.sizer_image_example, 0, wx.ALL, 5)
        sizer.Add(self.sizer_data_file_name, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_type, 0, wx.ALL, 5)
        sizer.Add(self.sizer_ports_checkboxlist, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_title, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_x, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y_label, 0, wx.ALL, 5)
        sizer.Add(self.sizer_graph_y, 0, wx.ALL, 5)
        # sizer.Add(self.sizer_graph_z_label, 0, wx.ALL, 5)
        # sizer.Add(self.sizer_graph_z, 0, wx.ALL, 5)
        # sizer.Add(self.sizer_graph_animated, 0, wx.ALL, 5)
        sizer.Add(self.sizer_plot_button, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def FillPortsList(self, event):
        self.data_file_name_value = self.data_file_name.GetValue()

        if check_value_is_valid_file(self.data_file_name_value, "Generic graph data file") == 0:
            return 0

        self.graph_type_value = self.graph_type.GetValue()
        if self.graph_type_value in generic_graph_types.keys():
            self.graph_type_value = generic_graph_types[self.graph_type_value]
        else:
            error_message("Graph type not selected", "Graph type error")
            return 0

        if str(self.graph_type_value) != "NN":
            error_message("Graph type invalid", "Graph type error")
            return 0

        file_table_result, list_of_s_param = opentouchstonefile(self.data_file_name_value, filter_label=None)

        self.ports_checkboxlist.Clear()

        for port in list_of_s_param:
            self.ports_checkboxlist.Append(port)

    def return_checked_ports(self):
        return [i for i in self.ports_checkboxlist.GetCheckedStrings()]

    def check_values(self):
        self.data_file_name_value = self.data_file_name.GetValue()

        if check_value_is_valid_file(self.data_file_name_value, "Generic graph data file") == 0:
            return 0

        self.graph_type_value = self.graph_type.GetValue()
        if self.graph_type_value in generic_graph_types.keys():
            self.graph_type_value = generic_graph_types[self.graph_type_value]
        else:
            error_message("Graph type not selected", "Graph type error")
            return 0

    def OnPlotGraph(self, event):
        result = [0]
        if self.check_values() == 0:
            return 0
        graph_title = self.graph_title.GetValue()

        graph_x, graph_y, dummy = self.check_and_return_Axis_ranges()
        if graph_x is None or graph_y is None:
            return None

        graph_z = Graph_Axis_Range(0, 0, 0, unit.MHz, "")

        IF_Frequency_selected = []
        SD_LO_Frequency = 0
        SD_LO_Level = 0
        SD_RF_Level = 0

        if str(self.graph_type_value) == "NN":
            # file_table_result, list_of_s_param = opentouchstonefile(self.data_file_name_value, filter_label=None)
            # dlg = wx.TextEntryDialog(self, "Insert s params - comma separated (ex. S12DB, S11A)", defaultValue=str(list_of_s_param)[1:-1].replace("'", ""))
            # dlg.ShowModal()
            # result = dlg.GetValue()
            # dlg.Destroy()
            # result = self.return_checked_ports()
            # IF_Frequency_selected = [r.strip() for r in result.split(",")]
            IF_Frequency_selected = self.return_checked_ports()
        elif str(self.graph_type_value) == "GG":
            IF_Frequency_selected = [0]

        current_font_style = self.Parent.GrandParent.get_selected_settings()

        result_folder = plot_spurius_graph(self.data_file_name_value,
                                           self.graph_type_value,
                                           graph_title,
                                           graph_x,
                                           graph_y,
                                           graph_z,
                                           SD_LO_Frequency=SD_LO_Frequency,
                                           SD_LO_Level=SD_LO_Level,
                                           SD_RF_Level=SD_RF_Level,
                                           IF_Frequency_selected=IF_Frequency_selected,
                                           font_style=current_font_style)

        try:
            last_svg = ""
            for svg_file in buildfitsfileslist(result_folder):
                last_svg = svg_file
                execute = [inkscape_exec, "-f", svg_file, '-M', svg_file[:-4] + '.emf']
                print("saving " + svg_file[:-4] + '.emf')
                subprocess.call(execute)
        except:
            print("Error saving " + last_svg)
        try:
            if str(self.graph_type_value) != "SD":
                webbrowser.open(result_folder)
        except:
            pass
