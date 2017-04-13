'''
Created on 9 Mar 2017

@author: Janion
'''

import serial.Serial as Serial
from threading import Thread

class ArduinoConnector():
    
    def __init__(self):
        self.isConnected = False
        
################################################################################

    def start(self, portName, baudRate):
        connectionThread = Thread(target=self.connect, args=(portName, baudRate))
        connectionThread.start()
        
################################################################################
    
    def connect(self, portName, baudRate):
        self.connection = Serial(portName, baudRate)
        self.isConnected = True

################################################################################
    
    def sendMessage(self, message):
        if self.isConnected:
            self.connection.write(unicode(message))
            self.connection.flush()
        