"""
Author: Anthony Makepeace
File: Main
"""

####
## Import libraries
####
import RPi.GPIO as GPIO
import time
import os

####
## Initialisation of Pins
####
GPIO.setmode(GPIO.BCM)

# Button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PIR


####
## Functions
####

# Welcome Message & Choice
def welcomeFunc():
    os.system('clear')
    print ("Welcome to Smart Doorbell")
    sleep(3)
    os.system('clear')
    print ("Please choose an option: ")
    print ("1. Alert Someone")
    print ("2. Fingerprint")
    print ("3. Keypad")
    print ("4. RFID")
    print ("5. Facial Recognition")
    choice = raw_input("Please input number of choice: ")
    choiceProcessor(choice)

# Takes choice and executes relevant function.
def choiceProcessor(choiceNo):
    if choiceNo == 1:
        print ("Alerting Someone Now..")
        print ("Please Wait...")
        #Call alert file

    elif choiceNo == 2:
        print ("Initialising Fingerprint Function...")
        print ("Please Wait...")
        #Call Fingerprint file

    elif choiceNo == 3:
        print ("Initialising Keyapad Function...")
        print ("Please Wait...")
        #Call keypad file

    elif choiceNo == 4:
        print ("Initialising RFID Function...")
        print ("Please Wait...")
        #Call RFID file

    elif choiceNo == 5:
        print ("Initialising Facial Recognition Function...")
        print ("Please Wait...")
        #Call facial Recognition file

####
## Main
####

# When main button is pressed call LCD Function
GPIO.add_event_detect(24, GPIO.RISING, callback=welcomeFunc)
