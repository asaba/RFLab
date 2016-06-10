'''
Created on 07/giu/2016

@author: sabah
'''

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import gca
from matplotlib.colors import colorConverter
#from mpl_toolkits.mplot3d import axes3d

from utility import create_csv, create_csv, unit_class, return_now_postfix
import os.path
from graphutility import styles, linecolors, markerstyles, csfont_axislegend, csfont_axisticks, csfont_legendlines, csfont_legendtitle, csfont_suptitle, csfont_title, styles_generic_XY

unit = unit_class()

def plot_XY_Single(fig, table_value, 
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
                   data_file_directory = "",
                   line_style = styles_generic_XY):
    """

    """
    x_y_offset = 0

    graph_sup_title = graph_title
    
    #last_group_index = tuple([table_value[0][index] for index in graph_group_index])
    #result = [table_value[0][:]]
    #for row in table_value[1:]:
    #    current_group_index = tuple([row[index] for index in graph_group_index])
    #    if current_group_index == last_group_index:
    #        result[-1].append(row[:])
    #    else:
    #        last_group_index = current_group_index
    #        result.append([row[:]])
            
            
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
    plt.xticks(graph_x.return_ticks_range(2))
    plt.yticks(graph_y.return_ticks_range(2))
    
    a = gca()
    a.set_xticklabels(a.get_xticks(), **csfont_axisticks)
    a.set_yticklabels(a.get_yticks(), **csfont_axisticks)
    
    
    
    plt.xlabel(graph_x.label.format(unit = unit.return_unit_str(graph_x.unit)), **csfont_axislegend)
    plt.ylabel(graph_y.label, **csfont_axislegend)
    #plt.title(graph_title, **csfont_title)
    plt.suptitle(graph_sup_title, linespacing = 2, **csfont_suptitle)
    plt.grid(True)

    mn = 1000
    mx = -1000
    s = 0 #style index
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
            
        ax.set_ylim([mn-x_y_offset, mx+x_y_offset])
        plt.xticks(graph_x.return_ticks_range(2))
        plt.yticks(graph_y.return_ticks_range(2))
        a.set_xticklabels(a.get_xticks(), **csfont_axisticks)
        a.set_yticklabels(a.get_yticks(), **csfont_axisticks)
        markercolor = tuple(list(colorConverter.to_rgb(line_style[s][1])) + [0.4])
        ax.plot(np.array(x), np.array(y), label=label, linestyle='-', marker=line_style[s][0], color=line_style[s][1], markerfacecolor=markercolor)
        s += 1
    
    if not (legend_title is None):
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        legend_object =  ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), title = legend_title)
        plt.setp(plt.gca().get_legend().get_title(), **csfont_legendtitle)
        plt.setp(plt.gca().get_legend().get_texts(), **csfont_legendlines) #legend 'list' fontsize
            
    
    save_file_name = os.path.join(data_file_directory, "Graph_" + graph_title)
    plt.savefig(save_file_name + ".png", dpi=200)
    plt.savefig(save_file_name + ".svg")
    
        

fig = None
ax = None
curve = None