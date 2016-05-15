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

from utility import save_data, save_settings, create_csv, unit_class, return_now_postfix
import os.path


unit = unit_class()

ip1_filename = "misura IP1 ZVA213_3.csv"

csfont = {'fontname':'Times New Roman'}

final = []
final2 = []

def openIP1file(filename):
    #open the output file and return the table of value without header
    #the table format is: [frequency, power_input, power_calibrated, is_calibrated, attenuation, power output]
    #return empty table if error
    result = []
    try:
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                result.append(row)
        #remove separator and header take unit value
        return result[2:], unit.return_unit( result[1][0].split("(")[1].split(")")[0]), os.path.dirname(filename)
    except:
        return [], unit.MHz, None
    

def splitIP1filetablevalue(table_value):
    """
    build a dictionary of values from table extracted from IP1 file measure
    the stucture is dict{frequency: [power_level_input, power_level_output, calibration_info]}
    """
    file_measures = {}
    power_input_curve = []
    power_linear_last_index = 0
    power_output_curve = []
    
    for i in table_value:
        current_frequency = eval(i[0].replace(",", "."))
        if current_frequency in file_measures:
            file_measures[current_frequency].append([eval(i[1].replace(",", ".")),
                                                                              eval(i[5].replace(",", ".")),
                                                                              i[3]])
        else:
            file_measures[current_frequency] = {}
            file_measures[current_frequency] = [[eval(i[1].replace(",", ".")),
                                                                              eval(i[5].replace(",", ".")),
                                                                              i[3]]]
        
    return file_measures
        

        

def calculate_all_IP1(data_file_name, graph_title, graph_x_label, graph_x_min, graph_x_max, graph_x_step, graph_y_label, graph_y_min, graph_y_max, graph_y_step, animated):
    file_table_result, unit_value, data_file_directory = openIP1file(data_file_name)
    
    for k, v in splitIP1filetablevalue(file_table_result).iteritems():
        calculateIP1(k, unit_value, sorted(v, key=lambda x: x[0]), graph_title, graph_x_label, graph_x_min, graph_x_max, graph_x_step, graph_y_label, graph_y_min, graph_y_max, graph_y_step, data_file_directory = data_file_directory, animated = animated) #return list of value sorted by power_level_input field. Used to manage different measure for different attenuations


