'''
Created on 08/mag/2016

@author: sabah
'''


#Convertion Loss

#Compression Point

#Harmonic Intermodulation Products
#Harmonic 1000MHz (LO = 5000MHz; RF = 3000MHz)


import csv
import numpy as np
from scipy.interpolate import UnivariateSpline
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import gca
from matplotlib.colors import colorConverter
#from mpl_toolkits.mplot3d import axes3d
import sys
import operator

from utility import create_csv, create_csv, unit_class, return_now_postfix
import os.path
from csvutility import frequency_LO_index, unit_LO_index, power_LO_index, is_LO_calibrated_index, frequency_RF_index, unit_RF_index, power_RF_index, is_RF_calibrated_index, frequency_IF_index, unit_IF_index, power_IF_index, is_IF_calibrated_index, n_LO_index, m_RF_index, conversion_loss, csv_file_header
from measure_scripts.csvutility import frequency_IF_index, frequency_LO_index
from graphutility import styles, linecolors, markerstyles, csfont_axislegend, csfont_axisticks, csfont_legendlines, csfont_legendtitle, csfont_suptitle, csfont_title

unit = unit_class()


final = []
final2 = []




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
            
            result_eval.append([eval(row[frequency_LO_index].replace(",", ".")),
                                unit.return_unit(row[unit_LO_index]),
                                eval(row[power_LO_index].replace(",", ".")),
                                row[is_LO_calibrated_index],
                                unit.unit_conversion(eval(row[frequency_RF_index].replace(",", ".")), unit.return_unit(row[unit_RF_index]), unit.return_unit(row[unit_LO_index])),
                                unit.return_unit(row[unit_LO_index]),
                                eval(row[power_RF_index].replace(",", ".")),
                                row[is_RF_calibrated_index],
                                round(unit.unit_conversion(eval(row[frequency_IF_index].replace(",", ".")), unit.return_unit(row[unit_IF_index]), unit.return_unit(row[unit_LO_index])), 0),
                                unit.return_unit(row[unit_LO_index]),
                                eval(row[power_IF_index].replace(",", ".")),
                                row[is_IF_calibrated_index],
                                eval(row[n_LO_index].replace(",", ".")),
                                eval(row[m_RF_index].replace(",", "."))])
        
        return result_eval, unit.return_unit(result[1][1]), os.path.dirname(filename)
    except:
        return [], unit.MHz, None

def splitSpuriusCfiletablevalueDict(data_file_name, graph_type, table_value, sort_data, group_level_01, SD_LO_Level, SD_RF_Level, SD_IF_Min_Level, savefile = True):
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
    for row in table_value:
        table_result.append(row + [-(row[power_RF_index] - row[power_IF_index])])
    
    if savefile:
        filepointer = open(data_file_name.split(".")[0] + "_" + graph_type + "_" + return_now_postfix() + ".csv", "wb")
        create_csv(filepointer, csv_file_header, [], table_result)
        filepointer.close()
    
    group_result = [[table_result[0][:]]]
    last_tupla = tuple([table_result[0][index] for index in group_level_01])
    #last_tupla = (table_result[0][n_LO_index], table_result[0][m_RF_index], table_result[0][frequency_LO_index], table_result[0][power_LO_index])
    for row in table_result[1:]:
        if graph_type == "SD" and row[power_LO_index] == SD_LO_Level and row[power_RF_index] == SD_RF_Level and row[power_IF_index]>SD_IF_Min_Level:
            current_tupla = tuple([row[index] for index in group_level_01])
            if last_tupla == current_tupla:
                group_result[-1].append(row[:])
            else:
                last_tupla = current_tupla
                group_result.append([row[:]])
        elif graph_type == "LO" or graph_type == "RF" or graph_type == "SP":
            current_tupla = tuple([row[index] for index in group_level_01])
            if last_tupla == current_tupla:
                group_result[-1].append(row[:])
            else:
                last_tupla = current_tupla
                group_result.append([row[:]])
    return group_result
        

