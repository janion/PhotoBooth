'''
Created on 4 Jan 2017

@author: Janion
'''

import wx
from time import sleep, time
from threading import Thread

from physical.camera.MockCamera import Camera
from physical.triggers.MockPhysicalTriggers import PhysicalTriggers
from graphics.DrawPanel import DrawPanel

class Window(wx.Frame):
    
    COUNTDOWN_FORMAT = "   %d   "

    TITLE = "PhotoBooth - %s"
    EFFECT_LABEL = "Effect: %s"
    SCREEN_OFFSET_X = 24
    SCREEN_OFFSET_Y = 46
    
    MODE_LABEL = "Mode: %s"
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

        self.isTakingPhoto = False
        self.isRecording = False
        self.setupCamera()
        self.SetTitle(self.TITLE % self.camera.getPhotoDirectory())
        physicalTriggers = PhysicalTriggers()
        physicalTriggers.start(self.changeMode, self.doCameraAction, self.changeEffectUp, self.changeEffectDown)
        
        self.timeFont = wx.Font(0, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.timeText = ""
        self.timeColour = "WHITE"
        
        self.optionsFont = wx.Font(0, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.optionsColour = "WHITE"
        
        self.mode = 0
    
        self.panel = DrawPanel(self, self.drawGui)
        
        self.Maximize()
        self.setupMenu()

        self.Bind(wx.EVT_CLOSE, self.onClose)
        self.Bind(wx.EVT_SIZE, self.onSizeOrMove)
        self.Bind(wx.EVT_MOVE, self.onSizeOrMove)

################################################################################
    
    def drawGui(self, dc):
        dc.BeginDrawing()
        
#         bmp = wx.Bitmap("hubbleBackground2.jpg")
#         bmp = wx.Bitmap("spiralGalaxy.jpg")
#         bmp = wx.Bitmap("supernova.png")
        bmp = wx.Bitmap("nebula.jpg")
        dc.DrawBitmap(bmp, 0, 0)
        
        dc.SetTextForeground(self.timeColour)
        dc.SetFont(self.timeFont)
        
        width, height = dc.GetTextExtent(self.timeText)
        dc.DrawText(self.timeText, 0, (self.panel.Size[1] / 3) - (height / 2))
        dc.DrawText(self.timeText, self.panel.Size[0] - width, (self.panel.Size[1] / 3) - (height / 2))
        
        dc.SetTextForeground(self.optionsColour)
        dc.SetFont(self.optionsFont)
        
        effectLabel = self.EFFECT_LABEL % self.camera.getEffectName()
        modeLabel = self.MODE_LABEL % self.MODES[self.mode]
        
        width, height = dc.GetTextExtent(effectLabel)
        dc.DrawText(effectLabel, (self.panel.Size[0] / 3) - (width / 2), (self.panel.Size[1] * 0.9) - (height / 2))
        
        width, height = dc.GetTextExtent(modeLabel)
        dc.DrawText(modeLabel, ((2 * self.panel.Size[0]) / 3) - (width / 2), (self.panel.Size[1] * 0.9) - (height / 2))
        
#         dc.SetPen(wx.Pen("RED", 3))
#         dc.SetBrush(wx.Brush("BLACK", style=wx.BRUSHSTYLE_TRANSPARENT))
#         padding = 20
#         width, height = dc.GetTextExtent(modeLabel)
#         dc.DrawRoundedRectangle(((3 * self.panel.Size[0]) / 4) - (width / 2) - padding,
#                                 (self.panel.Size[1] * 0.9) - (height / 2) - padding,
#                                 width + 2 * padding,
#                                 height + 2 * padding,
#                                 padding
#                                 )
    
        dc.EndDrawing()

################################################################################

    def toggleFullScreen(self, event):
        self.camera.setPreviewFullscreen(not self.camera.previewIsFullscreen())

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
        
        # Camera menu
        menu2 = wx.Menu()
        menu2.Append(201, "Change Mode")
        menu2.Append(202, "Effect Up")
        menu2.Append(203, "Effect Down")
        menu2.AppendSeparator()
        menu2.Append(204, "Go!")
        self.menuBar.Append(menu2, "Camera")
        
        self.SetMenuBar(self.menuBar)
        
        self.Bind(wx.EVT_MENU, self.setPhotoDirectory, id=101)
        self.Bind(wx.EVT_MENU, self.close, id=102)
        
        self.Bind(wx.EVT_MENU, self.changeMode, id=201)
        self.Bind(wx.EVT_MENU, self.changeEffectUp, id=202)
        self.Bind(wx.EVT_MENU, self.changeEffectDown, id=203)
        self.Bind(wx.EVT_MENU, self.doCameraAction, id=204)
        
        # Setup keyboard shortcuts
        shortcuts = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('P'), 1001),
                                         (wx.ACCEL_NORMAL, wx.WXK_SPACE, 1002),
                                         (wx.ACCEL_NORMAL, wx.WXK_UP, 1003),
                                         (wx.ACCEL_NORMAL, wx.WXK_DOWN, 1004),
                                         (wx.ACCEL_NORMAL, wx.WXK_RETURN, 1005)
                                         ])
        self.SetAcceleratorTable(shortcuts)
        self.Bind(wx.EVT_MENU, self.toggleFullScreen, id=1001)
        self.Bind(wx.EVT_MENU, self.changeMode, id=1002)
        self.Bind(wx.EVT_MENU, self.changeEffectUp, id=1003)
        self.Bind(wx.EVT_MENU, self.changeEffectDown, id=1004)
        self.Bind(wx.EVT_MENU, self.doCameraAction, id=1005)
        
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
        [width, __] = self.GetSize()
        x = (width/8) + X + self.SCREEN_OFFSET_X
        y = Y + self.SCREEN_OFFSET_Y
        newWidth = int(0.75 * width)

        self.camera.setPreview(x, y, newWidth, int(newWidth * resRatio))

        self.timeFont = wx.Font(width / 12, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.optionsFont = wx.Font(width / 40, wx.SWISS, wx.NORMAL, wx.BOLD)

        event.Skip()

################################################################################

    def changeEffectUp(self, event=None):
        self.camera.changeEffectUp()
        self.panel.redraw()

################################################################################

    def changeEffectDown(self, event=None):
        self.camera.changeEffectDown()
        self.panel.redraw()

################################################################################

    def changeMode(self, event=None):
        self.mode = (self.mode + 1) % len(self.MODES)
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
        self.timeColour = "RED"
        
        for x in xrange(self.VIDEO_MAX_LENGTH, 0, -1):
            self.timeText = self.COUNTDOWN_FORMAT % x
            wx.CallAfter(self.panel.redraw)
            
            while(time() < startTime + 1 + (self.VIDEO_MAX_LENGTH - x)):
                if not self.isRecording:
                    break;
                sleep(0.01)
                
            if not self.isRecording:
                break;
                
        # Reset labels
        self.timeText = ""
        wx.CallAfter(self.panel.redraw)

        self.camera.stopRecording()
        self.isRecording = False

################################################################################

    def countdownToSinglePhoto(self):
        self.isTakingPhoto = True
        self.timeColour = "WHITE"
        
        for x in xrange(self.PHOTO_COUNTDOWN_TIME, 0, -1):
            self.timeText = self.COUNTDOWN_FORMAT % x
            wx.CallAfter(self.panel.redraw)
            sleep(1)
            
        self.timeText = ""
        wx.CallAfter(self.panel.redraw)

        self.camera.takePhoto()
        self.isTakingPhoto = False

################################################################################

    def countdownToSequencePhotos(self):
        self.isTakingPhoto = True
        self.camera.startSequence()
        self.timeColour = "WHITE"
        
        for __ in xrange(self.PHOTO_SEQUENCE_COUNT):
            sleep(self.PHOTO_SEQUENCE_GAP_TIME)
            
            for x in xrange(self.PHOTO_COUNTDOWN_TIME, 0, -1):
                self.timeText = self.COUNTDOWN_FORMAT % x
                wx.CallAfter(self.panel.redraw)
                sleep(1)
                
            self.timeText = ""
            wx.CallAfter(self.panel.redraw)
            self.camera.takePhoto()
        
        self.camera.stopSequence()
        self.isTakingPhoto = False

################################################################################


if __name__ == '__main__':
    app = wx.App()
    fr = Window(None, -1)
    fr.Show()
    app.MainLoop()
