'''
Created on 26/dic/2015

@author: sabah
'''

# import images
from taskframe import TaskFrame
import wx
import os

from guitabs_image import ImagePanelClass


class NotebookDemo(wx.Notebook):
    """
    Notebook class
    """

    # ----------------------------------------------------------------------
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=
        wx.BK_DEFAULT
                             )

        # Create and add the second tab
        self.tabimage = ImagePanelClass(self)
        self.AddPage(self.tabimage, "Example Image")


########################################################################
class ImageFrame(TaskFrame):
    """
    Frame that holds all other widgets
    """

    # ----------------------------------------------------------------------
    def __init__(self, image_path):
        """Constructor"""
        TaskFrame.__init__(self, NotebookDemo,
                           "Plots",
                           size=(800, 680),
                           start_button=False
                           )


# ----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    frame = ImageFrame()
    app.MainLoop()
