'''
Created on 28/mag/2016

@author: sabah
'''

csfont_suptitle = {'fontname':'Times New Roman', "fontsize":"20"}
csfont_title = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_legendtitle = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_legendlines = {'fontname':'Times New Roman', "fontsize":"10"}
csfont_axislegend = {'fontname':'Times New Roman', "fontsize":"14"}
csfont_axisticks = {'fontname':'Times New Roman', "fontsize":"10"}
csfont_annotation = {'fontname':'Times New Roman', "fontsize":"10"}


styles = [(None, "b"), (None, "g"), (None, "r"), (None, "c"), (None, "m"), (None, "y"), (None, "k"),
          ("o", "b"), ("o", "g"), ("o", "r"), ("o", "c"), ("o", "m"), ("o", "y"), ("o", "k"),
          ("v", "b"), ("v", "g"), ("v", "r"), ("v", "c"), ("v", "m"), ("v", "y"), ("v", "k"),
          ("s", "b"), ("s", "g"), ("s", "r"), ("s", "c"), ("s", "m"), ("s", "y"), ("s", "k")]

linecolors = ["b", "g", "r", "c", "m", "y", "k"]
markerstyles = [None, "o", "v", "s", ]

class axis_range():
    def __init__(self, a_max, a_min, a_step, a_unit):
        self.max = a_max
        self.min = a_min
        self.step = a_step
        self.unit = a_unit