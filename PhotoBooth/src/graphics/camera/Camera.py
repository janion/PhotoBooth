# -*- coding: utf-8 *-*

from picamera import PiCamera
import os

class Camera():

    EFFECTS = ["none", "negative", "sketch", "emboss", "oilpaint",
               "hatch", "gpen", "pastel", "saturation",
               "washedout", "colorpoint", "colorpoint", "colorpoint", "colorpoint",
               "cartoon", "colorswap", "colorswap",
               "posterise"
               #"solarize" :,
               #"film" :,
               #"colorbalance" :
               #, "watercolor"
               ]

    EFFECT_PARAMS = [None, None, None, None, None, None, None, None,
                     None, None, 0, 1, 2, 3, None,
                     0, 1, 7
                   #"solarize" :,
                   #"film" :,
                   #"posterise" :,
                   #"colorbalance" :
                   ]
    EFFECT_INDEX = -1;
    
    PHOTO_NAME_FORMAT = "Photo%05d"

    def __init__(self,):
        self.camera = PiCamera()
        self.directory = os.getcwd()

################################################################################

    def getPreviewSize(self):
        return self.camera.preview.window[2:4]

################################################################################

    def startPreview(self, x, y, width, height):
        self.camera.start_preview(fullscreen=False, hflip=True, window=(x, y, width, height))
        self.effect()

################################################################################

    def setPreview(self, x, y, width, height):
        self.camera.preview.window = (x, y, width, height)

################################################################################

    def effect(self):
        self.EFFECT_INDEX = (self.EFFECT_INDEX + 1) % len(self.EFFECTS)
        self.camera.image_effect = self.EFFECTS[self.EFFECT_INDEX]

        if self.EFFECT_PARAMS[self.EFFECT_INDEX] != None:
            self.camera.image_effect_params = self.EFFECT_PARAMS[self.EFFECT_INDEX]

################################################################################

    def getEffectName(self):
        return self.EFFECTS[self.EFFECT_INDEX]

################################################################################

    def takePhoto(self):
        count = len(os.listdir(self.directory))
        self.camera.capture(self.PHOTO_NAME_FORMAT % (count + 1))

################################################################################

    def stopPreview(self):
        self.camera.stop_preview()

################################################################################

    def setPhotoDirectory(self, directory):
        self.directory = directory

################################################################################

    def getPhotoDirectory(self):
        return self.directory
