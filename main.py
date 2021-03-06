"""
Author: Anthony Makepeace
File: Main
"""

####
## Import libraries
####

# System imports
import RPi.GPIO as GPIO
from time import sleep
import os
import sys

# Subclass Functions
from Subclasses.Keypad import digit
from Subclasses.RFID import checkRFIDTag
from Subclasses.Alert import SendAlert
from Subclasses.faceRecognition.box import checkFace

# Kivy screen imports
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

# GPIO BCM mode selected
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# RGB LED
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
GPIO.output(ButtonBlueLED_pin, GPIO.HIGH)

#Buzzer
Buzzer_pin = 24
GPIO.setup(Buzzer_pin, GPIO.OUT)
GPIO.output(Buzzer_pin, GPIO.LOW)

#Turn Flash OFF
Flash_pin = 2
GPIO.setup(Flash_pin, GPIO.OUT)
GPIO.output(Flash_pin, GPIO.LOW)

# Load in kivy kv file for screens.
Builder.load_file('Subclasses/welcomemenu.kv')


####
## Classes & Functions
####

# RFID Screen checks user RFID authentication
class RFIDScreen(Screen):

    # Initial Green and Red Background RGBA values
    red = NumericProperty(0)
    green = NumericProperty(0)

    # Function called on load of the screen.
    def Decision(self, *args):
        # Runs keypad code check from subclass returning T/F
        checkTag = checkRFIDTag()

        if isinstance(checkTag, str):
            Clock.schedule_once(partial(self.DoorOpenString, checkTag)) # DoorOpen Sequence
            Clock.schedule_once(DoorControl.DoorClosed, 10) # Door Closed Sequence
            Clock.schedule_once(DoorControl.KillApp, 15) # Back to initial Menu
            return

        # True Output sees text, background and LED used as an inidicator.
        elif checkTag == True:
            Clock.schedule_once(DoorControl.DoorOpen) # DoorOpen Sequence
            Clock.schedule_once(DoorControl.DoorClosed, 10) # Door Closed Sequence
            Clock.schedule_once(DoorControl.KillApp, 15) # Back to initial Menu
            return

        # False output calls incorrect text function and resets
        elif checkTag == False:
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

    # Sets Screen green and says welcome and the name of the person
    def DoorOpenString(self, name, *args):
        print ("DEBUG: Door open name = %s" %name)
        self.the_text.text = "Welcome %s" %(name)
        self.green = 1
        LEDS("GREEN")

# Keypad Screen checks user keypad input for authentication
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

# Alert Screen sends telegram notification and runs live stream
class AlertSomeoneScreen(Screen):

    # Initial Green and Red Background RGBA values
    red = NumericProperty(0)
    green = NumericProperty(0)

    def Push(self, *args):

        # SendAlert Returns True or False for authentication
        decision = SendAlert()
        print decision

        if decision == True:
            Clock.schedule_once(DoorControl.DoorOpen) # LED Green
            Clock.schedule_once(DoorControl.DoorClosed, 30) # LED RED
            Clock.schedule_once(self.stopLiveStream, 35)
            Clock.schedule_once(DoorControl.KillApp, 35) # Back to initial Menu

        elif isinstance(decision, str):
            Clock.schedule_once(partial(self.RejectString, decision)) # DoorOpen Sequence
            #Clock.schedule_once(DoorControl.DoorClosed, 30) # Door Closed Sequence
            Clock.schedule_once(self.stopLiveStream, 35)
            Clock.schedule_once(DoorControl.KillApp, 35) # Back to initial Menu
            return

        else:
            Clock.schedule_once(self.entryDeclined)
            Clock.schedule_once(self.stopLiveStream, 30)
            Clock.schedule_once(DoorControl.KillApp, 30)

    # Entry declined prints screen text and sets background and RGB colour
    def entryDeclined(self, *args):
        self.the_text.text = "Entry Declined"
        self.red = 1
        LEDS("RED")

    # Kills live stream started within alert so that camera is available
    def stopLiveStream(self, *args):
        os.system("cd /home/pi/RPi_Cam_Web_Interface ; ./stop.sh")

    # Resets the text of the screen for next usage
    def textReset(self, *args):
        self.the_text.text = "Please Look at the Camera \n Wait for Response"
        self.green = 0
        self.red = 0

    # Sets Screen green and says welcome and the name of the person
    def RejectString(self, message, *args):
        print ("DEBUG: Message = %s" %message)
        self.the_text.text = "%s" %(message)
        self.red = 1
        LEDS("RED")


