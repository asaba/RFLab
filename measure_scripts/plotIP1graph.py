'''
Created on 08/mag/2016

@author: sabah
'''

import csv
import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import gca
import sys
from utility import eval_if, SplineError, PointNotFound

from csvutility import frequency_LO_index, unit_LO_index, power_LO_index, is_LO_calibrated_index, frequency_RF_index, \
    unit_RF_index, power_RF_index, is_RF_calibrated_index, frequency_IF_index, unit_IF_index, power_IF_index, \
    is_IF_calibrated_index, n_LO_index, m_RF_index, conversion_loss, csv_file_header

from graphutility import openSpuriusfile, splitSpuriusCfiletablevalueDict, order_and_group_data

from utility import save_data, save_settings, create_csv, unit_class, return_now_postfix
import os.path

unit = unit_class()

ip1_filename = "misura IP1 ZVA213_3.csv"

final = []
final2 = []


def openIP1file(filename):
    # open the output file and return the table of value without header
    # the table format is: [frequency, power_input, power_calibrated, is_calibrated, attenuation, power output]
    # return empty table if error
    result = []
    try:
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                result.append(row)
        # remove separator and header take unit value
        return result[2:], unit.return_unit(result[1][0].split("(")[1].split(")")[0]), os.path.dirname(filename)
    except:
        return [], unit.MHz, None


def splitIP1filetablevalue(table_value):
    """
    build a dictionary of values from table extracted from spurius file measure
    the stucture is dict{frequency: [power_level_input, power_level_output, calibration_info]}
    """
    file_measures = {}
    power_input_curve = []
    power_linear_last_index = 0
    power_output_curve = []

    for i in table_value:
        current_frequency = eval_if(i[0])
        if current_frequency in file_measures:
            file_measures[current_frequency].append([eval_if(i[1]),
                                                     eval_if(i[5]),
                                                     i[3]])
        else:
            file_measures[current_frequency] = {}
            file_measures[current_frequency] = [[eval_if(i[1]),
                                                 eval_if(i[5]),
                                                 i[3]]]

    return file_measures


def calculate_all_IP1(data_file_name,
                      graph_title,
                      graph_x,
                      graph_y,
                      IF_Frequency_selected,
                      animated,
                      font_style=None):
    """
    data = dict{frequency: [power_level_input, power_level_output, calibration_info]}
    """

    file_table_result, unit_value, data_file_directory = openSpuriusfile(data_file_name)

    data_table, data_file_directory, graph_group_index, x_index, y_index, z_index, legend_index = order_and_group_data(
        data_file_name,
        "IP1",
        SD_LO_Frequency=None,
        SD_LO_Level=None,
        SD_RF_Level=None,
        SD_IF_Min_Level=None,
        IF_Frequency_selected=[])

    for frequency in IF_Frequency_selected:
        ip1_data = [[]]
        ip3_data = [[]]
        for dt in data_table:
            if dt[0][m_RF_index] == 1 and dt[0][frequency_RF_index] == frequency:
                ip1_data = dt[:]
            elif dt[0][m_RF_index] == 3 and dt[0][frequency_RF_index] == frequency:
                ip3_data = dt[:]
        calculateIP1(ip1_data,
                     ip3_data,
                     graph_title,
                     graph_x,
                     graph_y,
                     data_file_directory=data_file_directory,
                     animated=animated,
                     font_style=font_style)  # return list of value sorted by power_level_input field. Used to manage different measure for different attenuations
        #####TODO
        # for k, v in splitSpuriusCfiletablevalueDict(file_table_result).iteritems():
        #    calculateIP1(k, unit_value, sorted(v, key=lambda x: x[0]), graph_title, graph_x_label, graph_x_min, graph_x_max, graph_x_step, graph_y_label, graph_y_min, graph_y_max, graph_y_step, data_file_directory = data_file_directory, animated = animated) #return list of value sorted by power_level_input field. Used to manage different measure for different attenuations


