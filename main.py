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
import sys
from Subclasses.Keypad import FourDigitCodeCheck
from Subclasses.RFID import checkRFIDTag
from Subclasses.Images import takePicture

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.clock import Clock

####
## Initialisation of Pins
####

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LED's
RedLED_pin = 25
GreenLED_pin = 18
GPIO.setup(GreenLED_pin,GPIO.OUT)
GPIO.setup(RedLED_pin,GPIO.OUT)
GPIO.output(RedLED_pin,GPIO.HIGH)
GPIO.output(GreenLED_pin,GPIO.LOW)

# Buttons
# Main Red
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# First Button (L to R)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Second Button (L to R)
GPIO.setup(1, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# PIR


####
## Functions
####


# Welcome Message & Choice
"""
def welcomeFunc():
    os.system('clear')
    print ("Welcome to Smart Doorbell")
    sleep(3)
    #takePicture()
    os.system('clear')
    print ("Please choose an option: ")
    print ("1. Alert Someone")
    print ("2. Keypad")
    print ("3. RFID")

    # Creates values to be cycled through by user.
    options = ["1", "2", "3"]
    helperX = 0

    sys.stdout.write("Option: %s \r" %options[helperX])
    sys.stdout.flush()




    while True:

        # If right button pressed then option increases by 1
        if GPIO.input(1) == GPIO.LOW and helperX != (len(options) - 1):
            helperX += 1
            #print "Option: %s " %options[helperX]
            sys.stdout.write("Option: %s \r" %options[helperX])
            sys.stdout.flush()

        # If right button pressed then option increases by 1
        if GPIO.input(5) == GPIO.LOW and helperX != 0:
            helperX -= 1
            #print "Option: %s " %options[helperX]
            sys.stdout.write("Option: %s \r" %options[helperX])
            sys.stdout.flush()

        # Red button press confirms selection
        if GPIO.input(23) == GPIO.LOW:
            #print ("You chose %s" %x)
            choiceProcessor(helperX)
            return

        # Debounce Sleep for Buttons
        sleep(0.2)

        # Option 3: Keypad
        #if GPIO.input(5) == GPIO.LOW:
        #    choiceProcessor(3)
        #    return

        # Option 4: RFID
        #if GPIO.input(1) == GPIO.LOW:
        #    choiceProcessor(4)
        #    return

    #choice = int(raw_input("Please input number of choice: "))
    #choiceProcessor(choice)

    """

Builder.load_file('Subclasses/welcomemenu.kv')

class DoorOpenScreen(Screen):
    pass

class RFIDScreen(Screen):

    def Decision(self, *args):
        rfidOutput = checkRFIDTag()
        text = self.ids['rfidtext']
        if rfidOutput == True:
            text.text = 'Door Open Please Enter'
            doorOpen()
            text.text = 'RFID Authentication\n Please Present Keycard / Fob'
            MyScreenManager.current = 'InitialMenu'
            return

class KeypadScreen(Screen):
    keypadTextTest = StringProperty("Please Input 4 Digit Passcode")

    def Decision(self, *args):
        keypadOutput = FourDigitCodeCheck()
        if keypadOutput == True:
            Clock.schedule_once(self.textOpen)
            Clock.schedule_once(DoorControl.DoorOpen)
            Clock.schedule_once(self.textClosed, 5)
            Clock.schedule_once(DoorControl.DoorClosed, 5)
            Clock.schedule_once(DoorControl.ResetMenu, 6)
            return

    def textOpen(self, *args):
        self.keypadTextTest = "Door Open"

    def textClosed(self, *args):
        self.keypadTextTest = "Door Closed"


class AlertSomeoneScreen(Screen):
    pass

class InitialMenu(Screen):
    def AlertSomeone(self, *args):
        print 'Alert'


    def Keypad(self, *args):
        print 'Keypad'

class DoorControl(Screen):
    def DoorOpen(self, *args):
        print ("Door Open : Please Enter")
        GreenLED("ON")
        return

    def DoorClosed(self, *args):
        GreenLED("OFF")
        return

    def ResetMenu(self, *args):
        MyScreenManager.current = 'InitialMenu'


#class MyScreenManager(ScreenManager):
#    pass
MyScreenManager = ScreenManager()
MyScreenManager.add_widget(InitialMenu(name='InitialMenu'))
MyScreenManager.add_widget(RFIDScreen(name='RFID'))
MyScreenManager.add_widget(KeypadScreen(name='Keypad'))
MyScreenManager.add_widget(DoorOpenScreen(name='DoorOpen'))


class introduction(App):
    def build(self):
        #self.load_kv('Subclasses/welcomemenu.kv')
        #return InitialMenu()
        return MyScreenManager



# Takes choice and executes relevant function.
def choiceProcessor(choiceNo):
    if choiceNo == 0:
        print ("Alerting Someone Now..")
        print ("Please Wait...")
        #Call alert function
        sleep(2)
        return

    elif choiceNo == 1:
        print ("Initialising Keyapad Function...")
        print ("Please Wait...")
        #Call keypad function
        keypadOutput = FourDigitCodeCheck()
        if keypadOutput == True:
            doorOpen()
            return

    elif choiceNo == 2:
        print ("Initialising RFID Function...")
        print ("Please Wait...")
        #Call RFID function
        rfidOutput = checkRFIDTag()
        if rfidOutput == True:
            doorOpen()
            return

# Function to open / release door. LED for bug fixing
def doorOpen1():
    print ("Door Open : Please Enter")
    GreenLED("ON")
    #sleep(5)
def doorOpen2():
    GreenLED("OFF")
    return

def GreenLED(status):
    if status == "ON":
        GPIO.output(RedLED_pin, GPIO.LOW)
        GPIO.output(GreenLED_pin,GPIO.HIGH)
    elif status == "OFF":
        GPIO.output(GreenLED_pin,GPIO.LOW)
        GPIO.output(RedLED_pin, GPIO.HIGH)
    else:
        print ("DEBUG: Please declare LED Green status ON/OFF")



####
## Main
####

# Polls for when button is pressed and calls welcome function.
while True:
    print ("Please Press Door Bell to Begin")
    if GPIO.wait_for_edge(23, GPIO.FALLING):
        introduction().run()
