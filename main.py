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
from Subclasses.Keypad import digit
from Subclasses.RFID import checkRFIDTag
from Subclasses.Images import takePicture
from Subclasses.Alert import SendAlert
from Subclasses.faceRecognition.box import checkFace

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.clock import Clock

from functools import partial

####
## Initialisation of Pins
####

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LED's
RedLED_pin = 18
GreenLED_pin = 15
BlueLED_pin = 14
GPIO.setup(GreenLED_pin,GPIO.OUT)
GPIO.setup(RedLED_pin,GPIO.OUT)
GPIO.setup(BlueLED_pin, GPIO.OUT)
GPIO.output(RedLED_pin,GPIO.LOW)
GPIO.output(GreenLED_pin,GPIO.LOW)
GPIO.output(BlueLED_pin, GPIO.HIGH)

# Button
# Piezo Trigger
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# RGB Setup
ButtonRedLED_pin = 4
ButtonGreenLED_pin = 17
ButtonBlueLED_pin = 3
GPIO.setup(ButtonGreenLED_pin,GPIO.OUT)
GPIO.setup(ButtonRedLED_pin,GPIO.OUT)
GPIO.setup(ButtonBlueLED_pin, GPIO.OUT)
# Pull LOW = ON HIGH = OFF
GPIO.output(ButtonRedLED_pin,GPIO.HIGH)
GPIO.output(ButtonGreenLED_pin,GPIO.HIGH)
GPIO.output(ButtonBlueLED_pin, GPIO.LOW)

#Buzzer
Buzzer_pin = 24
GPIO.setup(Buzzer_pin, GPIO.OUT)
GPIO.output(Buzzer_pin, GPIO.LOW)

#Turn Flash OFF
GPIO.setup(2, GPIO.OUT)
GPIO.output(2, GPIO.LOW)

# Load in kivy kv file for screens.
Builder.load_file('Subclasses/welcomemenu.kv')


####
## Classes & Functions
####

# RFID Screen loaded on option select
class RFIDScreen(Screen):

    # Initial Green and Red Background RGBA values
    red = NumericProperty(0)
    green = NumericProperty(0)

    # Function called on load of the screen.
    def Decision(self, *args):
        # Runs keypad code check from subclass returning T/F
        keypadOutput = checkRFIDTag()
        # True Output sees text, background and LED used as an inidicator.
        if keypadOutput == True:
            Clock.schedule_once(DoorControl.DoorOpen) # DoorOpen Sequence
            Clock.schedule_once(DoorControl.DoorClosed, 10) # Door Closed Sequence
            Clock.schedule_once(DoorControl.KillApp, 15) # Back to initial Menu
            return

        # False output calls incorrect text function and resets
        elif keypadOutput == False:
            Clock.schedule_once(self.textIncorrect)
            Clock.schedule_once(DoorControl.KillApp, 7)

    # Function changing text to the not Recognised text
    def textIncorrect(self, *args):
        self.the_text.text = "RFID Not Recognised"
        self.red = 1
        LEDS("RED")

    # Reset function called pre enter of the page. Put Default text here.
    def textReset(self, *args):
        self.the_text.text = "Please present card to keypad"
        self.green = 0
        self.red = 0

# Keypad Screen loaded on option select
class KeypadScreen(Screen):

    # Initial Green and Red Background RGBA values
    red = NumericProperty(0)
    green = NumericProperty(0)

    # Function called on load of the screen.
    def Decision(self, *args):

        # Creates password and iterates through to get 4 digit string.
        password = ''
        for i in range(4):
            pin = digit()
            print(pin)
            password += pin
            #self.the_pin.text += pin

        print(password) # Debug

        # Typed password is correct sees text, background and LED used as an inidicator.
        if password == "1234":
            Clock.schedule_once(DoorControl.DoorOpen) # LED Green
            Clock.schedule_once(DoorControl.DoorClosed, 10) # LED RED
            Clock.schedule_once(DoorControl.KillApp, 15) # Back to initial Menu
            return

        # If password is wrong calls incorrect function and resets.
        else:
            Clock.schedule_once(partial(self.textIncorrect, password))
            Clock.schedule_once(DoorControl.KillApp, 10)

    # Function changing text to the not wrong pin text
    def textIncorrect(self, password, *args):
        self.the_text.text = "Incorrect Code: " + password
        self.red = 1
        LEDS("RED")

    # Reset function called pre enter of the page. Put Default text here.
    def textReset(self, *args):
        self.the_text.text = "Please Input 4 Digit Passcode"
        self.the_pin.text = ""
        self.green = 0
        self.red = 0


