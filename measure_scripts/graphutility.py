'''
Created on 28/mag/2016

@author: sabah
'''
from utility import unit_class, return_now_postfix, create_csv
import numpy as np
import csv
import operator
import os
from scriptutility import Frequency_Range
from measure_scripts.csvutility import  frequency_LO_index, unit_LO_index, power_LO_index, is_LO_calibrated_index, frequency_RF_index, unit_RF_index, power_RF_index, is_RF_calibrated_index, frequency_IF_index, unit_IF_index, power_IF_index, is_IF_calibrated_index, n_LO_index, m_RF_index, conversion_loss, csv_file_header


unit = unit_class()

csfont_suptitle = {'fontname':'Times New Roman', "fontsize":"20"}
csfont_title = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_legendtitle = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_legendlines = {'fontname':'Times New Roman', "fontsize":"10"}
csfont_axislegend = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_axisticks = {'fontname':'Times New Roman', "fontsize":"12"}
csfont_annotation = {'fontname':'Times New Roman', "fontsize":"12"}

fontsizerange = range(9, 24)

font_styles = {
                "suptitle" : {'fontname':'Times New Roman', "fontsize":"20"},
                "title" : {'fontname':'Times New Roman', "fontsize":"14"},
                "legendtitle" : {'fontname':'Times New Roman', "fontsize":"14"},
                "legendlines" : {'fontname':'Times New Roman', "fontsize":"10"},
                "axislegend" : {'fontname':'Times New Roman', "fontsize":"14"},
                "axisticks" : {'fontname':'Times New Roman', "fontsize":"12"},
                "annotation" : {'fontname':'Times New Roman', "fontsize":"12"}}


styles = [("o", "b"), ("v", "g"), ("s", "r"), ("s", "c"), ("8", "m"), ("d", "y"), ("*", "k"),
          ("o", "b"), ("o", "g"), ("o", "r"), ("o", "c"), ("o", "m"), ("o", "y"), ("o", "k"),
          ("v", "b"), ("v", "g"), ("v", "r"), ("v", "c"), ("v", "m"), ("v", "y"), ("v", "k"),
          ("s", "b"), ("s", "g"), ("s", "r"), ("s", "c"), ("s", "m"), ("s", "y"), ("s", "k")]

styles_generic_XY = [(None, "b"), (None, "g"), (None, "r"), (None, "c"), (None, "m"), (None, "y"), (None, "k")]

linecolors = ["b", "g", "r", "c", "m", "y", "k"]
markerstyles = [None, "o", "v", "s", ]

generic_graph_types = {"Generic Graph" : "GG"}

graph_types = {"Conversion Loss" : "LO", 
               "Compression point" : "RF", 
               "Harmonic Intermodulation Products" : "SP", 
               "Spurious Distribution" : "SD"}


def openGenericTxtfile(filename, skip_first_row = 0):
    #open the output file and return the table of value without header
    #the table format is: [[value, value, ... value], [value, value, ... value], ... , [value, value, ... value]]
    #return table_of_values, uniform_unit, output_path_file
    #return empty table if error
    result = []
    try:
        with open(filename, 'r') as txtfile:
            for row in txtfile.readlines():
                result.append(row.split())
        #remove separator and header take unit value
        result_eval = []
        row_skiped_len = len(result[skip_first_row])
        first_column = result[0][1]
        for row in result[skip_first_row:]:
            #uniform unit and convert string to value
            if len(row) == row_skiped_len:
                if row[0] == "freq":
                    #new series
                    first_column = row[1]
                else:
                    result_eval.append([first_column] + [eval(token.replace(",", ".")) for token in row])
        
        return result_eval, unit.Hz, os.path.dirname(filename)
    except:
        return [], unit.Hz, None


