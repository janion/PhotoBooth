import wx


class Image(object):

    def __init__(self, imageFilePath, position=(0, 0)):
        self.imageFilePath = imageFilePath
        self.position = position

    def draw(self, dc):
        bmp = wx.Bitmap("graphics/nebula.jpg")
        dc.DrawBitmap(bmp, *self.position)
