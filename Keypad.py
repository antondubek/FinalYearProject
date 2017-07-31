"""
Author: Anthony Makepeace
File: Keypad
"""

####
## Import libraries
####
import keypadLib

####
## Initialisation of Pins
####

"""
Pins initialised within keypadLib.py
Set pins on line 29 & 30
Rows : 18 23 24 25
Columns: 4 17 27 26
"""

# Creates keyboard kp.
kp = RPi_GPIO.keypad(columnCount = 4)

####
## Functions
####
def digit():
    # Loop while waiting for a keypress
    r = None
    while r == None:
        r = kp.getKey()
    return r

def getFourDigitCode():
    # Getting digit 1, printing it, then sleep to allow the next digit press.
    d1 = digit()
    print d1
    sleep(1)

    d2 = digit()
    print d2
    sleep(1)

    d3 = digit()
    print d3
    sleep(1)

    d4 = digit()
    print d4

    # printing out the assembled 4 digit code.
    # print "You Entered %s%s%s%s "%(d1,d2,d3,d4)
    return ("%s%s%s%s") %(d1,d2,d3,d4)


####
## Main
####
