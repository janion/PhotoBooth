'''
Created on 2 Aug 2017

@author: Janion
'''

import wx


class DrawPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.BufferBmp = None
        self.widgets = []

        self.Bind(wx.EVT_SIZE, self.redraw)
        self.Bind(wx.EVT_PAINT, self._onPaint)
        
    def redraw(self, event=None):
        self.BufferBmp = wx.EmptyBitmap(self.Size[0], self.Size[1])
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.BufferBmp)
        self._drawWidgets(memdc)
        self.Refresh()

    def addWidget(self, widget):
        self.widgets.append(widget)

    def removeWidget(self, widget):
        self.widgets.remove(widget)

    def _drawWidgets(self, dc):
        dc.BeginDrawing()

        for widget in self.widgets:
            widget.draw(dc)

        dc.EndDrawing()

    def _onPaint(self, event):
        dc = wx.PaintDC(self)
        dc.BeginDrawing()
        dc.DrawBitmap(self.BufferBmp, 0, 0, True)
        dc.EndDrawing()
