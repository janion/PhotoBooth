# -*- coding: utf-8 *-*

import os


class Camera():
    EFFECTS = ["none", "negative", "sketch", "emboss", "oilpaint",
               "hatch", "gpen", "pastel", "saturation",
               "washedout", "colorpoint", "colorpoint", "colorpoint", "colorpoint",
               "cartoon", "colorswap", "colorswap",
               "posterise"
               ]

    EFFECT_NAMES = ["none", "negative", "sketch", "emboss", "oilpaint",
                    "hatch", "gpen", "pastel", "saturation",
                    "washedout", "green only", "orange only", "blue only", "purple only",
                    "cartoon", "BGR", "BRG",
                    "posterise"
                    #"solarize" :,
                    #"film" :,
                    #"colorbalance" :
                    #, "watercolor"
                    ]

    effectIndex = 0;
    isFull = False

    def __init__(self,):
        print "Camera created"
        self.directory = os.getcwd()
        self.preview = False

################################################################################

    def getPreviewSize(self):
        return (1000, 1000)

################################################################################

    def startPreview(self, x=0, y=0, width=0, height=0):
        print "Preview started"
        self.preview = True

################################################################################

    def setPreviewFullscreen(self, isFull):
        self.isFull = isFull
        if isFull:
            print "Preview full screen"
        else:
            print "Preview not full screen"

################################################################################

    def previewIsFullscreen(self):
        return self.isFull

################################################################################

    def setPreview(self, x, y, width, height):
        print "Preview set"

################################################################################

    def changeEffectUp(self):
        self.effectIndex = (self.effectIndex + 1) % len(self.EFFECTS)
        print "Effect changed up"

################################################################################

    def changeEffectDown(self):
        self.effectIndex = ((len(self.EFFECTS) + self.effectIndex) - 1) % len(self.EFFECTS)
        print "Effect changed down"

################################################################################

    def getEffectName(self):
        return self.EFFECT_NAMES[self.effectIndex]

################################################################################

    def takePhoto(self):
        print "Photo taken"

################################################################################

    def stopPreview(self):
        print "Preview stopped"
        self.preview = False

################################################################################

    def togglePreview(self):
        if self.preview:
            self.stopPreview()
        else:
            self.startPreview()

################################################################################

    def setPhotoDirectory(self, directory):
        self.directory = directory

################################################################################

    def getPhotoDirectory(self):
        return self.directory

################################################################################

    def startRecording(self):
        print "Starting recording"

################################################################################

    def stopRecording(self):
        print "Stopping recording"

################################################################################

    def startSequence(self):
        print "Starting sequence"

################################################################################

    def stopSequence(self):
        print "Stopping sequence"