class AlertSomeoneScreen(Screen):

    red = NumericProperty(0)
    green = NumericProperty(0)

    def Push(self, *args):

        #SendAlert Returns int 1 for yes, 2 for no, 0 for no response
        decision = SendAlert()
        print decision

        if decision == True:
            Clock.schedule_once(DoorControl.DoorOpen) # LED Green
            Clock.schedule_once(DoorControl.DoorClosed, 30) # LED RED
            Clock.schedule_once(self.stopLiveStream, 35)
            Clock.schedule_once(DoorControl.KillApp, 35) # Back to initial Menu

        else:
            Clock.schedule_once(self.entryDeclined)
            Clock.schedule_once(self.stopLiveStream, 30)
            Clock.schedule_once(DoorControl.KillApp, 30)

    def entryDeclined(self, *args):
        self.the_text.text = "Entry Declined"
        self.red = 1
        LEDS("RED")

    def stopLiveStream(self, *args):
        os.system("cd /home/pi/RPi_Cam_Web_Interface ; ./stop.sh")

    def textReset(self, *args):
        self.the_text.text = "Please Look at the Camera \n Wait for Response"
        self.green = 0
        self.red = 0


class InitialMenu(Screen):
    pass

class FacialRecognitionScreen(Screen):

    red = NumericProperty(0)
    green = NumericProperty(0)

    def FacialRecognition(self, *args):
        decision = checkFace()
        if decision == True:
            Clock.schedule_once(DoorControl.DoorOpen) # DoorOpen Sequence
            Clock.schedule_once(DoorControl.DoorClosed, 30) # Door Closed Sequence
            Clock.schedule_once(DoorControl.KillApp, 35) # Back to initial Menu
            return

        # False output calls incorrect text function and resets
        elif decision == False:
            Clock.schedule_once(self.textIncorrect)
            Clock.schedule_once(DoorControl.KillApp, 30)

    # Function changing text to the not Recognised text
    def textIncorrect(self, *args):
        self.the_text.text = "Face Not Recognised"
        self.red = 1


    def textReset(self, *args):
        self.the_text.text = "Please Look at the Camera"
        self.green = 0
        self.red = 0

class DoorControl(Screen):
    def DoorOpen(self, *args):
        print ("Door Open : Please Enter")
        MyScreenManager.current_screen.the_text.text = "Door Open"
        MyScreenManager.current_screen.green = 1
        LEDS("GREEN")
        return

    def DoorClosed(self, *args):
        print ("Door Closed : Please Enter")
        MyScreenManager.current_screen.the_text.text = "Door Closed"
        MyScreenManager.current_screen.green = 0
        MyScreenManager.current_screen.red = 1
        LEDS("RED")
        return

    def KillApp(self, *args):
        MyScreenManager.current = 'InitialMenu'
        App.get_running_app().stop()
        return

# Creation of a ScreenManager to host kivy screens.
MyScreenManager = ScreenManager()
MyScreenManager.add_widget(InitialMenu(name='InitialMenu'))
MyScreenManager.add_widget(RFIDScreen(name='RFID'))
MyScreenManager.add_widget(KeypadScreen(name='Keypad'))
MyScreenManager.add_widget(AlertSomeoneScreen(name='Alert'))
MyScreenManager.add_widget(FacialRecognitionScreen(name='FaceRecog'))

# Building the kivy app and loading the ScreenManager
class introduction(App):
    def build(self):
        return MyScreenManager


class WelcomeMessage(BoxLayout):
    pass

class welcomeText(App):
    def build(self):
        Clock.schedule_once(DoorControl.KillApp, 3)
        return WelcomeMessage()


def LEDS(status):
    if status == "GREEN":
        GPIO.output(BlueLED_pin, GPIO.LOW)
        GPIO.output(GreenLED_pin,GPIO.HIGH)
        GPIO.output(BlueLED_pin, GPIO.LOW)
        GPIO.output(ButtonRedLED_pin,GPIO.HIGH)
        GPIO.output(ButtonGreenLED_pin,GPIO.LOW)
        GPIO.output(ButtonBlueLED_pin, GPIO.HIGH)
        #GPIO.output(Buzzer_pin, GPIO.HIGH)
    elif status == "RED":
        GPIO.output(GreenLED_pin,GPIO.LOW)
        GPIO.output(RedLED_pin, GPIO.HIGH)
        GPIO.output(BlueLED_pin, GPIO.LOW)
        GPIO.output(ButtonRedLED_pin,GPIO.LOW)
        GPIO.output(ButtonGreenLED_pin,GPIO.HIGH)
        GPIO.output(ButtonBlueLED_pin, GPIO.HIGH)
        #GPIO.output(Buzzer_pin, GPIO.LOW)
    elif status == "BLUE":
        GPIO.output(GreenLED_pin,GPIO.LOW)
        GPIO.output(RedLED_pin, GPIO.LOW)
        GPIO.output(BlueLED_pin, GPIO.HIGH)
        GPIO.output(ButtonRedLED_pin,GPIO.HIGH)
        GPIO.output(ButtonGreenLED_pin,GPIO.HIGH)
        GPIO.output(ButtonBlueLED_pin, GPIO.LOW)
        #GPIO.output(Buzzer_pin, GPIO.LOW)

    else:
        print ("DEBUG: Please declare LED Green status ON/OFF")



####
## Main
####

# Polls for when button is pressed and calls welcome function.
while True:

    LEDS("BLUE")

    welcomeText().run()

    print ("Please Press Door Bell to Begin")
    if GPIO.wait_for_edge(23, GPIO.FALLING):
        introduction().run()
