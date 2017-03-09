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
    
    PHOTO_FILE_EXTENSION = ".jpg"
    VIDEO_FILE_EXTENSION = ".h264"
    PHOTO_NAME_FORMAT = "Photo%05d" + PHOTO_FILE_EXTENSION
    PHOTO_SEQUENCE_NAME_FORMAT = "Photo%05d.%d" + PHOTO_FILE_EXTENSION
    VIDEO_NAME_FORMAT = "Video%05d" + VIDEO_FILE_EXTENSION

    def __init__(self):
        self.camera = PiCamera()
        self.setPhotoDirectory(os.getcwd())
        self.isInSequence = False

################################################################################

    def getPreviewSize(self):
        return self.camera.preview.window[2:4]

################################################################################

    def startPreview(self, x, y, width, height):
        self.camera.start_preview(fullscreen=False, hflip=True, window=(x, y, width, height))
        self.changeEffect()

################################################################################

    def setPreview(self, x, y, width, height):
        self.camera.preview.window = (x, y, width, height)

################################################################################

    def changeEffectUp(self):
        self.EFFECT_INDEX = (self.EFFECT_INDEX + 1) % len(self.EFFECTS)
        self.camera.image_effect = self.EFFECTS[self.EFFECT_INDEX]

        if self.EFFECT_PARAMS[self.EFFECT_INDEX] != None:
            self.camera.image_effect_params = self.EFFECT_PARAMS[self.EFFECT_INDEX]

################################################################################

    def changeEffectDown(self):
        self.EFFECT_INDEX = ((len(self.EFFECTS) + self.EFFECT_INDEX) - 1) % len(self.EFFECTS)
        self.camera.image_effect = self.EFFECTS[self.EFFECT_INDEX]

        if self.EFFECT_PARAMS[self.EFFECT_INDEX] != None:
            self.camera.image_effect_params = self.EFFECT_PARAMS[self.EFFECT_INDEX]

################################################################################

    def getEffectName(self):
        return self.EFFECTS[self.EFFECT_INDEX]

################################################################################

    def takePhoto(self):
        if self.isInSequence:
            self.camera.capture(self.PHOTO_SEQUENCE_NAME_FORMAT % ((self.videoCount + 1), self.sequenceIndex))
        else:
            self.camera.capture(self.PHOTO_NAME_FORMAT % (self.videoCount + 1))

################################################################################

    def stopPreview(self):
        self.camera.stop_preview()

################################################################################

    def setPhotoDirectory(self, directory):
        self.directory = directory
        self.photoCount = len([name for name in os.listdir(self.directory) if name.endswith(self.PHOTO_FILE_EXTENSION)])
        self.videoCount = len([name for name in os.listdir(self.directory) if name.endswith(self.VIDEO_FILE_EXTENSION)])

################################################################################

    def getPhotoDirectory(self):
        return self.directory

################################################################################

    def startRecording(self):
        self.camera.start_recording(self.VIDEO_NAME_FORMAT % (self.videoCount + 1))

################################################################################

    def stopRecording(self):
        self.camera.stop_recording()

################################################################################

    def startSequence(self):
        self.isInSequence = True
        self.sequenceIndex = 1

################################################################################

    def stopSequence(self):
        self.isInSequence = False