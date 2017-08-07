'''
Created on 4 Jan 2017

@author: Janion
'''

from threading import Thread
from time import sleep, time

import wx

from graphics.canvas.DrawPanel import DrawPanel
from graphics.canvas.widgets.CanvasLabel import CanvasLabel, Alignment
from graphics.canvas.widgets.Image import Image


class Window(wx.Frame):
    
    COUNTDOWN_FORMAT = " %d "

    EFFECT_LABEL = "Effect: %s"
    SCREEN_OFFSET_X = 24
    SCREEN_OFFSET_Y = 55
    
    MODE_LABEL = "Mode: %s"
    MODE_SINGLE = "Single"
    MODE_4_TILE = "4 Tile"
    MODE_VIDEO = "Video"
    MODES = [MODE_SINGLE, MODE_4_TILE, MODE_VIDEO]
    
    PHOTO_COUNTDOWN_TIME = 3
    PHOTO_SEQUENCE_COUNT = 4
    PHOTO_SEQUENCE_GAP_TIME = 1
    VIDEO_MAX_LENGTH = 30

    BACKGROUND_IMAGE_PATH = "graphics/nebula.jpg"

    def __init__(self, parent, idd, camera, physicalTriggers=None):
        wx.Frame.__init__(self, parent, idd, style = wx.RESIZE_BORDER)

        self.camera = camera
        if physicalTriggers:
            physicalTriggers.start(self.changeMode, self.doCameraAction, self.changeEffectUp, self.changeEffectDown)

        self.isTakingPhoto = False
        self.isRecording = False
        
        self.mode = 0
        self.panel = DrawPanel(self)

        self.setupMenus()

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_SIZE, self.onSizeOrMove)
        self.Bind(wx.EVT_MOVE, self.onSizeOrMove)
        self.Bind(wx.EVT_MAXIMIZE, self.onSizeOrMove)

        self.background = Image(self.BACKGROUND_IMAGE_PATH)
        self.leftTimeLabel = CanvasLabel(colour="WHITE", alignment=Alignment.CENTRE_LEFT)
        self.rightTimeLabel = CanvasLabel(colour="WHITE", alignment=Alignment.CENTRE_RIGHT)
        self.effectLabel = CanvasLabel(text=self.EFFECT_LABEL % self.camera.getEffectName(),
                                       colour="WHITE",
                                       alignment=Alignment.CENTRE,
                                       isClickable=True)
        self.modeLabel = CanvasLabel(text=self.MODE_LABEL % self.MODES[self.mode],
                                     colour="WHITE",
                                     alignment=Alignment.CENTRE,
                                     isClickable=True)

        self.effectLabel.addHandler(self.changeEffectUp)
        self.modeLabel.addHandler(self.changeMode)

        self.panel.addWidget(self.background)
        self.panel.addWidget(self.leftTimeLabel)
        self.panel.addWidget(self.rightTimeLabel)
        self.panel.addWidget(self.effectLabel)
        self.panel.addWidget(self.modeLabel)

        self.ShowFullScreen(True)

################################################################################

    def toggleFullScreen(self, event):
        self.camera.setPreviewFullscreen(not self.camera.previewIsFullscreen())
            
################################################################################
            
    def setupMenus(self):
        contextMenu = wx.Menu()
        contextMenu.AppendMenu(-1, "File", self._createFileMenu())
        contextMenu.AppendMenu(-1, "Camera", self._createCameraMenu())
        self._createKeyboardShortcuts()

        self.Bind(wx.EVT_CONTEXT_MENU, lambda __: self._contextMenu(contextMenu))

################################################################################

    def _createFileMenu(self):
        menu = wx.Menu()
        menu.Append(101, "Set photo directory")
        menu.AppendSeparator()
        menu.Append(102, "Quit")

        self.Bind(wx.EVT_MENU, self.setPhotoDirectory, id=101)
        self.Bind(wx.EVT_MENU, self.close, id=102)

        return menu

################################################################################

    def _createCameraMenu(self):
        menu = wx.Menu()
        menu.Append(201, "Change Mode")
        menu.Append(202, "Effect Up")
        menu.Append(203, "Effect Down")
        menu.AppendSeparator()
        menu.Append(204, "Go!")
        menu.AppendSeparator()
        menu.Append(205, "Refresh")

        self.Bind(wx.EVT_MENU, self.changeMode, id=201)
        self.Bind(wx.EVT_MENU, self.changeEffectUp, id=202)
        self.Bind(wx.EVT_MENU, self.changeEffectDown, id=203)
        self.Bind(wx.EVT_MENU, self.doCameraAction, id=204)
        self.Bind(wx.EVT_MENU, self.onSizeOrMove, id=205)

        return menu

################################################################################

    def _createKeyboardShortcuts(self):
        shortcuts = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('P'), 1001),
                                         (wx.ACCEL_NORMAL, wx.WXK_SPACE, 1002),
                                         (wx.ACCEL_NORMAL, wx.WXK_UP, 1003),
                                         (wx.ACCEL_NORMAL, wx.WXK_DOWN, 1004),
                                         (wx.ACCEL_NORMAL, wx.WXK_RETURN, 1005),
                                         (wx.ACCEL_NORMAL, wx.WXK_F5, 1006),
                                         (wx.ACCEL_CTRL, ord('C'), 1007),
                                         (wx.ACCEL_CTRL, ord('Q'), 1008)
                                         ])

        self.SetAcceleratorTable(shortcuts)

        self.Bind(wx.EVT_MENU, self.toggleFullScreen, id=1001)
        self.Bind(wx.EVT_MENU, self.changeMode, id=1002)
        self.Bind(wx.EVT_MENU, self.changeEffectUp, id=1003)
        self.Bind(wx.EVT_MENU, self.changeEffectDown, id=1004)
        self.Bind(wx.EVT_MENU, self.doCameraAction, id=1005)
        self.Bind(wx.EVT_MENU, self.onSizeOrMove, id=1006)
        self.Bind(wx.EVT_MENU, lambda __: self.camera.togglePreview(), id=1007)
        self.Bind(wx.EVT_MENU, self.close, id=1008)
        
