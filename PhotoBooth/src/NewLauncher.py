'''
Created on 9 Jul 2016

@author: Janion
'''

import wx
from graphics.canvas.CanvasGui import Window
from physical.camera.Camera import Camera
from physical.triggers.MockPhysicalTriggers import PhysicalTriggers

if __name__ == '__main__':
    app = wx.App()
    camera = Camera()
    camera.startPreview(1000, 1000, 1280, 1024)

    fr = Window(None, -1, camera, PhysicalTriggers())
    fr.Show()
    app.MainLoop()
