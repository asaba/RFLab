'''
Created on 07/giu/2016

@author: sabah
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import gca
from matplotlib.colors import colorConverter
# from mpl_toolkits.mplot3d import axes3d

from utility import create_csv, create_csv, unit_class, return_now_postfix
import os.path
from graphutility import styles, linecolors, markerstyles, styles_generic_XY

unit = unit_class()


def build_table_value_from_x_y(x_list, y_list):
    result = []
    for index in range(len(x_list)):
        result.append([x_list[index],
                       unit.Hz,
                       y_list[index],
                       "NO CAL",
                       0,
                       unit.Hz,
                       0,
                       "NO_CAL",
                       0,
                       unit.Hz,
                       0,
                       "NO CAL",
                       0,
                       0])
    return result


def plot_XY_Single(fig1, table_value,
                   graph_group_index,
                   x_index,
                   y_index,
                   z_index,
                   legend_index,
                   legend_title,
                   graph_title,
                   graph_type,
                   graph_x,
                   graph_y,
                   graph_z,
                   data_file_directory="",
                   line_style=styles_generic_XY,
                   save=True,
                   font_style=None):
    """

    """
    x_y_offset = 0

    graph_sup_title = graph_title

    last_group_index = tuple([table_value[0][index] for index in graph_group_index])
    result = [[table_value[0][:]]]
    for row in table_value[1:]:
        current_group_index = tuple([row[index] for index in graph_group_index])
        if current_group_index == last_group_index:
            result[-1].append(row[:])
        else:
            last_group_index = current_group_index
            result.append([row[:]])

    ax = plt.axes(xlim=(graph_x.min, graph_x.max), ylim=(graph_y.min, graph_y.max))

    plt.xlabel(graph_x.label.format(unit=unit.return_unit_str(graph_x.unit)), **font_style["axislegend"])
    plt.ylabel(graph_y.label, **font_style["axislegend"])
    # plt.title(graph_title, **csfont_title)
    plt.suptitle(graph_sup_title, linespacing=2, **font_style["suptitle"])
    plt.grid(True)

    mn = 1000
    mx = -1000
    s = 0  # style index
    for row in result:
        if s == len(line_style):
            s = 0
        label = ""
        for l in legend_index:
            if l[1] is None:
                tmp_unit = "dBm"
                n_m = ""
            elif l[1] == -1:
                tmp_unit = ""
                n_m = ""
            else:
                tmp_unit = unit.return_unit_str(row[0][l[1]])
                n_m = row[0][l[3]]
            label += l[2] + " " + str(row[0][l[0]]) + " " + tmp_unit + " " + str(n_m) + "\n"
        label = label[0:-1]
        x = [x[x_index] for x in row]
        y = [y[y_index] for y in row]

        mn = graph_y.min
        mx = graph_y.max

        ax.set_ylim([mn - x_y_offset, mx + x_y_offset])
        xtk = [round(tk_x, 2) for tk_x in np.arange(graph_x.min, graph_x.max + graph_x.step, graph_x.step)]
        plt.xticks(xtk)
        plt.yticks(graph_y.return_ticks_range(2))
        a = gca()
        xtk_labels = ["{0:.2f}".format(unit.convertion_from_base(tk, graph_x.unit)) for tk in a.get_xticks()]
        a.set_xticklabels(xtk_labels, **font_style["axisticks"])
        a.set_yticklabels(a.get_yticks(), **font_style["axisticks"])
        markercolor = tuple(list(colorConverter.to_rgb(line_style[s][1])) + [0.4])
        ax.plot(np.array(x), np.array(y), label=label, linestyle='-', marker=line_style[s][0], color=line_style[s][1],
                markerfacecolor=markercolor)
        s += 1

    if not (legend_title is None):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        legend_object = ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title=legend_title)
        plt.setp(plt.gca().get_legend().get_title(), **font_style["legendtitle"])
        plt.setp(plt.gca().get_legend().get_texts(), **font_style["legendlines"])  # legend 'list' fontsize

    if save:
        save_file_name = os.path.join(data_file_directory, "Graph_" + graph_title)
        plt.savefig(save_file_name + ".png", dpi=200)
        plt.savefig(save_file_name + ".svg")
        plt.savefig(save_file_name + ".eps")
    else:
        plt.show()


ax = None
curve = None