# Runs facial recognition program for authentication
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
    # Sets on screen text as door open with a green background and LEDS
    def DoorOpen(self, *args):
        print ("Door Open : Please Enter")
        MyScreenManager.current_screen.the_text.text = "Door Open"
        MyScreenManager.current_screen.green = 1
        LEDS("GREEN")
        return

    # Sets on screen text as door closed with a red background and LEDS
    def DoorClosed(self, *args):
        print ("Door Closed")
        MyScreenManager.current_screen.the_text.text = "Door Closed"
        MyScreenManager.current_screen.green = 0
        MyScreenManager.current_screen.red = 1
        LEDS("RED")
        return

    # Kills the running app and returns to the selection menu
    def KillApp(self, *args):
        MyScreenManager.current = 'InitialMenu'
        App.get_running_app().stop()
        return

# Selection Screen loaded with authentication options
class InitialMenu(Screen):
    pass

# Creation of a ScreenManager to host kivy screens.
MyScreenManager = ScreenManager()
MyScreenManager.add_widget(InitialMenu(name='InitialMenu'))
MyScreenManager.add_widget(RFIDScreen(name='RFID'))
MyScreenManager.add_widget(KeypadScreen(name='Keypad'))
MyScreenManager.add_widget(AlertSomeoneScreen(name='Alert'))
MyScreenManager.add_widget(FacialRecognitionScreen(name='FaceRecog'))

# Building the kivy app and loading the ScreenManager
class menu(App):
    def build(self):
        return MyScreenManager

# Welcome Message Box Layout displayed when welcomeText App ran
class WelcomeMessage(BoxLayout):
    pass

# Welcome APP loaded first to load WelcomeMessage
# App killed ASAP so screenmanager can be ran
class welcomeText(App):
    def build(self):
        Clock.schedule_once(DoorControl.KillApp, 3)
        return WelcomeMessage()

# Functions controlling switch and internal RGB lighting
def LEDS(status):
    if status == "GREEN":
        GPIO.output(BlueLED_pin, GPIO.LOW)
        GPIO.output(GreenLED_pin,GPIO.HIGH)
        GPIO.output(BlueLED_pin, GPIO.LOW)
        GPIO.output(ButtonRedLED_pin,GPIO.HIGH)
        GPIO.output(ButtonGreenLED_pin,GPIO.LOW)
        GPIO.output(ButtonBlueLED_pin, GPIO.HIGH)
        GPIO.output(Buzzer_pin, GPIO.HIGH)
    elif status == "RED":
        GPIO.output(GreenLED_pin,GPIO.LOW)
        GPIO.output(RedLED_pin, GPIO.HIGH)
        GPIO.output(BlueLED_pin, GPIO.LOW)
        GPIO.output(ButtonRedLED_pin,GPIO.LOW)
        GPIO.output(ButtonGreenLED_pin,GPIO.HIGH)
        GPIO.output(ButtonBlueLED_pin, GPIO.HIGH)
        GPIO.output(Buzzer_pin, GPIO.LOW)
    elif status == "BLUE":
        GPIO.output(GreenLED_pin,GPIO.LOW)
        GPIO.output(RedLED_pin, GPIO.LOW)
        GPIO.output(BlueLED_pin, GPIO.HIGH)
        GPIO.output(ButtonRedLED_pin,GPIO.HIGH)
        GPIO.output(ButtonGreenLED_pin,GPIO.HIGH)
        GPIO.output(ButtonBlueLED_pin, GPIO.LOW)
        GPIO.output(Buzzer_pin, GPIO.LOW)

    # Debug if LED function passed invalid arguments
    else:
        print ("DEBUG: Please call function LEDS('RED/GREEN/BLUE')")



####
## Main
####

# Polls for when button is pressed and calls welcome function.
while True:

    # Sets the Switch and internal RGB as Blue
    LEDS("BLUE")

    # Runs welcomeText APP displaying WelcomeMessage
    # App quits ASAP so that rest of program can run
    welcomeText().run()

    # Debug Console Output
    print ("Please Press Door Bell to Begin")

    # Waits for piezo switch to be grounded and triggers APP
    if GPIO.wait_for_edge(23, GPIO.FALLING):
        menu().run()
