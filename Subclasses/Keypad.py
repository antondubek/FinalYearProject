
import keypadLib
from time import sleep
from sys import exit

kp = keypadLib.keypad(columnCount = 4)

def digit():
    # Loop while waiting for a keypress
    digitPressed = None
    while digitPressed == None:
        digitPressed = kp.getKey()
    sleep(0.5)
    return str(digitPressed)
