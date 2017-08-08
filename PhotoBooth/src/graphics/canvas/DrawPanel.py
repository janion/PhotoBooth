'''
Created on 2 Aug 2017

@author: Janion
'''

import wx


class DrawPanel(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.BufferBmp = wx.EmptyBitmap(0, 0)
        self.widgets = []

        self.Bind(wx.EVT_SIZE, self.redraw)
        self.Bind(wx.EVT_PAINT, self._onPaint)

        self.Bind(wx.EVT_LEFT_DOWN, self._mouseDown)
        self.Bind(wx.EVT_LEFT_UP, self._mouseUp)
        
    def redraw(self, event=None):
        self.BufferBmp = wx.EmptyBitmap(self.Size[0], self.Size[1])
        memdc = wx.MemoryDC()
        memdc.SelectObject(self.BufferBmp)
        self._drawWidgets(memdc)
        self.Refresh()

    def _onPaint(self, event):
        dc = wx.PaintDC(self)
        dc.BeginDrawing()
        dc.DrawBitmap(self.BufferBmp, 0, 0, True)
        dc.EndDrawing()

    def _drawWidgets(self, dc):
        dc.BeginDrawing()

        for widget in self.widgets:
            widget.draw(dc)

        dc.EndDrawing()

    def _mouseDown(self, event):
        dc = wx.MemoryDC(self.BufferBmp)
        for widget in list(reversed(self.widgets)):
            if widget.mouseDown(event, dc):
                break
        self.redraw()
        event.Skip()

    def _mouseUp(self, event):
        dc = wx.MemoryDC(self.BufferBmp)
        for widget in list(reversed(self.widgets)):
            if widget.mouseUp(event, dc):
                break
        self.redraw()
        event.Skip()

    def addWidget(self, widget):
        self.widgets.append(widget)

    def removeWidget(self, widget):
        self.widgets.remove(widget)