def return_ip1_ip3(p_linear_ip1, spl_ip1, t_ip3, graph_x, p_linear_ip3):
    # return the x, y position of IP1 and IP3 point
    # p_linear_ip1 - linear function for IP1
    # p_linear_ip3 - linear function for IP1
    # spl_ip1 - spline function for IP1
    # graph_x - X axis range for graph
    # t_ip3 - X points

    IP1_x = None
    IP3_x = None
    if t_ip3:
        min_x_line_value = t_ip3[0]
    else:
        # check TODO
        min_x_line_value = graph_x.min
    if p_linear_ip3:
        IP3_x_diff = abs(p_linear_ip1(min_x_line_value) - p_linear_ip3(min_x_line_value))
    for x in np.arange(min_x_line_value, graph_x.max, 0.0001):
        ip_line_point = p_linear_ip1(x)
        if IP1_x is None and abs(ip_line_point - spl_ip1(x)) >= 1:
            # IP1 found
            IP1_x = x
        if p_linear_ip3:
            if abs(ip_line_point - p_linear_ip3(x)) <= 0.001:
                IP3_x = x
    if IP1_x is None:
        spl_ip1_point = None
    else:
        spl_ip1_point = spl_ip1(IP1_x)
    if IP3_x is None:
        spl_ip3_point = None
    else:
        spl_ip3_point = p_linear_ip3(IP3_x)
    return IP1_x, spl_ip1_point, IP3_x, spl_ip3_point


