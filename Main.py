"""
Author: Anthony Makepeace
File: Main
"""

####
## Import libraries
####
import RPi.GPIO as GPIO
from time import sleep
import os
from Keypad import FourDigitCodeCheck

####
## Initialisation of Pins
####

GPIO.setmode(GPIO.BCM)

# LED's
RedLED_pin = 25
GreenLED_pin = 18
GPIO.setup(GreenLED_pin,GPIO.OUT)
GPIO.setup(RedLED_pin,GPIO.OUT)
GPIO.output(RedLED_pin,GPIO.LOW)
GPIO.output(GreenLED_pin,GPIO.LOW)

# Button
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

    while True:

        # Option 3: Keypad
        if GPIO.wait_for_edge(24, GPIO.FALLING):
            choiceProcessor(3)

        #elif GPIO.wait_for_edge(24, GPIO.FALLING):
        #    choiceProcessor(3)

    #choice = int(raw_input("Please input number of choice: "))
    #choiceProcessor(choice)

# Takes choice and executes relevant function.
def choiceProcessor(choiceNo):
    if choiceNo == 1:
        print ("Alerting Someone Now..")
        print ("Please Wait...")
        #Call alert function

    elif choiceNo == 2:
        print ("Initialising Fingerprint Function...")
        print ("Please Wait...")
        #Call Fingerprint function

    elif choiceNo == 3:
        print ("Initialising Keyapad Function...")
        print ("Please Wait...")
        #Call keypad function
        keypadOutput = FourDigitCodeCheck()
        if keypadOutput == True:
            doorOpen()

    elif choiceNo == 4:
        print ("Initialising RFID Function...")
        print ("Please Wait...")
        #Call RFID function

    elif choiceNo == 5:
        print ("Initialising Facial Recognition Function...")
        print ("Please Wait...")
        #Call facial Recognition function

# Function to open / release door. LED for bug fixing
def doorOpen():
    print ("Door Open")
    GreenLED_on()

def GreenLED_on():
    GPIO.output(GreenLED_pin,GPIO.HIGH)
    sleep(3)
    GPIO.output(GreenLED_pin,GPIO.LOW)

def RedLED_on(pin):
    print ("Red LED On")
    GPIO.output(pin,GPIO.HIGH)
    sleep(3)
    GPIO.output(pin,GPIO.LOW)


####
## Main
####

# Polls for when button is pressed and calls welcome function.
while True:
    print ("Please Press Door Bell to Begin")
    if GPIO.wait_for_edge(23, GPIO.FALLING):
        welcomeFunc()