def order_and_group_data(data_file_name, 
                       graph_type, 
                       SD_LO_Level,
                       SD_RF_Level,
                       SD_IF_Min_Level,
                       IF_Frequency_selected = 1000,
                       savefile = True):
    """
    data = dict{(n, m, Freq_LO, Level_LO, Level_RF): [Freq_unit_LO, Calib_LO, Freq_RF, Freq_unit_RF, Calib_RF, Freq_IF, Freq_unit_IF, Level_IF, Calib_IF, -(Level_RF - Level_IF)]}
    """
    file_table_result, unit_value, data_file_directory = openSpuriusfile(data_file_name)
    if graph_type == "LO":
        #sort_data: sort_data[-1] is the x axes
        sort_data = [n_LO_index, m_RF_index, frequency_LO_index, power_RF_index, power_LO_index, frequency_IF_index]
        #a graph for each tupla
        group_level_01 = [n_LO_index, m_RF_index, frequency_LO_index, power_RF_index]
        #a row for each tupla
        graph_group_index = [power_LO_index]
        x_index = frequency_IF_index
        y_index = conversion_loss
        legend_index = [(power_LO_index, None, "LO", n_LO_index)]
    elif graph_type == "RF":
        sort_data = [n_LO_index, m_RF_index, frequency_LO_index, frequency_RF_index,  power_LO_index, power_RF_index]
        group_level_01 = [n_LO_index, m_RF_index, frequency_LO_index, frequency_RF_index]
        graph_group_index = [power_LO_index]
        x_index = power_RF_index
        y_index = power_IF_index
        legend_index = [(power_LO_index, None, "LO", n_LO_index)]
    elif graph_type == "SP":
        sort_data = [frequency_IF_index, frequency_LO_index, frequency_RF_index,  power_LO_index, power_RF_index]
        group_level_01 = [frequency_IF_index, frequency_LO_index, frequency_RF_index,]
        graph_group_index = [power_LO_index]
        x_index = power_RF_index
        y_index = power_IF_index
        legend_index = [(power_LO_index, None, "LO", n_LO_index)]
    elif graph_type == "SD":
        sort_data = [n_LO_index, m_RF_index, power_LO_index, power_RF_index, power_IF_index]
        group_level_01 = [n_LO_index, m_RF_index, power_LO_index, power_RF_index]
        graph_group_index = [power_LO_index]
        x_index = frequency_IF_index
        y_index = power_IF_index
        legend_index = [(power_LO_index, None, "LO", n_LO_index)]
    #data_table = splitSpuriusCfiletablevalue(file_table_result)
    return splitSpuriusCfiletablevalueDict(data_file_name, graph_type, file_table_result, sort_data, group_level_01, SD_LO_Level = SD_LO_Level, SD_RF_Level = SD_RF_Level, SD_IF_Min_Level = SD_IF_Min_Level, savefile = savefile), data_file_directory, graph_group_index, x_index, y_index, legend_index
    
    
def convert_x_y_axes(data_table, graph_x_unit, x_index, graph_y_unit, y_index):
    result_eval = [[] for x in range(len(data_table))]
    k = 0
    for group in data_table:
        j = 0
        for row in group:
            new_row = []
            if x_index == frequency_LO_index:
                new_row.append(unit.unit_conversion(row[frequency_LO_index], row[unit_LO_index], graph_x_unit))
                new_row.append(graph_x_unit)
            elif y_index == frequency_LO_index:
                new_row.append(unit.unit_conversion(row[frequency_LO_index], row[unit_LO_index], graph_y_unit))
                new_row.append(graph_y_unit)
            else:
                new_row.append(row[frequency_LO_index])
                new_row.append(row[unit_LO_index])
            new_row.append(row[power_LO_index])
            new_row.append(row[is_LO_calibrated_index])
            if x_index == frequency_RF_index:
                new_row.append(unit.unit_conversion(row[frequency_RF_index], row[unit_RF_index], graph_x_unit))
                new_row.append(graph_x_unit)
            elif y_index == frequency_RF_index:
                new_row.append(unit.unit_conversion(row[frequency_RF_index], row[unit_RF_index], graph_y_unit))
                new_row.append(graph_y_unit)
            else:
                new_row.append(row[frequency_RF_index])
                new_row.append(row[unit_RF_index])
            new_row.append(row[power_RF_index])
            new_row.append(row[is_RF_calibrated_index])
            if x_index == frequency_IF_index:
                new_row.append(unit.unit_conversion(row[frequency_IF_index], row[unit_IF_index], graph_x_unit))
                new_row.append(graph_x_unit)
            elif y_index == frequency_RF_index:
                new_row.append(unit.unit_conversion(row[frequency_IF_index], row[unit_IF_index], graph_y_unit))
                new_row.append(graph_y_unit)
            else:
                new_row.append(row[frequency_IF_index])
                new_row.append(row[unit_IF_index])
            new_row.append(row[power_IF_index])
            new_row.append(row[is_IF_calibrated_index])
            new_row.append(row[n_LO_index])
            new_row.append(row[m_RF_index])
            new_row.append(row[conversion_loss])
            result_eval[k].append(new_row)
            j += 1
        k += 1
    return result_eval


