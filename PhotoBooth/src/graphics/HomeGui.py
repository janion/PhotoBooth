'''
Created on 4 Jan 2017

@author: Janion
'''

import wx
from time import sleep
from threading import Thread

from src.graphics.camera.MockCamera import Camera

class Window(wx.Frame):

    TITLE = "PhotoBooth - %s"
    EFFECT_LABEL = "Effect\n(%s)"
    SCREEN_OFFSET_X = 24
    SCREEN_OFFSET_Y = 46
    SELECTED = (255, 200, 200)

    def __init__(self, parent, idd):
        wx.Frame.__init__(self, parent, idd)
        self.panel = wx.Panel(self, -1)

        self.takingPhoto = False
        self.setupCamera()
        self.SetTitle(self.TITLE % self.camera.getPhotoDirectory())
        
        self.label1 = wx.StaticText(self.panel, -1, label="", style=wx.ALIGN_CENTER)
        self.label2 = wx.StaticText(self.panel, -1, label="", style=wx.ALIGN_CENTER)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.AddStretchSpacer(1)
        topSizer.Add(self.label1, 1, wx.ALL|wx.EXPAND, 5)
        topSizer.AddStretchSpacer(50)
        topSizer.Add(self.label2, 1, wx.ALL|wx.EXPAND, 5)
        topSizer.AddStretchSpacer(5)

        self.goBtn = wx.Button(self.panel, -1, label="Go", size=(100, 100))
        self.effectBtn = wx.Button(self.panel, -1,
                                   label=self.EFFECT_LABEL %
                                   self.camera.getEffectName(),
                                   size=(100, 100),
                                   style=wx.ID_JUSTIFY_RIGHT
                                   )

        self.goBtn.SetBackgroundColour(self.SELECTED)
        self.goBtn.SetFocus()
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.AddStretchSpacer()
        bottomSizer.Add(self.goBtn, 0, wx.ALL|wx.EXPAND, 5)
        bottomSizer.AddStretchSpacer()
        bottomSizer.Add(self.effectBtn, 0, wx.ALL|wx.EXPAND, 5)
        bottomSizer.AddStretchSpacer()
        
        fullSizer = wx.BoxSizer(wx.VERTICAL)
        fullSizer.Add(topSizer, 0, wx.ALL|wx.EXPAND, 5)
        fullSizer.AddStretchSpacer()
        fullSizer.Add(bottomSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.panel.SetSizer(fullSizer)
        
        self.Maximize()
        self.setupMenu()

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_SIZE, self.onSizeOrMove)
        self.Bind(wx.EVT_MOVE, self.onSizeOrMove)

        self.goBtn.Bind(wx.EVT_BUTTON, self.takePhoto)
        self.goBtn.Bind(wx.EVT_CHAR, self.keyPress)

        self.effectBtn.Bind(wx.EVT_BUTTON, self.effect)
        self.effectBtn.Bind(wx.EVT_CHAR, self.keyPress)

################################################################################

    def setupCamera(self):
        self.camera = Camera()
        self.camera.startPreview(1000, 1000, 1280, 1024)
            
################################################################################
            
    def setupMenu(self):
        self.menuBar = wx.MenuBar()
        
        menu1 = wx.Menu()
        menu1.Append(101, "Set photo directory")
        menu1.AppendSeparator()
        menu1.Append(102, "Quit")
        self.menuBar.Append(menu1, "File")
        
        self.SetMenuBar(self.menuBar)
        
        self.Bind(wx.EVT_MENU, self.setPhotoDirectory, id=101)
        self.Bind(wx.EVT_MENU, self.onClose, id=102)
        
################################################################################

    def setPhotoDirectory(self, event):
        dlg = wx.DirDialog(self, message="Choose destination for photos", style=wx.DD_DEFAULT_STYLE)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            self.camera.setPhotoDirectory(dlg.GetPath())
            self.SetTitle(self.TITLE % self.camera.getPhotoDirectory())

        dlg.Destroy()

################################################################################

    def keyPress(self, event):
        if event.GetEventObject() == self.goBtn and event.GetUnicodeKey() == 316:
            self.effectBtn.SetFocus()
            self.effectBtn.SetBackgroundColour(self.SELECTED)
            self.goBtn.SetBackgroundColour(None)
        elif event.GetEventObject() == self.effectBtn and event.GetUnicodeKey() == 314:
            self.goBtn.SetFocus()
            self.goBtn.SetBackgroundColour(self.SELECTED)
            self.effectBtn.SetBackgroundColour(None)
        event.Skip()

################################################################################

    def onSizeOrMove(self, event):
        (resX, resY) = self.camera.getPreviewSize()
        if resX == 0 or resY == 0:
            return

        resRatio = float(resY) / resX

        [X, Y] = self.GetPosition()
        [width, height] = self.GetSize()
        x = (width/8) + X + self.SCREEN_OFFSET_X
        y = Y + self.SCREEN_OFFSET_Y
        newWidth = int(0.75 * width)

        self.camera.setPreview(x, y, newWidth, int(newWidth * resRatio))
#         self.fakeDisplay.SetSize((newWidth / 10, int(newWidth * resRatio) / 10))

#         [btnWidth, btnHeight] = self.goBtn.GetSize()
#         self.effectBtn.SetPosition(((((3 * width) / 2) - btnWidth) / 2, height - btnHeight - 50))
#         self.goBtn.SetPosition((((width / 2) - btnWidth) / 2, height - btnHeight - 50))
#         self.label1.SetPosition(((width - btnWidth) / 2, height - self.label1.GetSize()[1] - 10))

        self.label1.SetFont(wx.Font(height / 8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.label2.SetFont(wx.Font(height / 8, wx.SWISS, wx.NORMAL, wx.BOLD))

        event.Skip()

################################################################################

    def effect(self, event):
        self.camera.effect()
        self.effectBtn.SetLabel(self.EFFECT_LABEL % self.camera.getEffectName())

################################################################################

    def takePhoto(self, event):
        if not self.takingPhoto:
            self.takingPhoto = True
            photoThread = Thread(target=self.countdown)
            photoThread.start()

################################################################################

    def onClose(self, event):
        self.camera.stopPreview()
        event.Skip()

################################################################################

    def countdown(self):
        for x in xrange(5, 0, -1):
            wx.CallAfter(self.label1.SetLabel, str(x))
            wx.CallAfter(self.label2.SetLabel, str(x))
            sleep(1)
        wx.CallAfter(self.label1.SetLabel, "")
        wx.CallAfter(self.label2.SetLabel, "")

        self.camera.takePhoto()
        self.takingPhoto = False
