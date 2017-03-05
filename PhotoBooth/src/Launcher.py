'''
Created on 9 Jul 2016

@author: Janion
'''

import wx
from graphics.HomeGui import Window

if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1)
    fr.Show()
    app.MainLoop()