def plot_spurius_graph(data_file_name, 
                       graph_type, 
                       graph_title, 
                       graph_x_label, 
                       graph_x_label_auto, 
                       graph_x_min, 
                       graph_x_min_auto,
                       graph_x_max, 
                       graph_x_max_auto, 
                       graph_x_step, 
                       graph_x_step_auto, 
                       graph_x_unit,
                       graph_y_label, 
                       graph_y_label_auto,
                       graph_y_min,
                       graph_y_min_auto, 
                       graph_y_max, 
                       graph_y_max_auto, 
                       graph_y_step, 
                       graph_y_step_auto,
                       graph_y_unit,
                       SD_LO_Level,
                       SD_RF_Level,
                       SD_IF_Min_Level,
                       IF_Frequency_selected = 1000):
    """
    data = dict{(n, m, Freq_LO, Level_LO, Level_RF): [Freq_unit_LO, Calib_LO, Freq_RF, Freq_unit_RF, Calib_RF, Freq_IF, Freq_unit_IF, Level_IF, Calib_IF, -(Level_RF - Level_IF)]}
    """
    
    data_table, data_file_directory, graph_group_index, x_index, y_index, legend_index = order_and_group_data(data_file_name, 
                       graph_type, 
                       SD_LO_Level = SD_LO_Level,
                       SD_RF_Level = SD_RF_Level,
                       SD_IF_Min_Level = SD_IF_Min_Level,
                       IF_Frequency_selected = IF_Frequency_selected)
    
    data_table = convert_x_y_axes(data_table, graph_x_unit, x_index, graph_y_unit, y_index)
    
    data_file_directory = os.path.join(data_file_directory, "_".join([graph_type, return_now_postfix()]))
    if not os.path.exists(data_file_directory):
        try:
            os.makedirs(data_file_directory)
        except:
            print("Error creating " + data_file_directory)
            return 0
    group_for_SD = []
    for row_grouped in data_table:
        plot_this = False
        if (graph_type == "RF" or graph_type == "LO") and (row_grouped[0][n_LO_index] == 1 or row_grouped[0][n_LO_index] == -1) and (row_grouped[0][m_RF_index] == 1 or row_grouped[0][m_RF_index] == -1):
            plot_this = True
        elif graph_type == "SP" and row_grouped[0][n_LO_index] != 1 and row_grouped[0][n_LO_index] != -1 and row_grouped[0][m_RF_index] != 1 and row_grouped[0][m_RF_index] != -1 and row_grouped[0][frequency_IF_index] == IF_Frequency_selected:
            plot_this = True
        elif graph_type == "SD" and row_grouped[0][n_LO_index] != 1 and row_grouped[0][n_LO_index] != -1 and row_grouped[0][m_RF_index] != 1 and row_grouped[0][m_RF_index] != -1:
            group_for_SD.append(row_grouped[:])
            plot_this = False
        if plot_this:
            plot_spurius_C(table_value = row_grouped,
                           graph_group_index = graph_group_index,
                           x_index = x_index,
                           y_index = y_index,
                           legend_index = legend_index, 
                           graph_title = graph_title, 
                           graph_type = graph_type,
                           graph_x_label = graph_x_label, 
                           graph_x_label_auto = graph_x_label_auto,
                           graph_x_min = graph_x_min, 
                           graph_x_min_auto = graph_x_min_auto,
                           graph_x_max = graph_x_max, 
                           graph_x_max_auto = graph_x_max_auto,
                           graph_x_step = graph_x_step, 
                           graph_x_step_auto = graph_x_step_auto,
                           graph_x_unit = graph_x_unit,
                           graph_y_label = graph_y_label, 
                           graph_y_label_auto = graph_y_label_auto,
                           graph_y_min = graph_y_min, 
                           graph_y_min_auto = graph_y_min_auto,
                           graph_y_max = graph_y_max, 
                           graph_y_max_auto = graph_y_max_auto,
                           graph_y_step = graph_y_step, 
                           graph_y_step_auto = graph_y_step_auto,
                           graph_y_unit = graph_y_unit,
                           data_file_directory = data_file_directory)
    if len(group_for_SD)>0:
        plot_spurius_C(table_value = group_for_SD,
                           graph_group_index = graph_group_index,
                           x_index = x_index,
                           y_index = y_index,
                           legend_index = legend_index, 
                           graph_title = graph_title, 
                           graph_type = graph_type,
                           graph_x_label = graph_x_label, 
                           graph_x_label_auto = graph_x_label_auto,
                           graph_x_min = graph_x_min, 
                           graph_x_min_auto = graph_x_min_auto,
                           graph_x_max = graph_x_max, 
                           graph_x_max_auto = graph_x_max_auto,
                           graph_x_step = graph_x_step, 
                           graph_x_step_auto = graph_x_step_auto,
                           graph_x_unit = graph_x_unit,
                           graph_y_label = graph_y_label, 
                           graph_y_label_auto = graph_y_label_auto,
                           graph_y_min = graph_y_min, 
                           graph_y_min_auto = graph_y_min_auto,
                           graph_y_max = graph_y_max, 
                           graph_y_max_auto = graph_y_max_auto,
                           graph_y_step = graph_y_step, 
                           graph_y_step_auto = graph_y_step_auto,
                           graph_y_unit = graph_y_unit,
                           data_file_directory = data_file_directory)