def openSpuriusfile(filename):
    #open the output file and return the table of value without header
    #the table format is: [frequency_LO, unit_LO, power_LO, is_LO_calibrated, frequency_RF, unit_RF, power_RF, is_RF_calibrated, frequency_IF, unit_IF, power_IF, is_IF_calibrated, n_LO, m_RF]
    #return table_of_values, uniform_unit, output_path_file
    #return empty table if error
    result = []
    try:
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                result.append(row)
        #remove separator and header take unit value
        result_eval = []
        for row in result[2:]:
            #uniform unit and convert string to value
            
            result_eval.append([unit.convertion_to_base(eval(row[frequency_LO_index].replace(",", ".")), unit.return_unit(row[unit_LO_index])),
                                unit.Hz,
                                eval(row[power_LO_index].replace(",", ".")),
                                row[is_LO_calibrated_index],
                                unit.convertion_to_base(eval(row[frequency_RF_index].replace(",", ".")), unit.return_unit(row[unit_RF_index])),
                                unit.Hz,
                                eval(row[power_RF_index].replace(",", ".")),
                                row[is_RF_calibrated_index],
                                unit.convertion_to_base(eval(row[frequency_IF_index].replace(",", ".")), unit.return_unit(row[unit_IF_index])),
                                unit.Hz,
                                eval(row[power_IF_index].replace(",", ".")),
                                row[is_IF_calibrated_index],
                                eval(row[n_LO_index].replace(",", ".")),
                                eval(row[m_RF_index].replace(",", "."))])
        
        return result_eval, unit.Hz, os.path.dirname(filename)
    except:
        return [], unit.Hz, None

def splitSpuriusCfiletablevalueDict(data_file_name, graph_type, table_value, sort_data, group_level_01, SD_LO_Frequency, SD_LO_Level, SD_RF_Level, SD_IF_Min_Level, savefile = True):
    """
    build a list of list of data sorted by sort_data index list and grouped by group_level_01 index list
    the restult is [[LO_Freq, LO_Freq_unit, LO_Level, ..., n_LO, m_RF, -(RF_Level-IF_level)], 
                    [LO_Freq, LO_Freq_unit, LO_Level, ..., n_LO, m_RF, -(RF_Level-IF_level)], 
                    ..., 
                    [LO_Freq, LO_Freq_unit, LO_Level, ..., n_LO, m_RF, -(RF_Level-IF_level)]]
    """
    #the table format is: [
   
    table_value = sorted(table_value, key=operator.itemgetter(*sort_data)) 
    
    #add columnd -(power_RF - power_IF)
    table_result = []
    if graph_type in graph_types.values() + ["IP1"]:
        for row in table_value:
            table_result.append(row + [-(row[power_RF_index] - row[power_IF_index])])
    elif graph_type in generic_graph_types.values():
        table_result = table_value
    
    if savefile:
        filepointer = open(data_file_name.split(".")[0] + "_" + graph_type + "_" + return_now_postfix() + ".csv", "wb")
        create_csv(filepointer, csv_file_header, [], table_result)
        filepointer.close()
    
    group_result = [[table_result[0][:]]]
    last_tupla = tuple([table_result[0][index] for index in group_level_01])
    #last_tupla = (table_result[0][n_LO_index], table_result[0][m_RF_index], table_result[0][frequency_LO_index], table_result[0][power_LO_index])
    for row in table_result[1:]: #first row in group_result yet
        if graph_type == "SD" and row[power_LO_index] == SD_LO_Level and row[power_RF_index] == SD_RF_Level and row[power_IF_index]>SD_IF_Min_Level:
            if row[frequency_LO_index] == SD_LO_Frequency:

                    current_tupla = tuple([row[index] for index in group_level_01])
                    if last_tupla == current_tupla:
                        group_result[-1].append(row[:])
                    else:
                        last_tupla = current_tupla
                        group_result.append([row[:]])
        elif graph_type == "GG":
            current_tupla = tuple([row[index] for index in group_level_01])
            if last_tupla == current_tupla:
                group_result[-1].append(row[:])
            else:
                last_tupla = current_tupla
                group_result.append([row[:]])
            #group_result[-1].append(row[:])
        elif graph_type in ["LO", "RF", "SP", "IP1"]:
            current_tupla = tuple([row[index] for index in group_level_01])
            if last_tupla == current_tupla:
                group_result[-1].append(row[:])
            else:
                last_tupla = current_tupla
                group_result.append([row[:]])
    return group_result


