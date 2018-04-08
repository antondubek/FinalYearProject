"""
Author: Anthony Makepeace
File: Alert
"""

####
## Import libraries
####
import keypadLib
from time import sleep
from sys import exit

####
## Initialisation
####

# Defines the keypad as a 4 column pad
kp = keypadLib.keypad(columnCount = 4)

####
## Functions
####

# Waits for a digit press and returns it as a string
def digit():
    # Loop while waiting for a keypress
    digitPressed = None
    while digitPressed == None:
        digitPressed = kp.getKey()
    sleep(0.5)
    return str(digitPressed)
