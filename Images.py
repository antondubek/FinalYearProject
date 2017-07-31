"""
Author: Anthony Makepeace
File: Images
About: File to include functions relating to taking and
uploading images to a location where a web application can find them.
"""

####
## Import libraries
####
import time
import os
from datetime import datetime

####
## Initialisation of Pins
####

####
## Functions
####
def takePicture():
    now = datetime.now()
    time = now.strftime(“%Y-%m-%d-%H-%M”)
    print ("Taking Picture")
    os.system("cd /home/pi/Documents/TestProjects/WebcamPics | fswebcam " + time +".jpg")

####
## Main
####
