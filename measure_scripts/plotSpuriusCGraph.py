'''
Created on 08/mag/2016

@author: sabah
'''

# Convertion Loss

# Compression Point

# Harmonic Intermodulation Products
# Harmonic 1000MHz (LO = 5000MHz; RF = 3000MHz)


import subprocess
import time
import csv
import numpy as np
from scipy.interpolate import UnivariateSpline
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.pyplot import gca
from matplotlib.colors import colorConverter
# from mpl_toolkits.mplot3d import axes3d
import sys
import operator

from utility import create_csv, create_csv, unit_class, return_now_postfix
import os.path
from csvutility import frequency_LO_index, unit_LO_index, power_LO_index, is_LO_calibrated_index, frequency_RF_index, \
    unit_RF_index, power_RF_index, is_RF_calibrated_index, frequency_IF_index, unit_IF_index, power_IF_index, \
    is_IF_calibrated_index, n_LO_index, m_RF_index, conversion_loss, csv_file_header

from graphutility import styles, linecolors, markerstyles, styles_generic_XY, openGenericTxtfile, openSpuriusfile, \
    splitSpuriusCfiletablevalueDict, order_and_group_data
from measure_scripts.graphutility import graph_types, generic_graph_types
from plotXYgraph import plot_XY_Single

unit = unit_class()

final = []
final2 = []


def convert_x_y_axes_generic(data_table, graph_x_unit, x_index, graph_y_unit, y_index):
    result_eval = [[] for x in range(len(data_table))]
    k = 0
    for group in data_table:
        j = 0
        for row in group:
            new_row = [row[0]]
            # to generilize !!!!
            new_row.append(unit.unit_conversion(row[x_index], unit.Hz, graph_x_unit))
            new_row.append(row[y_index])
            result_eval[k].append(new_row)
            j += 1
        k += 1
    return result_eval


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
                       graph_x,
                       graph_y,
                       graph_z,
                       SD_LO_Frequency,
                       SD_LO_Level,
                       SD_RF_Level,
                       IF_Frequency_selected=1000,
                       font_style=None):
    """
    data = dict{(n, m, Freq_LO, Level_LO, Level_RF): [Freq_unit_LO, Calib_LO, Freq_RF, Freq_unit_RF, Calib_RF, Freq_IF, Freq_unit_IF, Level_IF, Calib_IF, -(Level_RF - Level_IF)]}
    """

    data_table, data_file_directory, graph_group_index, x_index, y_index, z_index, legend_index = order_and_group_data(
        data_file_name,
        graph_type,
        SD_LO_Frequency=SD_LO_Frequency,
        SD_LO_Level=SD_LO_Level,
        SD_RF_Level=SD_RF_Level,
        SD_IF_Min_Level=graph_z.min,
        IF_Frequency_selected=IF_Frequency_selected)

    # if graph_type in graph_types.values():
    #    data_table = convert_x_y_axes(data_table, graph_x.unit, x_index, graph_y.unit, y_index)
    # elif graph_type in generic_graph_types.values():
    #    data_table = convert_x_y_axes_generic(data_table, graph_x.unit, x_index, graph_y.unit, y_index)

    data_file_directory = os.path.join(data_file_directory, "_".join([graph_type, return_now_postfix()]))
    if not os.path.exists(data_file_directory):
        try:
            os.makedirs(data_file_directory)
        except:
            print("Error creating " + data_file_directory)
            return 0
    group_for_SD = []
    group_for_GG = []
    for row_grouped in data_table:
        plot_this = False
        graph_type = str(graph_type)
        if (graph_type == "RF" or graph_type == "LO") and (
                        row_grouped[0][n_LO_index] == 1 or row_grouped[0][n_LO_index] == -1) and (
                        row_grouped[0][m_RF_index] == 1 or row_grouped[0][m_RF_index] == -1):
            plot_this = True
        elif graph_type == "SP" and row_grouped[0][n_LO_index] != 1 and row_grouped[0][n_LO_index] != -1 and \
                        row_grouped[0][m_RF_index] != 1 and row_grouped[0][m_RF_index] != -1 and row_grouped[0][
            frequency_IF_index] == IF_Frequency_selected:
            plot_this = True
        elif graph_type == "IP1" and row_grouped[0][n_LO_index] == 1 and row_grouped[0][
            frequency_IF_index] == IF_Frequency_selected:
            plot_this = True
        elif graph_type == "SD" and row_grouped[0][n_LO_index] != 1 and row_grouped[0][n_LO_index] != -1 and \
                        row_grouped[0][m_RF_index] != 1 and row_grouped[0][m_RF_index] != -1:
            group_for_SD.append(row_grouped[:])
            plot_this = False
        elif graph_type == "GG":
            group_for_GG = row_grouped[:]
            plot_this = False
        elif graph_type == "NN":
            group_for_GG = row_grouped[:]
            plot_this = False
        if plot_this:
            if graph_type == "IP1":
                pass
            else:
                plot_spurius_C(table_value=row_grouped,
                               graph_group_index=graph_group_index,
                               x_index=x_index,
                               y_index=y_index,
                               z_index=z_index,
                               legend_index=legend_index,
                               graph_title=graph_title,
                               graph_type=graph_type,
                               graph_x=graph_x,
                               graph_y=graph_y,
                               graph_z=graph_z,
                               data_file_directory=data_file_directory,
                               font_style=font_style)
    if len(group_for_SD) > 0:
        plot_spurius_C(table_value=group_for_SD,
                       graph_group_index=graph_group_index,
                       x_index=x_index,
                       y_index=y_index,
                       z_index=z_index,
                       legend_index=legend_index,
                       graph_title=graph_title,
                       graph_type=graph_type,
                       graph_x=graph_x,
                       graph_y=graph_y,
                       graph_z=graph_z,
                       data_file_directory=data_file_directory,
                       font_style=font_style)
    if len(group_for_GG) > 0:
        plot_XY_Single(fig, table_value=group_for_GG,
                       graph_group_index=graph_group_index,
                       x_index=x_index,
                       y_index=y_index,
                       z_index=z_index,
                       legend_index=legend_index,
                       legend_title="",
                       graph_title=graph_title,
                       graph_type=graph_type,
                       graph_x=graph_x,
                       graph_y=graph_y,
                       graph_z=graph_z,
                       data_file_directory=data_file_directory,
                       font_style=font_style)
    return data_file_directory


