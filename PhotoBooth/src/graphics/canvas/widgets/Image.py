import wx


class Image(object):

    def __init__(self, imageFilePath, position=(0, 0)):
        self.bmp = wx.Bitmap(imageFilePath)
        self.position = position

    def draw(self, dc):
        dc.DrawBitmap(self.bmp, *self.position)

    def mouseDown(self, event, dc):
        pass

    def mouseUp(self, event, dc):
        pass
