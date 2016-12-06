'''
Created on 13/mag/2016

@author: sabah
'''

import measure_scripts.tscpy as tscp
from utility import unit_class, return_now_postfix
import time
import datetime
from debug import TSC_class
from matplotlib.pyplot import figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

unit = unit_class()

csfont = {'fontname': 'Times New Roman'}

if "TSC" not in globals():
    # print("TSC not defined")
    TSC = TSC_class()
    TSC_delay = 0
else:
    TSC_delay = 1

TSC_collecting_delay = 1
result_file_name = "C:\\Users\\Labele\\Desktop\\Spurius\\LO_cal"

fig = None


def TSC_measure(TSC, TSC_collecting_delay=TSC_collecting_delay, result_file_name=result_file_name, TSC_plot_adev=False,
                createprogressdialog=None):
    # wait for TSC_collecting_delay minutes
    dialog = createprogressdialog
    for count in range(0, int(TSC_collecting_delay * 60)):
        if not createprogressdialog is None:
            import wx
            wx.MicroSleep(1000)
            message = "Collecting..."
            newvalue = int(float(count) / (TSC_collecting_delay * 60) * 100)
            dialog.Update(newvalue, message)
    dialog.Destroy()

    TSC.save_on_csv(result_file_name)

    if TSC_plot_adev:
        plot_adev(TSC.get_adev(), result_file_name)
        # tscp.instruments.fig.show()


def plot_adev(adevs, result_file_name, tag='', tsc=None):
    fig = figure()
    fig.add_axes()
    ax = fig.gca()
    timestamp = str(datetime.datetime.now())

    for adev in adevs:
        ax.errorbar(adev['adev']['tau'], adev['adev']['adev'], xerr=None, yerr=adev['adev']['err'],
                    label="tau0 = {0}, neq bw = {1}".format(adev['TAU0'], adev['NEQBW']))
    ax.loglog()
    ax.grid(b=True, which='major', linestyle='--')
    ax.grid(b=True, which='mminor', linestyle=':')
    ax.legend()
    ax.set_xlabel('tau [s]', **csfont)
    ax.set_ylabel('Allan deviation', **csfont)
    at_str = '' if tsc == None else '@ ' + str(tsc.socket[0])
    ax.set_title('{0}TSC5120A {1}: Allan deviation data captured at {2}.'.format(tag, at_str, timestamp), **csfont)

    line_ani = None

    line_ani = animation.FuncAnimation(fig, update_line, 1, fargs=(ax, adevs,), interval=0, blit=False, repeat=False)
    plt.show()
    fig.savefig(os.path.join(result_file_name, "plot_" + return_now_postfix() + ".png"))
    fig.savefig(os.path.join(result_file_name, "plot_" + return_now_postfix() + ".svg"))
    fig.savefig(os.path.join(result_file_name, "plot_" + return_now_postfix() + ".eps"))
    # fig.savefig(os.path.join(result_file_name, "plot_" + return_now_postfix() + ".ps"))
    # return IP1_x


def update_line(num, ax, adevs):
    # line.set_data(data[0, :num], data[1,:num])
    return ax


fig = None

ax = None
retta = None
curve = None
ip1 = None

line_ani = None