def plot_spurius_C(table_value,
                   graph_group_index,
                   x_index,
                   y_index,
                   z_index,
                   legend_index,
                   graph_title,
                   graph_type,
                   graph_x,
                   graph_y,
                   graph_z,
                   data_file_directory="",
                   font_style=None):
    fig = plt.figure()
    # for i in range (1, 13):
    #    fig.add_subplot(4, 3, i)
    plot_spurius_Single(fig, table_value=table_value,
                        graph_group_index=graph_group_index,
                        x_index=x_index,
                        y_index=y_index,
                        z_index=z_index,
                        legend_index=legend_index,
                        graph_title=graph_title,
                        graph_type=graph_type,
                        graph_x=graph_x,
                        graph_y=graph_y,
                        graph_z=graph_z,
                        data_file_directory=data_file_directory,
                        font_style=font_style)


def filter_spurius_on_harmonic(data_rows):
    result = []
    for row in data_rows:
        # exclude the spurius with the same frequency of intermodulation of LO and RF
        freq_LO = row[frequency_LO_index]
        freq_RF = row[frequency_RF_index]
        freq_IF = row[frequency_IF_index]
        n = row[n_LO_index]
        m = row[m_RF_index]
        spurius_freq = freq_IF
        harmonic_freq = [1 * freq_LO - 1 * freq_RF, 1 * freq_LO + 1 * freq_RF, -1 * freq_LO - 1 * freq_RF,
                         -1 * freq_LO + 1 * freq_RF]

        if not spurius_freq in harmonic_freq:
            result.append(row[:])
        else:
            print(row)
    return result


