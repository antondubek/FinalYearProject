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
def checkRFIDTag():

    print("Starting")

    while True:

        print ("Please Present Tag to Reader")
        rdr.wait_for_tag()

        (error, data) = rdr.request()
        #if not error:
            #print("\nDetected: " + format(data, "02x"))

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