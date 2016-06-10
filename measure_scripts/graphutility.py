'''
Created on 28/mag/2016

@author: sabah
'''
from utility import unit_class
import numpy as np
from scriptutility import Frequency_Range



unit = unit_class()

csfont_suptitle = {'fontname':'Times New Roman', "fontsize":"20"}
csfont_title = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_legendtitle = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_legendlines = {'fontname':'Times New Roman', "fontsize":"10"}
csfont_axislegend = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_axisticks = {'fontname':'Times New Roman', "fontsize":"12"}
csfont_annotation = {'fontname':'Times New Roman', "fontsize":"12"}


styles = [("o", "b"), ("v", "g"), ("s", "r"), ("s", "c"), ("8", "m"), ("d", "y"), ("*", "k"),
          ("o", "b"), ("o", "g"), ("o", "r"), ("o", "c"), ("o", "m"), ("o", "y"), ("o", "k"),
          ("v", "b"), ("v", "g"), ("v", "r"), ("v", "c"), ("v", "m"), ("v", "y"), ("v", "k"),
          ("s", "b"), ("s", "g"), ("s", "r"), ("s", "c"), ("s", "m"), ("s", "y"), ("s", "k")]

styles_generic_XY = [(None, "b"), (None, "g"), (None, "r"), (None, "c"), (None, "m"), (None, "y"), (None, "k")]

linecolors = ["b", "g", "r", "c", "m", "y", "k"]
markerstyles = [None, "o", "v", "s", ]

generic_graph_types = {"Generic Graph" : "GG"}

graph_types = {"Conversion Loss" : "LO", "Compression point" : "RF", "Harmonic Intermodulation Products" : "SP", "Spurious Distribution" : "SD"}

        
class Graph_Axis_Range(Frequency_Range):
    def __init__(self, a_min, a_max, a_step, a_unit, a_label):
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
        
    def return_ticks_range(self, round_value = 2):
        return [round(x, 2) for x in np.arange(self.min, self.max + self.step, self.step)]