def calculateIP1(frequency, frequency_unit_value, table_value, graph_title, graph_x_label = 'Input Power(dBm)', graph_x_min = -40, graph_x_max = 10, graph_x_step = 5, graph_y_label = 'Output Power(dBm)', graph_y_min = -30, graph_y_max = 20, graph_y_step = 5, return_IP1 = False, data_file_directory = "", animated = False):
    
    power_input_curve = []
    power_linear_last_index = 0
    power_output_curve = []
    calibrated = True
    IP1_x = None
    
    
    
    start_power = table_value[0][0]
    for i in table_value:
        if i[2] != "CAL":
            calibrated = False
        power_input_curve.append(i[0])
        power_output_curve.append(i[1])
        if abs(power_input_curve[-1] - start_power) <= 5:
            power_linear_last_index += 1
    
    x_curve = np.array(power_input_curve)
    y_curve = np.array(power_output_curve)
    coefficient_linear = np.polyfit(x_curve[:power_linear_last_index], y_curve[:power_linear_last_index], 1)
    p_linear = np.poly1d(coefficient_linear)
    spl = UnivariateSpline(x_curve, y_curve, s=0)
    t = x_curve
    s_linear = [p_linear(x) for x in t]
    line_ani = None
    fig = plt.figure()
    
    if graph_x_min is None:
        graph_x_min = -40
    if graph_x_max is None:
        graph_x_max = 10
    if graph_x_step is None:
        graph_x_step = 5
    if graph_y_min is None:
        graph_y_min = -30
    if graph_y_max is None:
        graph_y_max = 20
    if graph_y_step is None:
        graph_y_step = 5
    if animated:
        interval = 1
    else:
        interval = 0
    
    
    ax = plt.axes(xlim=(graph_x_min, graph_x_max), ylim=(graph_y_min, graph_y_max))
    ip1, = ax.plot([], [], "ro")
    retta, = ax.plot([], [], "g--")
    #ax2 = plt.axes(xlim=(-40, 10), ylim=(-30, 20))
    curve, = ax.plot([], [], "r-")
    #ax3 = plt.axes(xlim=(-40, 10), ylim=(-30, 20))
    
    plt.xticks(np.arange(graph_x_min, graph_x_max +1, graph_x_step))
    plt.yticks(np.arange(graph_y_min, graph_y_max +1, graph_y_step))
    
    
    a = gca()
    a.set_xticklabels(a.get_xticks(), **csfont)
    a.set_yticklabels(a.get_yticks(), **csfont)
    
    if not graph_x_label:
        graph_x_label = 'Input Power(dBm)'
    plt.xlabel(graph_x_label, **csfont)
    if not graph_y_label:
        graph_y_label = "Output Power (dBm)"
    plt.ylabel(graph_y_label, **csfont)
    if not graph_title:
        graph_title = "Freq. " + str(frequency) + " " + unit.return_unit_str(frequency_unit_value) + " Cable Cal." + str(calibrated)
    plt.title(graph_title, **csfont)
    plt.grid(True)
    lower = 0
    upper = len(t)
    middle = 0
    if return_IP1:
        for i in range(0, int(np.log2(len(t)))-1):
            middle = lower + int((upper-lower) /2)
            if abs(p_linear(t[middle]) - spl(t[middle]))<0.8:
                lower = middle
            else:
                upper = middle
        #for x in np.arange(t[0], t[-1], 0.0001):
        for x in np.arange(t[middle], t[-1], 0.0001):
            if abs(p_linear(x) - spl(x))>=1:
                #IP1 found
                IP1_x = x
                #plt.plot(x, spl(x), "ro")
                #plt.text(x+0.2, spl(x)+0.2, "{}".format(x))
                break
    
    curve_data = np.array([t, [spl(x) for x in t]])
    line_data = np.array([t, s_linear])
    line_ani = animation.FuncAnimation(fig, update_line, len(line_data[0]),  fargs=(line_data, retta, p_linear, curve_data, curve, spl, ip1), interval=interval, blit=False, repeat=False)
    plt.show()
    fig.savefig(os.path.join(data_file_directory, "Freq_" + str(frequency) + unit.return_unit_str(frequency_unit_value) + "_Cable_Cal" + str(calibrated) + "_" + return_now_postfix() + ".png"))
    return IP1_x
 
def update_line(num, line_data, line, line_generator, curve_data, curve, curve_generator, ip1):
    #line.set_data(data[0, :num], data[1,:num])
    if len(line.get_xdata()) == len(line_data[0]):
        return line, curve
    line.set_xdata(np.append(line.get_xdata(), line_data[0][num]))
    line.set_ydata(np.append(line.get_ydata(), line_data[1][num]))
    #line2.set_data(data2[0, :num], data2[1, :num])
    curve.set_xdata(np.append(curve.get_xdata(), curve_data[0][num]))
    curve.set_ydata(np.append(curve.get_ydata(), curve_data[1][num]))
    if len(ip1.get_xdata())==0:
        if abs(line_data[1][num] - curve_data[1][num]) > 1.0:
            for x in np.arange(curve_data[0][num-1], curve_data[0][num+1], 0.0001):
                if abs(line_generator(x) - curve_generator(x))>=1:
                    #IP1 found
                    ip1.set_xdata(np.append(ip1.get_xdata(), curve_data[0][num]))
                    ip1.set_ydata(np.append(ip1.get_ydata(), curve_data[1][num]))
                    plt.text(x+0.2, curve_generator(x)-2, "{:.3f} dBm".format(x), **csfont)
                    break
    return line, curve
 
 
 
#print "Prepare data and chart..."
#data = np.array(final)
#data2 = np.array(final2)
 
fig = None

#ax = plt.axes(xlim=(0, 2), ylim=(-2, 2))
#retta, = ax.plot([], [])
#ax2 = plt.axes(xlim=(0, 2), ylim=(-2, 2))
#curve, = ax2.plot([], [], "r")

ax = None
retta = None
curve = None
ip1 = None

# add subplot to chart
#ax = fig.add_subplot(111)
# first line is red
#retta, = ax.plot([], [], 'r-')
 
#ax2 = fig.add_subplot(111)
#and set line color to blue
#curve, = ax2.plot([], [], 'b-')
line_ani = None


if __name__ == "__main__":
    sys.exit(calculate_all_IP1(ip1_filename, graph_title = None))