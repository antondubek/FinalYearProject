"""
Author: Anthony Makepeace
File: Keypad
"""

####
## Import libraries
####
import RPi_GPIO
from time import sleep
from sys import exit

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

def FourDigitCodeCheck():

    # Setup variables
    attempt = "0000"
    passcode = "1234"
    counter = 0
    attemptCounter = 0
    attemptsAllowed = 3

    print ("Enter 4 Digit Pin Code")

    # Loop while waiting for a keypress
    while True:

        """ If attemptCounter < attemptsAllowed """
        if (attemptCounter < attemptsAllowed):
            # Loop to get a pressed digit
            digit = None
            while digit == None:
                digit = kp.getKey()

                # Print the result
            print "Digit Entered:       %s"%digit
            attempt = (attempt[1:] + str(digit))
            print "Attempt value:       %s"%attempt

            # Check for passcode match
            if (attempt == passcode):
                print "Your code was correct, goodbye."
                return True

            else:
                counter += 1
                print "Entered digit count: %s"%counter

                if (counter >= 4):
                    print "Incorrect code!"
                    sleep(3)
                    print "Try Again"
                    sleep(1)
                    counter = 0
                    attemptCounter += 1


            sleep(0.5)

        else:
            print ("You have exceeded the number of attempts")
            return False


####
## Main
####
