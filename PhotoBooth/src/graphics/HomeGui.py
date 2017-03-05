'''
Created on 4 Jan 2017

@author: Janion
'''

import wx
from time import sleep, time
from threading import Thread

from src.graphics.camera.MockCamera import Camera

class Window(wx.Frame):

    TITLE = "PhotoBooth - %s"
    EFFECT_LABEL = "Effect\n(%s)"
    SCREEN_OFFSET_X = 24
    SCREEN_OFFSET_Y = 46
    FOCUS_COLOUR = (255, 200, 200)
    MODE_LABEL = "Mode\n(%s)"
    MODE_SINGLE = "Single"
    MODE_4_TILE = "4 Tile"
    MODE_VIDEO = "Video"
    MODES = [MODE_SINGLE, MODE_4_TILE, MODE_VIDEO]
    PHOTO_COUNTDOWN_TIME = 5
    VIDEO_MAX_LENGTH = 5

    def __init__(self, parent, idd):
        wx.Frame.__init__(self, parent, idd)
        self.panel = wx.Panel(self, -1)

        self.isTakingPhoto = False
        self.isRecording = False
        self.setupCamera()
        self.SetTitle(self.TITLE % self.camera.getPhotoDirectory())
        
        topSizer = self.createLabels()
        
        bottomSizer = self.createButtons()
        
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

################################################################################

    def createLabels(self):
        self.label1 = wx.StaticText(self.panel, -1, label="", style=wx.ALIGN_CENTER)
        self.label2 = wx.StaticText(self.panel, -1, label="", style=wx.ALIGN_CENTER)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.AddStretchSpacer(1)
        topSizer.Add(self.label1, 1, wx.ALL|wx.EXPAND, 5)
        topSizer.AddStretchSpacer(50)
        topSizer.Add(self.label2, 1, wx.ALL|wx.EXPAND, 5)
        topSizer.AddStretchSpacer(5)
        
        return topSizer

################################################################################

    def createButtons(self):
        self.goBtn = wx.Button(self.panel, -1, label="Go", size=(100, 100))
        self.effectBtn = wx.Button(self.panel, -1,
                                   label=self.EFFECT_LABEL %
                                   self.camera.getEffectName(),
                                   size=(100, 100)
                                   )
        self.mode = 0
        self.modeBtn = wx.Button(self.panel, -1,
                                   label=self.MODE_LABEL %
                                   self.MODES[self.mode],
                                   size=(100, 100)
                                   )

        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.AddStretchSpacer()
        bottomSizer.Add(self.modeBtn, 0, wx.ALL|wx.EXPAND, 5)
        bottomSizer.AddStretchSpacer()
        bottomSizer.Add(self.goBtn, 0, wx.ALL|wx.EXPAND, 5)
        bottomSizer.AddStretchSpacer()
        bottomSizer.Add(self.effectBtn, 0, wx.ALL|wx.EXPAND, 5)
        bottomSizer.AddStretchSpacer()
        
        # Mode button
        self.modeBtn.Bind(wx.EVT_SET_FOCUS, lambda event: self.modeBtn.SetBackgroundColour(self.FOCUS_COLOUR))
        self.modeBtn.Bind(wx.EVT_KILL_FOCUS, lambda event: self.modeBtn.SetBackgroundColour(None))
        # Go button
        self.goBtn.Bind(wx.EVT_SET_FOCUS, lambda event: self.goBtn.SetBackgroundColour(self.FOCUS_COLOUR))
        self.goBtn.Bind(wx.EVT_KILL_FOCUS, lambda event: self.goBtn.SetBackgroundColour(None))
        # Effect button
        self.effectBtn.Bind(wx.EVT_SET_FOCUS, lambda event: self.effectBtn.SetBackgroundColour(self.FOCUS_COLOUR))
        self.effectBtn.Bind(wx.EVT_KILL_FOCUS, lambda event: self.effectBtn.SetBackgroundColour(None))
        
        self.goBtn.SetFocus()
        
        self.modeBtn.Bind(wx.EVT_BUTTON, self.changeMode)
        self.goBtn.Bind(wx.EVT_BUTTON, self.doCameraAction)
        self.effectBtn.Bind(wx.EVT_BUTTON, self.changeEffect)
        
        return bottomSizer

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
        self.Bind(wx.EVT_MENU, self.close, id=102)
        
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

        self.label1.SetFont(wx.Font(height / 8, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.label2.SetFont(wx.Font(height / 8, wx.SWISS, wx.NORMAL, wx.BOLD))

        event.Skip()

################################################################################

    def changeEffect(self, event):
        self.camera.changeEffect()
        self.effectBtn.SetLabel(self.EFFECT_LABEL % self.camera.getEffectName())

################################################################################

    def changeMode(self, event):
        self.mode = (self.mode + 1) % len(self.MODES)
        self.modeBtn.SetLabel(self.MODE_LABEL % self.MODES[self.mode])

################################################################################

    def doCameraAction(self, event):
        if self.MODES[self.mode] == self.MODE_SINGLE and not self.isTakingPhoto:
            photoThread = Thread(target=self.countdownToSinglePhoto)
            photoThread.start()
        elif self.MODES[self.mode] == self.MODE_4_TILE:
            pass
        elif self.MODES[self.mode] == self.MODE_VIDEO:
            if not self.isRecording:
                self.isRecording = True
                # Start timer
                videoThread = Thread(target=self.countdownForVideo)
                videoThread.start()
            else:
                self.isRecording = False

################################################################################

    def close(self, event):
        self.Close()

################################################################################

    def onClose(self, event):
        self.camera.stopPreview()
        event.Skip()

################################################################################

    def countdownForVideo(self):
        self.modeBtn.Enable(False)
        self.camera.startRecording()
        startTime = time()
        
        wx.CallAfter(self.label1.SetForegroundColour, (255, 0, 0))
        wx.CallAfter(self.label2.SetForegroundColour, (255, 0, 0))
        for x in xrange(self.VIDEO_MAX_LENGTH, 0, -1):
            wx.CallAfter(self.label1.SetLabel, str(x))
            wx.CallAfter(self.label2.SetLabel, str(x))
            
            while(time() < startTime + 1 + (self.VIDEO_MAX_LENGTH - x)):
                if not self.isRecording:
                    # Reset labels
                    wx.CallAfter(self.label1.SetForegroundColour, None)
                    wx.CallAfter(self.label2.SetForegroundColour, None)
                    break;
                
        wx.CallAfter(self.label1.SetLabel, "")
        wx.CallAfter(self.label2.SetLabel, "")

        self.camera.stopRecording()
        self.isRecording = False
        self.modeBtn.Enable(True)

################################################################################

    def countdownToSinglePhoto(self):
        self.isTakingPhoto = True
        self.modeBtn.Enable(False)
        for x in xrange(self.PHOTO_COUNTDOWN_TIME, 0, -1):
            wx.CallAfter(self.label1.SetLabel, str(x))
            wx.CallAfter(self.label2.SetLabel, str(x))
            sleep(1)
        wx.CallAfter(self.label1.SetLabel, "")
        wx.CallAfter(self.label2.SetLabel, "")

        self.camera.doCameraAction()
        self.isTakingPhoto = False
        self.modeBtn.Enable(True)