################################################################################

    def _contextMenu(self, menu):
        self.PopupMenu(menu)
        # menu.Destroy()

################################################################################

    def setPhotoDirectory(self, event):
        dlg = wx.DirDialog(self, message="Choose destination for photos", style=wx.DD_DEFAULT_STYLE)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data.
        if dlg.ShowModal() == wx.ID_OK:
            self.camera.setPhotoDirectory(dlg.GetPath())

        dlg.Destroy()

################################################################################

    def onSizeOrMove(self, event=None):
        (resX, resY) = self.camera.getPreviewSize()
        if resX == 0 or resY == 0:
            return

        resRatio = float(resY) / resX

        [X, Y] = self.GetPosition()
        [width, __] = self.GetSize()
        x = (width/8) + X + self.SCREEN_OFFSET_X
        y = Y + self.SCREEN_OFFSET_Y
        newWidth = int(0.75 * width)

        self.camera.setPreview(x, y, newWidth, int(newWidth * resRatio))

        self.leftTimeLabel.setFont(wx.Font(width / 12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.rightTimeLabel.setFont(wx.Font(width / 12, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.leftTimeLabel.setPosition((0, (self.panel.Size[1] / 3)))
        self.rightTimeLabel.setPosition((self.panel.Size[0], (self.panel.Size[1] / 3)))

        self.effectLabel.setFont(wx.Font(width / 40, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.modeLabel.setFont(wx.Font(width / 40, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.effectLabel.setPosition(((self.panel.Size[0] / 3), (self.panel.Size[1] * 0.9)))
        self.modeLabel.setPosition(((2 * self.panel.Size[0] / 3), (self.panel.Size[1] * 0.9)))

        self.panel.redraw()
        event.Skip()

################################################################################

    def changeEffectUp(self, event=None):
        if not self.isTakingPhoto and not self.isRecording:
            self.camera.changeEffectUp()
            self.effectLabel.setText(self.EFFECT_LABEL % self.camera.getEffectName())
            self.panel.redraw()

################################################################################

    def changeEffectDown(self, event=None):
        if not self.isTakingPhoto and not self.isRecording:
            self.camera.changeEffectDown()
            self.effectLabel.setText(self.EFFECT_LABEL % self.camera.getEffectName())
            self.panel.redraw()

################################################################################

    def changeMode(self, event=None):
        if not self.isTakingPhoto and not self.isRecording:
            self.mode = (self.mode + 1) % len(self.MODES)
            self.modeLabel.setText(self.MODE_LABEL % self.MODES[self.mode])
            self.panel.redraw()

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
        self.camera.startRecording()
        startTime = time()
        self.leftTimeLabel.setColour("RED")
        self.rightTimeLabel.setColour("RED")
        
        for x in xrange(self.VIDEO_MAX_LENGTH, 0, -1):
            self.leftTimeLabel.setText(self.COUNTDOWN_FORMAT % x)
            self.rightTimeLabel.setText(self.COUNTDOWN_FORMAT % x)
            wx.CallAfter(self.panel.redraw)
            
            while(time() < startTime + 1 + (self.VIDEO_MAX_LENGTH - x)):
                if not self.isRecording:
                    break;
                sleep(0.01)
                
            if not self.isRecording:
                break;
                
        # Reset labels
        self.leftTimeLabel.setText("")
        self.rightTimeLabel.setText("")
        wx.CallAfter(self.panel.redraw)

        self.camera.stopRecording()
        self.isRecording = False

################################################################################

    def countdownToSinglePhoto(self):
        self.isTakingPhoto = True
        self.leftTimeLabel.setColour("WHITE")
        self.rightTimeLabel.setColour("WHITE")
        
        for x in xrange(self.PHOTO_COUNTDOWN_TIME, 0, -1):
            self.leftTimeLabel.setText(self.COUNTDOWN_FORMAT % x)
            self.rightTimeLabel.setText(self.COUNTDOWN_FORMAT % x)
            wx.CallAfter(self.panel.redraw)
            sleep(1)

        self.leftTimeLabel.setText("")
        self.rightTimeLabel.setText("")
        wx.CallAfter(self.panel.redraw)

        self.camera.takePhoto()
        self.isTakingPhoto = False

################################################################################

    def countdownToSequencePhotos(self):
        self.isTakingPhoto = True
        self.camera.startSequence()
        self.leftTimeLabel.setColour("WHITE")
        self.rightTimeLabel.setColour("WHITE")
        
        for __ in xrange(self.PHOTO_SEQUENCE_COUNT):
            sleep(self.PHOTO_SEQUENCE_GAP_TIME)
            
            for x in xrange(self.PHOTO_COUNTDOWN_TIME, 0, -1):
                self.leftTimeLabel.setText(self.COUNTDOWN_FORMAT % x)
                self.rightTimeLabel.setText(self.COUNTDOWN_FORMAT % x)
                wx.CallAfter(self.panel.redraw)
                sleep(1)

            self.leftTimeLabel.setText("")
            self.rightTimeLabel.setText("")
            wx.CallAfter(self.panel.redraw)
            self.camera.takePhoto()
        
        self.camera.stopSequence()
        self.isTakingPhoto = False