def plot_3d_distribution(fig,
                         data_table,
                         x_index,
                         y_index,
                         z_index,
                         legend_index,
                         graph_title,
                         graph_x,
                         graph_y,
                         graph_z,
                         data_file_directory,
                         font_style):
    bar_with = 5e+7  # Hz
    bar_with_unit = unit.Hz

    ax = fig.add_subplot(111, projection='3d')

    front_back_position = [x * 10 for x in
                           range(0, len(data_table))]  # same number of y ticks as list of value for couple n,m
    color = ['r', 'g', 'b', 'y']
    yticklabels = [str(r[0][n_LO_index]) + ", " + str(r[0][m_RF_index]) for r in data_table]
    ax.set_yticks(front_back_position)
    ax.set_yticklabels(yticklabels, **font_style["axislegend"])
    color_index = 0
    fb_index = 0
    sort_data = [frequency_IF_index]
    for row_group in data_table:
        tmp_row_group = sorted(row_group, key=operator.itemgetter(*sort_data))
        tmp_row_group = filter_spurius_on_harmonic(tmp_row_group)
        freq = [unit.convertion_from_base(r[frequency_IF_index], graph_x.unit) for r in tmp_row_group]
        level = [r[power_IF_index] - graph_z.min for r in tmp_row_group]
        freq_result = []
        level_result = []
        for f_index in range(len(freq)):
            if freq[f_index] >= graph_x.min and freq[f_index] <= graph_x.max:
                freq_result.append(freq[f_index])
                level_result.append(level[f_index])
        color_index += 1
        if color_index >= len(color):
            color_index = 0
        ax.bar(freq_result, level_result, zs=front_back_position[fb_index], color=color[color_index],
               width=unit.unit_conversion(bar_with, bar_with_unit, graph_x.unit), zdir='y', alpha=0.8)
        fb_index += 1

    plt.suptitle("Spuriuos Distribution", **font_style["suptitle"])
    plt.title(graph_title, **font_style["title"])
    ax.set_xlabel(graph_x.label, **font_style["axislegend"])
    ax.set_ylabel(graph_y.label, **font_style["axislegend"])
    ax.set_zlabel(graph_z.label, **font_style["axislegend"])

    ax.set_xlim3d(graph_x.from_base().min, graph_x.from_base().max)
    ax.set_xticks(graph_x.from_base().return_arange())
    ax.set_ylim3d(0, front_back_position[-1])
    new_zlimit = (0, graph_z.from_base().max - graph_z.from_base().min)
    ax.set_zlim3d(new_zlimit)
    zticks = np.arange(new_zlimit[0], new_zlimit[1], graph_z.from_base().step)
    ax.set_zticks(zticks)
    fig.canvas.draw()
    zticklabels = ax.get_zticklabels()
    new_zticklabels = [str(eval(zt.get_text()) + graph_z.from_base().min) for zt in zticklabels]
    ax.set_zticklabels(new_zticklabels, **font_style["axisticks"])
    # plt.gca().invert_zaxis()
    plt.show()


