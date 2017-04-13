'''
Created on 4 Jan 2017

@author: Janion
'''

import wx
from time import sleep, time
from threading import Thread

from src.physical.camera.MockCamera import Camera
from src.physical.triggers.MockPhysicalTriggers import PhysicalTriggers

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
    
    PHOTO_COUNTDOWN_TIME = 3
    PHOTO_SEQUENCE_COUNT = 4
    PHOTO_SEQUENCE_GAP_TIME = 1
    VIDEO_MAX_LENGTH = 30

    def __init__(self, parent, idd):
        wx.Frame.__init__(self, parent, idd)
        self.panel = wx.Panel(self, -1)

        self.isTakingPhoto = False
        self.isRecording = False
        self.setupCamera()
        self.SetTitle(self.TITLE % self.camera.getPhotoDirectory())
        physicalTriggers = PhysicalTriggers()
        physicalTriggers.start(self.changeMode, self.doCameraAction, self.changeEffectUp, self.changeEffectDown)
        
        topSizer = self.createLabels()
        bottomSizer = self.createButtons()
        
        fullSizer = wx.BoxSizer(wx.VERTICAL)
        fullSizer.AddStretchSpacer()
        fullSizer.Add(topSizer, 0, wx.ALL|wx.EXPAND, 5)
        fullSizer.AddStretchSpacer()
        fullSizer.Add(bottomSizer, 0, wx.ALL|wx.EXPAND, 5)
        self.panel.SetSizer(fullSizer)
        
        self.Maximize()
        self.setupMenu()

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_SIZE, self.onSizeOrMove)
        self.Bind(wx.EVT_MOVE, self.onSizeOrMove)
#         self.panel.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

################################################################################

    def toggleFullScreen(self, event):
        self.camera.setPreviewFullscreen(not self.camera.previewIsFullscreen())

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
        
        self.goBtn.SetFocus()
        
        self.modeBtn.Bind(wx.EVT_BUTTON, self.changeMode)
        self.goBtn.Bind(wx.EVT_BUTTON, self.doCameraAction)
        self.effectBtn.Bind(wx.EVT_BUTTON, self.changeEffectUp)
        
        return bottomSizer

################################################################################

    def setupCamera(self):
        self.camera = Camera()
        self.camera.startPreview(1000, 1000, 1280, 1024)
            
################################################################################
            
    def setupMenu(self):
        self.menuBar = wx.MenuBar()
        
        # File menu
        menu1 = wx.Menu()
        menu1.Append(101, "Set photo directory")
        menu1.AppendSeparator()
        menu1.Append(102, "Quit")
        self.menuBar.Append(menu1, "File")
        
        self.SetMenuBar(self.menuBar)
        
        self.Bind(wx.EVT_MENU, self.setPhotoDirectory, id=101)
        self.Bind(wx.EVT_MENU, self.close, id=102)
        
        # Setup keyboard shortcuts
        shortcuts = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('P'), 1001)])
        self.SetAcceleratorTable(shortcuts)
        self.Bind(wx.EVT_MENU, self.toggleFullScreen, id=1001)
        
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

    def changeEffectUp(self, event=None):
        self.camera.changeEffectUp()
        self.effectBtn.SetLabel(self.EFFECT_LABEL % self.camera.getEffectName())

################################################################################

    def changeEffectDown(self, event=None):
        self.camera.changeEffectDown()
        self.effectBtn.SetLabel(self.EFFECT_LABEL % self.camera.getEffectName())

################################################################################

    def changeMode(self, event=None):
        self.mode = (self.mode + 1) % len(self.MODES)
        self.modeBtn.SetLabel(self.MODE_LABEL % self.MODES[self.mode])

################################################################################

    def doCameraAction(self, event=None):
        if self.MODES[self.mode] == self.MODE_SINGLE and not self.isTakingPhoto:
            photoThread = Thread(target=self.countdownToSinglePhoto)
            photoThread.start()
        elif self.MODES[self.mode] == self.MODE_4_TILE and not self.isTakingPhoto:
            photoThread = Thread(target=self.countdownToSequencePhotos)
            photoThread.start()
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
                    break;
                sleep(0.01)
                
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
            wx.CallAfter(self.label1.SetLabelText, str(x))
            wx.CallAfter(self.label2.SetLabelText, str(x))
            sleep(1)
        wx.CallAfter(self.label1.SetLabel, "")
        wx.CallAfter(self.label2.SetLabel, "")

        self.camera.takePhoto()
        self.isTakingPhoto = False
        self.modeBtn.Enable(True)

################################################################################

    def countdownToSequencePhotos(self):
        self.isTakingPhoto = True
        self.modeBtn.Enable(False)
        self.camera.startSequence()
        
        for i in xrange(self.PHOTO_SEQUENCE_COUNT):
            sleep(self.PHOTO_SEQUENCE_GAP_TIME)
            for x in xrange(self.PHOTO_COUNTDOWN_TIME, 0, -1):
                wx.CallAfter(self.label1.SetLabel, str(x))
                wx.CallAfter(self.label2.SetLabel, str(x))
                sleep(1)
            wx.CallAfter(self.label1.SetLabel, "")
            wx.CallAfter(self.label2.SetLabel, "")
    
            self.camera.takePhoto()
        
        self.camera.stopSequence()
        self.isTakingPhoto = False
        self.modeBtn.Enable(True)

################################################################################

    def OnEraseBackground(self, event):
        dc = event.GetDC()
 
        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("graphics/hubbleBackground2.jpg")
        dc.DrawBitmap(bmp, 0, 0)
