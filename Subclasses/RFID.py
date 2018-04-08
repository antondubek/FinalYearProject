"""
Author: Anthony Makepeace
File: RFID
"""

####
## Import libraries
####
import signal
import time

from pirc522 import RFID

####
## Initialisation
####
rdr = RFID()
cardsAccept = "229,49,219,209"


####
## Functions
####

# Waits for RFID tag before checking whether in accpeted list. If so, returns true else returns false.
def checkRFIDTag():

    print("Starting")

    while True:

        print ("Please Present Tag to Reader")
        rdr.wait_for_tag()

        (error, data) = rdr.request()

        (error, uid) = rdr.anticoll()
        if not error:
            cardID = str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])

            #print(cardID)

            if cardID == cardsAccept:
                print ("RFID Accepted")
                return True

            else:
                print ("Sorry this RFID is not recognised")
                return False



####
## Main
####