def plot_spurius_Single(fig, table_value,
                        graph_group_index,
                        x_index,
                        y_index,
                        z_index,
                        legend_index,
                        graph_title,
                        graph_type,
                        graph_x,
                        graph_y,
                        graph_z,
                        data_file_directory="",
                        font_style=None):
    """

    """
    spl = []

    filter_1 = False

    x_y_offset = 0
    graph_type = str(graph_type)
    if graph_type == "LO":
        if not graph_x.label:
            graph_x.label = 'IF Freq (' + unit.return_unit_str(graph_x.unit) + ')'
        else:
            graph_x.label = graph_x.label.format(unit=unit.return_unit_str(graph_x.unit))
        if not graph_y.label:
            graph_y.label = 'IF Power Loss ({unit})'.format(unit=unit.return_unit_str(graph_y.unit))
        if not graph_title:
            graph_sup_title = "Conversion Loss"
        else:
            graph_sup_title = graph_title
        graph_title = "LO " + unit.return_human_readable_str(
            table_value[0][frequency_LO_index]) + " - RF " + unit.return_human_readable_str(
            table_value[0][power_RF_index], unit.dBm)
        legend_title = "LO Power"
    elif graph_type == "RF":
        if not graph_x.label:
            graph_x.label = 'RF Power ({unit})'.format(unit=unit.return_unit_str(graph_x.unit))
        else:
            graph_x.label = graph_x.label.format(unit=unit.return_unit_str(graph_x.unit))
        if not graph_y.label:
            graph_y.label = "IF Power ({unit})".format(unit=unit.return_unit_str(graph_y.unit))
        if not graph_title:
            graph_sup_title = "Compression Point"

        else:
            graph_sup_title = graph_title
        graph_title = "LO " + unit.return_human_readable_str(
            table_value[0][frequency_LO_index]) + " - RF " + unit.return_human_readable_str(
            table_value[0][frequency_RF_index])
        legend_title = "LO Power"
    elif graph_type == "SP":
        if not graph_x.label:
            graph_x.label = 'RF Power ({unit})'.format(unit=unit.return_unit_str(graph_x.unit))
        else:
            graph_x.label = graph_x.label.format(unit=unit.return_unit_str(graph_x.unit))
        if not graph_y.label:
            graph_y.label = "IF Power ({unit})".format(unit=unit.return_unit_str(graph_y.unit))
        if not graph_title:
            graph_sup_title = "Harmonic Intermodulation Products\n"
        else:
            graph_sup_title = graph_title
        graph_title = "IF " + unit.return_human_readable_str(
            table_value[0][frequency_IF_index]) + " (LO " + unit.return_human_readable_str(
            table_value[0][frequency_LO_index]) + " (" + str(
            table_value[0][n_LO_index]) + ")" + "; RF " + unit.return_human_readable_str(
            table_value[0][frequency_RF_index]) + " (" + str(table_value[0][m_RF_index]) + "))"
        filter_1 = True
        legend_title = "LO Power"
    elif graph_type == "SD":
        if not graph_x.label:
            graph_x.label = 'IF Freq ({unit})'.format(unit=unit.return_unit_str(graph_x.unit))
        else:
            graph_x.label = graph_x.label.format(unit=unit.return_unit_str(graph_x.unit))
        if not graph_y.label:
            graph_y.label = "Intermodulation"
        if not graph_z.label:
            graph_z.label = "IF Power ({unit})".format(unit=unit.return_unit_str(graph_z.unit))
        if not graph_title:
            graph_sup_title = "Spurious Distribution"
        filter_1 = True
        graph_title = "LO " + unit.return_human_readable_str(
            table_value[0][0][frequency_LO_index]) + " " + unit.return_human_readable_str(
            table_value[0][0][power_LO_index], unit.dBm) + " - RF " + unit.return_human_readable_str(
            table_value[0][0][power_RF_index], unit.dBm)
        legend_title = "Power LO"

    # split by RF_level or LO_level
    if str(graph_type) != "SD":
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
        plot_3d_distribution(fig, table_value,
                             x_index,
                             y_index,
                             z_index,
                             legend_index,
                             graph_title,
                             graph_x,
                             graph_y,
                             graph_z,
                             data_file_directory,
                             font_style=font_style)
    else:

        ax = plt.axes(xlim=(graph_x.from_base().min, graph_x.from_base().max),
                      ylim=(graph_y.from_base().min, graph_y.from_base().max))
        plt.xticks(graph_x.return_ticks_range(2))
        plt.yticks(graph_y.return_ticks_range(2))

        a = gca()
        a.set_xticklabels(a.get_xticks(), **font_style["axisticks"])
        a.set_yticklabels(a.get_yticks(), **font_style["axisticks"])

        plt.xlabel(graph_x.label, **font_style["axislegend"])
        plt.ylabel(graph_y.label, **font_style["axislegend"])
        plt.title(graph_title, **font_style["title"])
        plt.suptitle(graph_sup_title, linespacing=2, **font_style["suptitle"])
        plt.grid(True)

        # Put a legend to the right of the current axis
        mn = 1000
        mx = -1000
        s = 0  # style index
        for row in result:
            if filter_1 and (row[0][n_LO_index] == 1 or row[0][n_LO_index] == -1 or row[0][m_RF_index] == 1 or row[0][
                m_RF_index] == -1):
                continue
            if s == len(styles):
                s = 0
            label = ""
            for l in legend_index:
                tmp_unit = unit.return_unit_str(row[0][l[1]]) or "dBm"
                n_m = ""
                if l[1] > 0:
                    n_m = row[0][l[3]]
                label += l[2] + " " + str(row[0][l[0]]) + " " + tmp_unit + " " + str(n_m) + "\n"
            label = label[0:-1]
            x = [unit.convertion_from_base(x[x_index], graph_x.unit) for x in row]
            y = [unit.convertion_from_base(y[y_index], graph_y.unit) for y in row]

            mn = graph_y.from_base().min
            mx = graph_y.from_base().max

            ax.set_ylim([mn - x_y_offset, mx + x_y_offset])
            plt.xticks(graph_x.return_ticks_range(2))
            plt.yticks(graph_y.return_ticks_range(2))
            a.set_xticklabels(a.get_xticks(), **font_style["axisticks"])
            a.set_yticklabels(a.get_yticks(), **font_style["axisticks"])
            markercolor = tuple(list(colorConverter.to_rgb(styles[s][1])) + [0.4])
            ax.plot(np.array(x), np.array(y), label=label, linestyle='-', marker=styles[s][0], color=styles[s][1],
                    markerfacecolor=markercolor)
            s += 1

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.7, box.height])
        legend_object = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=legend_title)
        # legend_object.set_title(title = legend_title, prop = csfont_title)
        # legend_object.get_title().set_fontsize(csfont_title["fontsize"]) #legend 'Title' fontsize
        # legend_object.get_title().set_fontname(csfont_title["fontname"])
        plt.setp(plt.gca().get_legend().get_title(), **font_style["legendtitle"])
        plt.setp(plt.gca().get_legend().get_texts(), **font_style["legendlines"])  # legend 'list' fontsize

        # curves_data.append(np.array([t, [spl[-1](x) for x in t]]))
        # len(curves_data[0][0])
        # line_ani = animation.FuncAnimation(fig, update_sprius_line, 100,  fargs=(curves_data, curves, spl), interval=interval, blit=False, repeat=False)
        # plt.show()

        save_file_name = os.path.join(data_file_directory, "Graph_" + graph_title)
        plt.savefig(save_file_name + ".png", dpi=200)
        plt.savefig(save_file_name + ".svg")


fig = None
ax = None
curve = None


# if __name__ == "__main__":
#    sys.exit(calculate_all_IP1(ip1_filename, graph_title = None))