def order_and_group_data(data_file_name, 
                       graph_type, 
                       SD_LO_Frequency,
                       SD_LO_Level,
                       SD_RF_Level,
                       SD_IF_Min_Level,
                       IF_Frequency_selected = 1000,
                       savefile = True):
    """
    data = dict{(n, m, Freq_LO, Level_LO, Level_RF): [Freq_unit_LO, Calib_LO, Freq_RF, Freq_unit_RF, Calib_RF, Freq_IF, Freq_unit_IF, Level_IF, Calib_IF, -(Level_RF - Level_IF)]}
    """
    if graph_type in graph_types.values() + ["IP1"]:
        file_table_result, unit_value, data_file_directory = openSpuriusfile(data_file_name)
    elif graph_type in generic_graph_types.values():
        file_table_result, unit_value, data_file_directory = openGenericTxtfile(data_file_name, skip_first_row = 1)
        
    sort_data = []
    group_level_01 = []
    graph_group_index = []
    x_index = power_RF_index
    y_index = power_IF_index
    z_index = power_IF_index
    legend_index = [(power_LO_index, None, "", n_LO_index)]
    
    
    if graph_type == "LO":
        #sort_data: sort_data[-1] is the x axes
        sort_data = [n_LO_index, m_RF_index, frequency_LO_index, power_RF_index, power_LO_index, frequency_IF_index]
        #a graph for each tupla
        group_level_01 = [n_LO_index, m_RF_index, frequency_LO_index, power_RF_index]
        #a row for each tupla
        graph_group_index = [power_LO_index]
        x_index = frequency_IF_index
        y_index = conversion_loss
        legend_index = [(power_LO_index, unit.dB, "", n_LO_index)]
    if graph_type == "GG":
        #sort_data: sort_data[-1] is the x axes
        sort_data = [0, 1]
        #a graph for each tupla
        group_level_01 = []
        #a row for each tupla
        graph_group_index = [0]
        x_index = 1
        y_index = 2
        legend_index = [(0, -1, "", 0)]
    elif graph_type == "RF":
        sort_data = [n_LO_index, m_RF_index, frequency_LO_index, frequency_RF_index,  power_LO_index, power_RF_index]
        group_level_01 = [n_LO_index, m_RF_index, frequency_LO_index, frequency_RF_index]
        graph_group_index = [power_LO_index]
        x_index = power_RF_index
        y_index = power_IF_index
        legend_index = [(power_LO_index, unit.dB, "", n_LO_index)]
    elif graph_type == "IP1":
        sort_data = [n_LO_index, frequency_LO_index, power_LO_index]
        group_level_01 = [n_LO_index, frequency_LO_index]
        graph_group_index = [frequency_LO_index]
        x_index = power_LO_index
        y_index = power_IF_index
        legend_index = [(power_LO_index, unit.dB, "", n_LO_index)]
    elif graph_type == "SP":
        sort_data = [frequency_IF_index, frequency_LO_index, frequency_RF_index,  power_LO_index, power_RF_index] #, n_LO_index, m_RF_index]
        group_level_01 = [frequency_IF_index, frequency_LO_index, frequency_RF_index]
        graph_group_index = [power_LO_index]
        x_index = power_RF_index
        y_index = power_IF_index
        legend_index = [(power_LO_index, unit.dB, "", n_LO_index)]
    elif graph_type == "SD":
        sort_data = [n_LO_index, m_RF_index, power_LO_index, power_RF_index, power_IF_index]
        group_level_01 = [n_LO_index, m_RF_index, power_LO_index, power_RF_index]
        graph_group_index = [power_LO_index]
        x_index = frequency_IF_index
        y_index = power_IF_index
        legend_index = [(power_LO_index, unit.dB, "", n_LO_index)]
    #data_table = splitSpuriusCfiletablevalue(file_table_result)
    return splitSpuriusCfiletablevalueDict(data_file_name, graph_type, file_table_result, sort_data, group_level_01, SD_LO_Frequency = SD_LO_Frequency, SD_LO_Level = SD_LO_Level, SD_RF_Level = SD_RF_Level, SD_IF_Min_Level = SD_IF_Min_Level, savefile = savefile), data_file_directory, graph_group_index, x_index, y_index, z_index, legend_index
    

class Graph_Axis_Range(Frequency_Range):
    def __init__(self, a_min, a_max, a_step, a_unit, a_label = None):
        Frequency_Range.__init__(self, a_min, a_max, a_step, a_unit)
        if a_label is None:
            self.label = None
        elif a_label == "":
            self.label = None
        else:
            self.label = a_label
        
    def set_default(self):
        self.min = 100
        self.max = 3000
        self.step = 100
        self.label = "Axes"
        self.unit = unit.MHz
        
    def return_ticks_range(self, round_value = 2, not_round = False):
        if not_round:
            return np.arange(self.from_base().min, self.from_base().max + self.from_base().step, self.from_base().step)
        else:
            return [round(x, round_value) for x in np.arange(self.from_base().min, self.from_base().max + self.from_base().step, self.from_base().step)]