def plot_spurius_C(table_value, 
                   graph_group_index,
                   x_index,
                   y_index,
                   legend_index, 
                   graph_title, 
                   graph_type,
                   graph_x_label = 'Input Power(dBm)', 
                   graph_x_label_auto = False,
                   graph_x_min = 100, 
                   graph_x_min_auto = False,
                   graph_x_max = 3000, 
                   graph_x_max_auto = False,
                   graph_x_step = 100, 
                   graph_x_step_auto = False,
                   graph_x_unit = unit.MHz,
                   graph_y_label = 'Output Power(dBm)', 
                   graph_y_label_auto = False,
                   graph_y_min = -10, 
                   graph_y_min_auto = False,
                   graph_y_max = 0, 
                   graph_y_max_auto = False,
                   graph_y_step = 1, 
                   graph_y_step_auto = False,
                   graph_y_unit = unit.MHz,
                   data_file_directory = ""):
    
    fig = plt.figure()
    #for i in range (1, 13):
    #    fig.add_subplot(4, 3, i)
    plot_spurius_Single(fig, table_value = table_value, 
                   graph_group_index = graph_group_index,
                   x_index = x_index,
                   y_index = y_index,
                   legend_index = legend_index,  
                   graph_title = graph_title, 
                   graph_type = graph_type,
                   graph_x_label = graph_x_label, 
                   graph_x_label_auto = graph_x_label_auto,
                   graph_x_min = graph_x_min, 
                   graph_x_min_auto = graph_x_min_auto,
                   graph_x_max = graph_x_max, 
                   graph_x_max_auto = graph_x_max_auto,
                   graph_x_step = graph_x_step, 
                   graph_x_step_auto = graph_x_step_auto,
                   graph_x_unit = graph_x_unit,
                   graph_y_label = graph_y_label, 
                   graph_y_label_auto = graph_y_label_auto,
                   graph_y_min = graph_y_min, 
                   graph_y_min_auto = graph_y_min_auto,
                   graph_y_max = graph_y_max, 
                   graph_y_max_auto = graph_y_max_auto,
                   graph_y_step = graph_y_step, 
                   graph_y_step_auto = graph_y_step_auto,
                   graph_y_unit = graph_y_unit,
                   data_file_directory = data_file_directory)
    
    
def plot_3d_distribution(fig, data_table):

    ax = fig.add_subplot(111, projection='3d')
    front_back_position = [x*10 for x in range(1, len(data_table)+2)] #same number of y ticks as list of value for couple n,m
    color = ['r', 'g', 'b', 'y']
    yticklabels = [str(r[0][n_LO_index])+ ", " + str(r[0][m_RF_index]) for r in data_table]
    ax.set_yticks(front_back_position)
    ax.set_yticklabels(yticklabels)
    color_index = 0
    fb_index = 0
    sort_data = [frequency_IF_index]
    for row_group in data_table:
        tmp_row_group = sorted(row_group, key=operator.itemgetter(*sort_data)) 
        freq = [r[frequency_IF_index] for r in tmp_row_group]
        level = [r[power_IF_index] for r in tmp_row_group]
        #ref = min(level)
        #level = [l - ref for l in level]
        color_index += 1
        if color_index >= len(color):
            color_index = 0
        ax.bar(freq, level, zs=front_back_position[fb_index], color = color[color_index], width  = 50, zdir='y', alpha=0.8)
        fb_index += 1
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.gca().invert_zaxis()
    plt.show()


