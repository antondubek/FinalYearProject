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
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
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

# Load in kivy kv file for screens.
Builder.load_file('Subclasses/welcomemenu.kv')


####
## Classes & Functions
####

# RFID Screen loaded on option select
class RFIDScreen(Screen):
    pass

# Keypad Screen loaded on option select
class KeypadScreen(Screen):
    # Initial Text on the screen
    keypadText = StringProperty("Please Input 4 Digit Passcode")
    # Initial Green and Red Background RGBA values
    red = NumericProperty(0)
    green = NumericProperty(0)

    # Function called on load of the screen.
    def Decision(self, *args):
        # Runs keypad code check from subclass returning T/F
        keypadOutput = FourDigitCodeCheck()
        # True Output sees text, background and LED used as an inidicator.
        if keypadOutput == True:
            Clock.schedule_once(self.textOpen) # Door Open + Green Background
            Clock.schedule_once(DoorControl.DoorOpen) # LED Green
            Clock.schedule_once(self.textClosed, 10) # Door Closed + Red Background
            Clock.schedule_once(DoorControl.DoorClosed, 10) # LED RED
            Clock.schedule_once(DoorControl.ResetMenu, 15) # Back to initial Menu
            return

        elif keypadOutput == False:
            Clock.schedule_once(self.textIncorrect)
            Clock.schedule_once(DoorControl.ResetMenu, 10)


    def textOpen(self, *args):
        self.keypadText = "Door Open"
        self.green = 1

    def textClosed(self, *args):
        self.keypadText = "Door Closed"
        self.green = 0
        self.red = 1

    def textIncorrect(self, *args):
        self.keypadText = "Incorrect Code \n Please try another option"
        self.red = 1

    def textReset(self, *args):
        self.keypadText = "Please Input 4 Digit Passcode"
        self.green = 0
        self.red = 0



class AlertSomeoneScreen(Screen):
    pass

class InitialMenu(Screen):
    pass

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
        return

# Creation of a ScreenManager to host kivy screens.
MyScreenManager = ScreenManager()
MyScreenManager.add_widget(InitialMenu(name='InitialMenu'))
MyScreenManager.add_widget(RFIDScreen(name='RFID'))
MyScreenManager.add_widget(KeypadScreen(name='Keypad'))

# Building the kivy app and loading the ScreenManager
class introduction(App):
    def build(self):
        return MyScreenManager

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
