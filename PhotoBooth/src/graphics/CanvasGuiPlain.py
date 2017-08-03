'''
Created on 4 Jan 2017

@author: Janion
'''

import wx
from graphics.DrawPanel import DrawPanel


class Window(wx.Frame):
    
    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, title="Title here", size=(400, 300))
    
        # Initialize our various samples and add them to the notebook.
        self.canvas = DrawPanel(self, self.drawPolygon)
    
    def drawPolygon(self, dc):
        dc.BeginDrawing()
        
        bmp = wx.Bitmap("hubbleBackground2.jpg")
        dc.DrawBitmap(bmp, 0, 0)
        
        dc.SetTextForeground("WHITE")
        dc.SetFont(wx.Font(40, wx.wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        width, height = dc.GetTextExtent("Hello")
        
        dc.DrawText("Hello", self.canvas.Size[0] - width, self.canvas.Size[1] - height)
    
        dc.EndDrawing()

if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1)
    fr.Show()
    app.MainLoop()
