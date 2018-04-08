"""
Author: Anthony Makepeace
File: RFID
"""

####
## Import libraries
####
import signal
import time
from time import sleep
import picamera
import telepot
from datetime import datetime
from pirc522 import RFID


####
## Initialisation
####
#Initialises and connects to the telegram doorbell bot
bot = telepot.Bot(token='471263091:AAEFiEIp0Sd_ud0I0G7ARHzIsTE56TMmm2Y')
chatID = 489826446

# Initialise RFID Reader
rdr = RFID()

# Accepted Card Lists
residentCards = {"229,49,219,209" : "Anthony", "1" : "Mark"}
cleanerCards = ["3"]

####
## Functions
####
def takePicture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1080, 720)
        camera.rotation = 90
        now = datetime.now()
        label = now.strftime("%c")
        print ("Initialising Camera")
        camera.start_preview()
        sleep(2)
        os.chdir ("/home/pi/DoorbellImages")
        camera.capture("%s.jpg" %label)
        print ("Picture Taken")
        camera.close()
        return label

def checkRFIDTag():

    print("DEBUG: Starting RFID Authentication")

    while True:

        print("DEBUG: Waiting for card")

        rdr.wait_for_tag()
        (error, data) = rdr.request()
        (error, uid) = rdr.anticoll()

        # Reads the card RFID tag and writes to cardID string
        if not error:
            cardID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

        now = datetime.now()
        dayOfWeek = now.today().weekday()
        hour = now.hour

        # Check to see if card is a resident
        if cardID in residentCards:
            print ("DEBUG: Resident %s" %residentCards[cardID])
            bot.sendMessage(chatID, '%s has just arrived home' %residentCards[cardID])
            return residentCards[cardID]

        # Checks to see if card is a cleaner and in the permitted time frame
        elif cardID in cleanerAccept:

            # If the dayOfWeek is Mon-Sun(0-6) hour is between 24HR hours
            if dayOfWeek == 6 and hour < 15 and hour > 14:
                print ("DEBUG: Cleaner")
                label = takePicture()
                bot.sendMessage(chatID, 'The cleaner has arrived and been let in!')
                bot.sendPhoto(chatID, open('/home/pi/DoorbellImages/%s.jpg' %label,'rb'), caption = label)
                return True

            else:
                print ("DEBUG: Cleaner False")
                return False

        # Returns False for unknown cards
        else:
            print ("DEBUG: Unrecognised Card False")
            return False
