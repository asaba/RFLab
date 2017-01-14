'''
Created on 28/dic/2015

@author: sabah
'''

import wx
import os

from guiobjects import return_image


class ImagePanelClass(wx.Panel):
    def __init__(self, parent, image_path):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.sizer_image = return_image(self, image_path)
