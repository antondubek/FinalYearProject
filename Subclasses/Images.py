"""
Author: Anthony Makepeace
File: Images
About: File to include functions relating to taking and
uploading images to a location where a web application can find them.
"""

####
## Import libraries
####
import picamera
from datetime import datetime
from time import sleep
import os

####
## Initialisation
####


####
## Functions
####
def takePicture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1080, 720)
        now = datetime.now()
        label = now.strftime("%c")
        print ("Initialising Camera")
        camera.start_preview()
        sleep(1)
        os.chdir ("/home/pi/DoorbellImages")
        camera.capture("%s.jpg" %label)
        print ("Picture Taken")
        camera.close()

####
## Main
####
