'''
Created on 04/gen/2016

@author: sabah
'''

import wx
import random

from graph import GraphFrame

class DataGen(object):
    """ A silly class that generates pseudo-random data for
        display in the plot.
    """
    def __init__(self, instrument, init=50):
        self.data = self.init = init
        
    def next(self):
        self._recalc_data()
        return self.data
    
    def _recalc_data(self):
        delta = random.uniform(-0.5, 0.5)
        r = random.random()

        if r > 0.9:
            self.data += delta * 15
        elif r > 0.8: 
            # attraction to the initial value
            delta += (0.5 if self.init > self.data else -0.5)
            self.data += delta
        else:
            self.data += delta

if __name__ == '__main__':
    app = wx.App()
    app.frame = GraphFrame(DataGen(None), 100)
    app.frame.Show()
    app.MainLoop()