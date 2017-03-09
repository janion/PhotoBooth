'''
Created on 8 Mar 2017

@author: Janion
'''

import wx
import RPi.GPIO as GPIO

class PhysicalTriggers():
    
    MODE_BUTTON = 3;
    EFFECT_UP_BUTTON = 5;
    EFFECT_DOWN_BUTTON = 7;
    GO_BUTTON = 9;
    BUTTONS = [MODE_BUTTON, EFFECT_UP_BUTTON, EFFECT_DOWN_BUTTON, GO_BUTTON]
    
    def start(self, modeAction, goAction, effectUpAction, effectDownAction):
        # Setup GPIO
        GPIO.setmode(GPIO.BOARD)
        
        # Setup button pins as inputs
        for button in self.BUTTONS:
            GPIO.setup(button, GPIO.IN)
        
        # Add listeners to GPIO edges
        GPIO.add_event_detect(self.MODE_BUTTON, GPIO.RISING, callback=lambda x : wx.CallAfter(modeAction), bouncetime=100)
        GPIO.add_event_detect(self.EFFECT_UP_BUTTON, GPIO.RISING, callback=lambda x : wx.CallAfter(effectUpAction), bouncetime=100)
        GPIO.add_event_detect(self.EFFECT_DOWN_BUTTON, GPIO.RISING, callback=lambda x : wx.CallAfter(effectDownAction), bouncetime=100)
        GPIO.add_event_detect(self.GO_BUTTON, GPIO.RISING, callback=lambda x : wx.CallAfter(goAction), bouncetime=100)
    
    
        