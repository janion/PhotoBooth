import wx


class EmptyArea(object):

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.handlers = []
        self.mousePressed = False

    def draw(self, dc):
        dc.SetPen(wx.Pen("GREEN", 3))
        dc.SetBrush(wx.Brush("BLACK", style=wx.TRANSPARENT))
        dc.DrawRectangle(self.x, self.y, self.width, self.height)

    def mouseDown(self, event, dc):
        eventConsumed = False
        eventPosition = event.GetLogicalPosition(dc)
        if self.x < eventPosition[0] < self.x + self.width:
            if self.y < eventPosition[1] < self.y + self.height:
                self.mousePressed = True
                eventConsumed = True

        return eventConsumed

    def mouseUp(self, event, dc):
        eventConsumed = False
        eventPosition = event.GetLogicalPosition(dc)
        if self.x < eventPosition[0] < self.x + self.width:
            if self.y < eventPosition[1] < self.y + self.height:
                if self.mousePressed:
                    for handler in self.handlers:
                        handler(event)
                        eventConsumed = True

        self.mousePressed = False
        return eventConsumed

    def addHandler(self, handler):
        self.handlers.append(handler)

    def removeHandler(self, handler):
        self.handlers.remove(handler)

    def setArea(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        print x, y, width, height