def plot_spurius_Single(fig, table_value, 
                   graph_group_index,
                   x_index,
                   y_index,
                   legend_index, 
                   graph_title, 
                   graph_type,
                   graph_x_label = 'Input Power(dBm)', 
                   graph_x_label_auto = False,
                   graph_x_min = 100, 
                   graph_x_min_auto = False,
                   graph_x_max = 3000, 
                   graph_x_max_auto = False,
                   graph_x_step = 100, 
                   graph_x_step_auto = False,
                   graph_x_unit = unit.MHz,
                   graph_y_label = 'Output Power(dBm)', 
                   graph_y_label_auto = False,
                   graph_y_min = -10, 
                   graph_y_min_auto = False,
                   graph_y_max = 0, 
                   graph_y_max_auto = False,
                   graph_y_step = 1, 
                   graph_y_step_auto = False,
                   graph_y_unit = unit.MHz,
                   data_file_directory = ""):
    """

    """
    spl = []
    
    filter_1 = False
    if graph_x_min is None:
        graph_x_min = 100
    if graph_x_max is None:
        graph_x_max = 3000
    if graph_x_step is None:
        graph_x_step = 100
    if graph_y_min is None:
        graph_y_min = -10
    if graph_y_max is None:
        graph_y_max = 0
    if graph_y_step is None:
        graph_y_step = 1
         
    x_y_offset = 0

    
    if graph_type == "LO":
        if not graph_x_label:
            graph_x_label = 'IF Freq (' + unit.return_unit_str(table_value[0][x_index + 1])  +  ')'
        else:
            graph_x_label = graph_x_label.format(unit = unit.return_unit_str(table_value[0][x_index + 1]))
        if not graph_y_label:
            graph_y_label = "IF Power Loss (dBm)"
        if not graph_title:
            graph_sup_title = "Conversion Loss"
        else:
            graph_sup_title = graph_title
        graph_title = "LO " + str(table_value[0][frequency_LO_index]) + unit.return_unit_str(table_value[0][unit_LO_index]) + " - RF " + str(table_value[0][power_RF_index]) + "dBm"
        legend_title = "LO"
    elif graph_type == "RF":
        if not graph_x_label:
            graph_x_label = 'RF Power (dBm)'
        else:
            graph_x_label = graph_x_label.format(unit = "dBm")
        if not graph_y_label:
            graph_y_label = "IF Power (dBm)"
        if not graph_title:
            graph_sup_title = "Compression Point"
            
        else:
            graph_sup_title = graph_title
        graph_title = "LO " + str(table_value[0][frequency_LO_index]) + unit.return_unit_str(table_value[0][unit_LO_index]) + " - RF " + str(table_value[0][frequency_RF_index]) + unit.return_unit_str(table_value[0][unit_RF_index])
        legend_title = "LO"
    elif graph_type == "SP":
        if not graph_x_label:
            graph_x_label = 'RF Power (dBm)'
        else:
            graph_x_label = graph_x_label.format(unit = "dBm")
        if not graph_y_label:
            graph_y_label = "IF Power (dBm)"
        if not graph_title:
            graph_sup_title = "Harmonic Intermodulation Products"
        else:
            graph_sup_title = graph_title
        graph_title = "IF " + str(table_value[0][frequency_IF_index]) + unit.return_unit_str(table_value[0][unit_IF_index]) + " (LO " + str(table_value[0][frequency_LO_index]) + unit.return_unit_str(table_value[0][unit_LO_index]) + " (" + str(table_value[0][n_LO_index]) + ")" + "; RF " + str(table_value[0][frequency_RF_index]) + unit.return_unit_str(table_value[0][unit_RF_index]) + "(" + str(table_value[0][m_RF_index]) + "))"
        filter_1 = True
        legend_title = "LO"
    elif graph_type == "SD":
        if not graph_x_label:
            graph_x_label = 'IF Freq (MHz)'
        if not graph_y_label:
            graph_y_label = "IF Power (dBm)"
        if not graph_title:
            graph_sup_title = "Spurious Distribution"
        filter_1 = True
        graph_title = ""
        legend_title = "IF"
        
    #split by RF_level or LO_level
    if graph_type != "SD":
        last_group_index = tuple([table_value[0][index] for index in graph_group_index])
        result = [[table_value[0][:]]]
        for row in table_value[1:]:
            current_group_index = tuple([row[index] for index in graph_group_index])
            if current_group_index == last_group_index:
                result[-1].append(row[:])
            else:
                last_group_index = current_group_index
                result.append([row[:]])

    
    
    if graph_type == "SD":
        plot_3d_distribution(fig, table_value)
    else:

        ax = plt.axes(xlim=(graph_x_min, graph_x_max), ylim=(graph_y_min, graph_y_max))
        plt.xticks([round(x, 2) for x in np.arange(graph_x_min, graph_x_max +1, graph_x_step)])
        plt.yticks([round(x, 2) for x in np.arange(graph_y_min, graph_y_max +1, graph_y_step)])
        
        a = gca()
        a.set_xticklabels(a.get_xticks(), **csfont_axisticks)
        a.set_yticklabels(a.get_yticks(), **csfont_axisticks)
        
        
        
        plt.xlabel(graph_x_label, **csfont_axislegend)
        plt.ylabel(graph_y_label, **csfont_axislegend)
        plt.title(graph_title, **csfont_title)
        plt.suptitle(graph_sup_title, **csfont_suptitle)
        plt.grid(True)
        
        #graph_n_LO = table_value[0][12]
        #graph_m_LO = table_value[0][13]
        
        
        
        # Shrink current axis by 20%
    
    
    
    # Put a legend to the right of the current axis
        mn = 1000
        mx = -1000
        s = 0 #style index
        for row in result:
            if filter_1 and (row[0][n_LO_index] == 1 or row[0][n_LO_index] == -1 or row[0][m_RF_index] == 1 or row[0][m_RF_index] == -1):
                continue
            if s == len(styles):
                s = 0
            label = ""
            for l in legend_index:
                if l[1] is None:
                    tmp_unit = "dBm"
                    n_m = ""
                else:
                    tmp_unit = unit.return_unit_str(row[0][l[1]])
                    n_m = row[0][l[3]]
                label += l[2] + " " + str(row[0][l[0]]) + " " + tmp_unit + " " + str(n_m) + "\n"
            label = label[0:-1]
            x = [x[x_index] for x in row]
            y = [y[y_index] for y in row]
            if graph_y_min_auto:
                if min(y)<mn:
                    mn = min(y)
            else:
                mn = graph_y_min
            if graph_y_max_auto:
                if max(y)>mx:
                    mx = max(y)
            else:
                mx = graph_y_max
                
                
            
                
            ax.set_ylim([mn-x_y_offset, mx+x_y_offset])
            plt.xticks([round(xt, 2) for xt in np.arange(graph_x_min, graph_x_max +1, graph_x_step)])
            plt.yticks([round(yt, 2) for yt in np.arange(mn-x_y_offset, mx+x_y_offset +1, graph_y_step)])
            a.set_xticklabels(a.get_xticks(), **csfont_axisticks)
            a.set_yticklabels(a.get_yticks(), **csfont_axisticks)
            markercolor = tuple(list(colorConverter.to_rgb(styles[s][1])) + [0.4])
            ax.plot(np.array(x), np.array(y), label=label, linestyle='-', marker=styles[s][0], color=styles[s][1], markerfacecolor=markercolor)
            s += 1
        
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
        legend_object =  ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title = legend_title)
        #legend_object.set_title(title = legend_title, prop = csfont_title)
        #legend_object.get_title().set_fontsize(csfont_title["fontsize"]) #legend 'Title' fontsize
        #legend_object.get_title().set_fontname(csfont_title["fontname"])
        plt.setp(plt.gca().get_legend().get_title(), **csfont_legendtitle)
        plt.setp(plt.gca().get_legend().get_texts(), **csfont_legendlines) #legend 'list' fontsize
            
            
            #curves_data.append(np.array([t, [spl[-1](x) for x in t]]))
        #len(curves_data[0][0])
        #line_ani = animation.FuncAnimation(fig, update_sprius_line, 100,  fargs=(curves_data, curves, spl), interval=interval, blit=False, repeat=False)
        #plt.show()
        
        
        plt.savefig(os.path.join(data_file_directory, "Graph_" + graph_title + ".png"))
        

fig = None
ax = None
curve = None


#if __name__ == "__main__":
#    sys.exit(calculate_all_IP1(ip1_filename, graph_title = None))