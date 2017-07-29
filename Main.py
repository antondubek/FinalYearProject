
####
## Import libraries
####
import RPi.GPIO as GPIO
import time



####
## Initialisation of Pins
####
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)



####
## Functions
####
