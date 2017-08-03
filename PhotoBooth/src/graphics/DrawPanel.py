'''
Created on 2 Aug 2017

@author: Janion
'''

import wx


class DrawPanel(wx.Panel):
    
    def __init__(self, parent, drawFun):
        wx.Panel.__init__(self, parent, -1)
        self.BufferBmp = None

        self.drawFun = drawFun
        self.Bind(wx.EVT_SIZE, self.redraw)
        self.Bind(wx.EVT_PAINT, self.onPaint)
        
    def redraw(self, event=None):
        self.BufferBmp = wx.EmptyBitmap(self.Size[0], self.Size[1])
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.BufferBmp)
        self.drawFun(memdc)
        self.Refresh()

    def onPaint(self, evt):
        dc = wx.PaintDC(self)
        dc.BeginDrawing()
        dc.DrawBitmap(self.BufferBmp, 0, 0, True)
        dc.EndDrawing()