def calculateIP1(table_value_ip1,
                 table_value_ip3,
                 graph_title,
                 graph_x,
                 graph_y,
                 return_IP1=True,
                 data_file_directory="",
                 animated=False,
                 font_style=None):
    power_input_curve_ip1 = []
    power_linear_last_index_ip1 = 0
    power_output_curve_ip1 = []
    calibrated_ip1 = True
    IP1_x = None
    power_input_curve_ip3 = []
    power_linear_last_index_ip3 = 0
    power_output_curve_ip3 = []
    calibrated_ip3 = True
    IP3_x = None

    start_power = table_value_ip1[0][power_RF_index]
    for i in table_value_ip1:
        if str(i[is_RF_calibrated_index]) != "CAL":
            calibrated_ip1 = False
        power_input_curve_ip1.append(i[power_RF_index])
        power_output_curve_ip1.append(i[power_IF_index])
        if abs(power_input_curve_ip1[-1] - start_power) <= 5:
            power_linear_last_index_ip1 += 1

    x_curve_ip1 = np.array(power_input_curve_ip1)
    y_curve_ip1 = np.array(power_output_curve_ip1)
    coefficient_linear_ip1 = np.polyfit(x_curve_ip1[:power_linear_last_index_ip1],
                                        y_curve_ip1[:power_linear_last_index_ip1], 1)
    p_linear_ip1 = np.poly1d(coefficient_linear_ip1)
    try:
        spl_ip1 = UnivariateSpline(x_curve_ip1, y_curve_ip1, s=0)
    except:
        raise SplineError("Spline Error")
    t_ip1 = x_curve_ip1
    s_linear_ip1 = [p_linear_ip1(x) for x in
                    np.append(t_ip1,
                              [graph_x.max])]  # aggiungo un punto alla retta per disegnarla oltre la fine della curva

    t_ip3 = None
    p_linear_ip3 = None

    if len(table_value_ip3[0]) > 0:
        start_power = table_value_ip3[0][power_RF_index]
        start_power_index = 0
        for i in range(len(table_value_ip3)):
            if str(table_value_ip3[i][is_LO_calibrated_index]) != "CAL":
                calibrated_ip3 = False
            if table_value_ip3[i][power_IF_index] > -90:
                start_power = table_value_ip3[i][power_RF_index]
                start_power_index = i
                break
        for i in range(len(table_value_ip3)):
            power_input_curve_ip3.append(table_value_ip3[i][power_RF_index])
            power_output_curve_ip3.append(table_value_ip3[i][power_IF_index])
            if table_value_ip3[i][power_IF_index] > -90:
                if abs(table_value_ip3[i][power_RF_index] - start_power) <= 15:
                    power_linear_last_index_ip3 = i

        x_curve_ip3 = np.array(power_input_curve_ip3)
        y_curve_ip3 = np.array(power_output_curve_ip3)
        coefficient_linear_ip3 = np.polyfit(x_curve_ip3[start_power_index:power_linear_last_index_ip3],
                                            y_curve_ip3[start_power_index:power_linear_last_index_ip3], 1)
        p_linear_ip3 = np.poly1d(coefficient_linear_ip3)
        spl_ip3 = UnivariateSpline(x_curve_ip3, y_curve_ip3, s=0)
        t_ip3 = x_curve_ip3
        s_linear_ip3 = [p_linear_ip3(x) for x in np.append(t_ip3, [graph_x.max])]

    line_ani = None

    fig = plt.figure()

    if animated:
        interval = 1
    else:
        interval = 0

    ax = plt.axes(xlim=(graph_x.min, graph_x.max), ylim=(graph_y.min, graph_y.max))
    # ip1, = ax.plot([], [], "ro")
    # retta_ip1, = ax.plot([], [], "g--")
    # curve_ip1, = ax.plot([], [], "r-")
    # ip3, = ax.plot([], [], "bo")
    # retta_ip3, = ax.plot([], [], "c--")
    # curve_ip3, = ax.plot([], [], "b-")

    plt.xticks(graph_x.return_ticks_range())
    plt.yticks(graph_y.return_ticks_range())

    a = gca()
    a.set_xticklabels(a.get_xticks(), **font_style["axisticks"])
    a.set_yticklabels(a.get_yticks(), **font_style["axisticks"])

    if not graph_x.label:
        graph_x.label = 'Input Power(dBm)'
    plt.xlabel(graph_x.label, **font_style["axislegend"])
    if not graph_y.label:
        graph_y.label = "Output Power (dBm)"
    plt.ylabel(graph_y.label, **font_style["axislegend"])
    if not graph_title:
        graph_title = unit.return_human_readable_str(table_value_ip1[0][frequency_RF_index]) + " Cable Cal." + str(
            calibrated_ip1)
    plt.title(graph_title, **font_style["title"])
    plt.grid(True)
    lower = 0
    upper = len(t_ip1)
    middle = 0
    if return_IP1:
        ip1_x, ip1_y, ip3_x, ip3_y = return_ip1_ip3(p_linear_ip1, spl_ip1, t_ip3, graph_x, p_linear_ip3)

    curve_data_ip1 = np.array([t_ip1, [spl_ip1(x) for x in t_ip1]])
    line_data_ip1 = np.array([np.append(t_ip1, [graph_x.max]), s_linear_ip1])
    if len(table_value_ip3[0]) > 0:
        curve_data_ip3 = np.array([t_ip3, [spl_ip3(x) for x in t_ip3]])
        line_data_ip3 = np.array(np.append(t_ip3, [graph_x.max]), s_linear_ip3)
    if ip1_x is None:
        raise PointNotFound("IP1 not not found")
    else:
        # plot IP1 point
        ip1, = ax.plot([ip1_x], [ip1_y], "ro")
        plt.text(ip1_x + 0.2, ip1_y - 2, "{:.3f} dBm".format(ip1_x), **font_style["annotation"])
    retta_ip1, = ax.plot(line_data_ip1[0], line_data_ip1[1], "g--")
    curve_ip1, = ax.plot(curve_data_ip1[0], curve_data_ip1[1], "r-")
    if ip3_x is None:
        # TODO
        # Message IP3 not found
        pass
    else:
        ip3, = ax.plot([ip3_x], [ip3_y], "bo")
        plt.text(ip3_x + 0.2, ip3_y - 2, "{:.3f} dBm".format(ip3_x), **font_style["annotation"])
        retta_ip3, = ax.plot(line_data_ip3[0], line_data_ip3[1], "c--")
        curve_ip3, = ax.plot(curve_data_ip3[0], curve_data_ip3[1], "b-")

    # line_ani = animation.FuncAnimation(fig, update_line, len(line_data_ip1[0]),  fargs=(line_data_ip1, retta_ip1, p_linear_ip1, curve_data_ip1, curve_ip1, spl_ip1, ip1, line_data_ip3, retta_ip3, p_linear_ip3, curve_data_ip3, curve_ip3, spl_ip3, ip3), interval=interval, blit=False, repeat=False)
    plt.show()
    save_file_name = os.path.join(data_file_directory, unit.return_human_readable_str(
        table_value_ip1[0][frequency_RF_index]) + "_Cable_Cal" + str(
        calibrated_ip1) + "_" + return_now_postfix())
    fig.savefig(save_file_name + ".png")
    fig.savefig(save_file_name + ".svg")
    fig.savefig(save_file_name + ".eps")
    return IP1_x


