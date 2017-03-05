# -*- coding: utf-8 *-*

import os

class Camera():
    EFFECTS = ["none", "negative", "sketch", "emboss", "oilpaint",
               "hatch", "gpen", "pastel", "saturation",
               "washedout", "colorpoint", "colorpoint", "colorpoint", "colorpoint",
               "cartoon", "colorswap", "colorswap",
               "posterise"
               ]
    EFFECT_INDEX = 0;

    def __init__(self,):
        print "Camera created"
        self.directory = os.getcwd()

################################################################################

    def getPreviewSize(self):
        return (1000, 1000)

################################################################################

    def startPreview(self, x, y, width, height):
        print "Preview started"

################################################################################

    def setPreview(self, x, y, width, height):
        print "Preview set"

################################################################################

    def changeEffect(self):
        self.EFFECT_INDEX = (self.EFFECT_INDEX + 1) % len(self.EFFECTS)
        print "Effect changed"

################################################################################

    def getEffectName(self):
        return self.EFFECTS[self.EFFECT_INDEX]

################################################################################

    def doCameraAction(self):
        print "Photo taken"

################################################################################

    def stopPreview(self):
        print "Preview stopped"

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
