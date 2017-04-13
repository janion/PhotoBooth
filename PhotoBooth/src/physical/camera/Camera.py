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
        self.effectIndex = 0;
        self.camera.image_effect = self.EFFECTS[self.effectIndex]

################################################################################

    def setPreviewFullscreen(self, isFull):
        self.camera.preview.fullscreen = isFull

################################################################################

    def previewIsFullscreen(self):
        return self.camera.preview.fullscreen

################################################################################

    def setPreview(self, x, y, width, height):
        self.camera.preview.window = (x, y, width, height)

################################################################################

    def changeEffectUp(self):
        self.effectIndex = (self.effectIndex + 1) % len(self.EFFECTS)
        self.camera.image_effect = self.EFFECTS[self.effectIndex]

        if self.EFFECT_PARAMS[self.effectIndex] != None:
            self.camera.image_effect_params = self.EFFECT_PARAMS[self.effectIndex]

################################################################################

    def changeEffectDown(self):
        self.effectIndex = ((len(self.EFFECTS) + self.effectIndex) - 1) % len(self.EFFECTS)
        self.camera.image_effect = self.EFFECTS[self.effectIndex]

        if self.EFFECT_PARAMS[self.effectIndex] != None:
            self.camera.image_effect_params = self.EFFECT_PARAMS[self.effectIndex]

################################################################################

    def getEffectName(self):
        return self.EFFECTS[self.effectIndex]

################################################################################

    def takePhoto(self):
        if self.isInSequence:
            self.camera.capture(self.PHOTO_SEQUENCE_NAME_FORMAT % ((self.photoCount + 1), self.sequenceIndex))
        else:
            self.camera.capture(self.PHOTO_NAME_FORMAT % (self.photoCount + 1))
        
        self.photoCount += 1

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
        self.videoCount += 1

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