# def update_line(num, line_data_ip1, line_ip1, line_generator_ip1, curve_data_ip1, curve_ip1, curve_generator_ip1, ip1, line_data_ip3, line_ip3, line_generator_ip3, curve_data_ip3, curve_ip3, curve_generator_ip3, ip3):
#    #line.set_data(data[0, :num], data[1,:num])
#    if len(line_ip1.get_xdata()) == len(line_data_ip1[0]):
#        return line_ip1, curve_ip1, line_ip3, curve_ip3
#    line_ip1.set_xdata(np.append(line_ip1.get_xdata(), line_data_ip1[0][num]))
#    line_ip1.set_ydata(np.append(line_ip1.get_ydata(), line_data_ip1[1][num]))
#    line_ip3.set_xdata(np.append(line_ip3.get_xdata(), line_data_ip3[0][num]))
#    line_ip3.set_ydata(np.append(line_ip3.get_ydata(), line_data_ip3[1][num]))
#    #line2.set_data(data2[0, :num], data2[1, :num])
#    #if num < len(curve_data_ip1[0]):
#    curve_ip1.set_xdata(np.append(curve_ip1.get_xdata(), curve_data_ip1[0][num]))
#    curve_ip1.set_ydata(np.append(curve_ip1.get_ydata(), curve_data_ip1[1][num]))
#    curve_ip3.set_xdata(np.append(curve_ip3.get_xdata(), curve_data_ip3[0][num]))
#    curve_ip3.set_ydata(np.append(curve_ip3.get_ydata(), curve_data_ip3[1][num]))
#    if len(ip1.get_xdata())==0:
#        if abs(line_data_ip1[1][num] - curve_data_ip1[1][num]) > 1.0:
#            for x in np.arange(curve_data_ip1[0][num-1], curve_data_ip1[0][num+1], 0.0001):
#                if abs(line_generator_ip1(x) - curve_generator_ip1(x))>=1:
#                    #IP1 found
#                    ip1.set_xdata(np.append(ip1.get_xdata(), curve_data_ip1[0][num]))
#                    ip1.set_ydata(np.append(ip1.get_ydata(), curve_data_ip1[1][num]))
#                    plt.text(x+0.2, curve_generator_ip1(x)-2, "{:.3f} dBm".format(x), **font_style["annotation"])
#                    break
#    if len(ip3.get_xdata())==0:
#        if line_data_ip1[1][num] > line_data_ip3[1][num]:
#            diff = line_data_ip1[1][num] - line_data_ip3[1][num]
#        else:
#            diff = line_data_ip3[1][num] - line_data_ip1[1][num]
#        
#        if diff < 0.0:
#            for x in np.arange(line_data_ip3[0][num-1], line_data_ip3[0][num+1], 0.0001):
#                if abs(line_generator_ip1(x) - line_generator_ip1(x))<0.0001:
#                    #IP3 found
#                    ip3.set_xdata(np.append(ip3.get_xdata(), line_data_ip3[0][num]))
#                    ip3.set_ydata(np.append(ip3.get_ydata(), line_data_ip3[1][num]))
#                    plt.text(x+0.2, line_generator_ip1(x)-2, "{:.3f} dBm".format(x), **font_style["annotation"])
#                    break
#    return line_ip1, curve_ip1, line_ip3, curve_ip3

fig = None

ax = None
retta_ip1 = None
curve_ip1 = None
retta_ip3 = None
curve_ip3 = None
ip1 = None
ip3 = None

line_ani = None

if __name__ == "__main__":
    sys.exit(calculate_all_IP1(ip1_filename, graph_title=None))
