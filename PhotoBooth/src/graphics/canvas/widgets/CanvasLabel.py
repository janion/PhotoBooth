import wx


class Alignment(object):
    TOP_LEFT = "TOP_LEFT"
    TOP_CENTRE = "TOP_CENTRE"
    TOP_RIGHT = "TOP_RIGHT"

    CENTRE_LEFT = "CENTRE_LEFT"
    CENTRE = "CENTRE_CENTRE"
    CENTRE_RIGHT = "CENTRE_RIGHT"

    BOTTOM_LEFT = "BOTTOM_LEFT"
    BOTTOM_CENTRE = "BOTTOM_CENTRE"
    BOTTOM_RIGHT = "BOTTOM_RIGHT"


def _movePosition(position, width, height, alignment):
    (newX, newY) = position

    if alignment in [Alignment.TOP_CENTRE, Alignment.CENTRE, Alignment.BOTTOM_CENTRE]:
        newX -= width / 2
    elif alignment in [Alignment.TOP_RIGHT, Alignment.CENTRE_RIGHT, Alignment.BOTTOM_RIGHT]:
        newX -= width

    if alignment in [Alignment.CENTRE_LEFT, Alignment.CENTRE, Alignment.CENTRE_RIGHT]:
        newY -= height / 2
    elif alignment in [Alignment.BOTTOM_LEFT, Alignment.BOTTOM_CENTRE, Alignment.BOTTOM_RIGHT]:
        newY -= height

    return newX, newY


class CanvasLabel(object):

    TEXT_KEY = "text"
    COLOUR_KEY = "colour"
    FONT_KEY = "font"
    POSITION_KEY = "position"
    ALIGNMENT_KEY = "alignment"
    CLICKABLE_KEY = "isClickable"

    DEFAULT_TEXT = ""
    DEFAULT_COLOUR = "WHITE"
    DEFAULT_FONT_PARAMETERS = (10, wx.SWISS, wx.NORMAL, wx.BOLD)
    DEFAULT_POSITION = (0, 0)
    DEFAULT_ALIGNMENT = Alignment.TOP_LEFT
    DEFAULT_CLICKABLE = False
    
    PADDING = 10
    CLICKED_BORDER_COLOUR = "RED"
    CLICKED_BORDER_WIDTH = 3

    def __init__(self, **kwargs):
        self.text = kwargs[self.TEXT_KEY] if kwargs.has_key(self.TEXT_KEY) else self.DEFAULT_TEXT
        self.colour = kwargs[self.COLOUR_KEY] if kwargs.has_key(self.COLOUR_KEY) else self.DEFAULT_COLOUR
        self.font = kwargs[self.FONT_KEY] if kwargs.has_key(self.FONT_KEY) else wx.Font(*self.DEFAULT_FONT_PARAMETERS)
        self.position = kwargs[self.POSITION_KEY] if kwargs.has_key(self.POSITION_KEY) else self.DEFAULT_POSITION
        self.alignment = kwargs[self.ALIGNMENT_KEY] if kwargs.has_key(self.ALIGNMENT_KEY) else self.DEFAULT_ALIGNMENT
        self.isClickable = kwargs[self.CLICKABLE_KEY] if kwargs.has_key(self.CLICKABLE_KEY) else self.DEFAULT_CLICKABLE

        self.size = (0, 0)
        self.mousePressed = False
        self.handlers = []

    def draw(self, dc):
        dc.SetTextForeground(self.colour)
        dc.SetFont(self.font)

        self.size = width, height = dc.GetTextExtent(self.text)

        position = _movePosition(self.position, width, height, self.alignment)
        dc.DrawText(self.text, *position)

        if self.mousePressed:
            dc.SetPen(wx.Pen(self.CLICKED_BORDER_COLOUR, self.CLICKED_BORDER_WIDTH))
            dc.SetBrush(wx.Brush(self.CLICKED_BORDER_COLOUR, style=wx.BRUSHSTYLE_TRANSPARENT))
            dc.DrawRoundedRectangle(position[0] - self.PADDING,
                                    position[1] - self.PADDING,
                                    width + 2 * self.PADDING,
                                    height + 2 * self.PADDING,
                                    self.PADDING
                                    )

    def mouseDown(self, event, dc):
        if self.isClickable:
            width, height = self.size
            position = _movePosition(self.position, width, height, self.alignment)
            eventPosition = event.GetLogicalPosition(dc)
            if position[0] < eventPosition[0] < position[0] + width:
                if position[1] < eventPosition[1] < position[1] + height:
                    self.mousePressed = True

    def mouseUp(self, event, dc):
        if self.isClickable:
            width, height = self.size
            position = _movePosition(self.position, width, height, self.alignment)
            eventPosition = event.GetLogicalPosition(dc)
            if position[0] < eventPosition[0] < position[0] + width:
                if position[1] < eventPosition[1] < position[1] + height:
                    if self.mousePressed:
                        for handler in self.handlers:
                            handler(event)

            self.mousePressed = False

    def addHandler(self, handler):
        self.handlers.append(handler)

    def removeHandler(self, handler):
        self.handlers.remove(handler)

    def setText(self, text):
        self.text = text

    def setColour(self, colour):
        self.colour = colour

    def setFont(self, font):
        self.font = font

    def setPosition(self, position):
        self.position = position

    def setAlignment(self, alignment):
        self.alignment = alignment
