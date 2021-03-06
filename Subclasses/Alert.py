"""
Author: Anthony Makepeace
File: Alert
"""

####
## Import libraries
####
import os
import telepot
from time import sleep
import picamera
from datetime import datetime
from telepot.loop import MessageLoop
import RPi.GPIO as GPIO

####
## Initialisation
####

#Initialises and connects to the telegram doorbell bot
bot = telepot.Bot(token='471263091:AAEFiEIp0Sd_ud0I0G7ARHzIsTE56TMmm2Y')
chatID = 489826446

# Sets ID to default to False if no reply is received
id = 2

####
## Functions
####

# Takes a picture using camera and saves it as time and date
# Returns the picture name so can be sent by bot to user.
def takePicture():
    with picamera.PiCamera() as camera:
        camera.resolution = (1080, 720)
        now = datetime.now()
        label = now.strftime("%c")
        print ("Initialising Camera")
        camera.start_preview()
        sleep(2)
        os.chdir ("/home/pi/DoorbellImages")
        camera.capture("%s.jpg" %label)
        print ("Picture Taken")
        camera.close()
        return label

# Live Steam Control
def startLiveStream():
    os.system("cd /home/pi/RPi_Cam_Web_Interface ; ./start.sh")

def stopLiveStream():
    os.system("cd /home/pi/RPi_Cam_Web_Interface ; ./stop.sh")


# Bot message handler looking for yes or no response from user
# Sets ID True/False based on response which is relayed to Main
def handle(msg):
    global id
    global command

    command = msg['text']

    print 'Got command: %s' % command

    if command.lower() == 'yes':
        bot.sendMessage(chatID, 'Yes Selected')
        id = 1
        return

    elif command.lower() == 'no':
        bot.sendMessage(chatID, 'No Selected')
        id = 2
        return

    else:
        bot.sendMessage(chatID, 'Message Selected')
        id = 3
        return

def getID():
    return id

# Called function from main; takes picture, starts livestream, sends user picture and livestream link, listens for response
# for 10 seconds before then returning True or False to Main for processing.
def SendAlert():
    GPIO.output(2, GPIO.HIGH)
    label = takePicture()
    startLiveStream()
    bot.sendMessage(chatID, 'Someone is at your door! \n Reply yes or no for entry or with a message \n View Stream @ http://raspberrypi3.local/html/index.php')
    bot.sendPhoto(chatID, open('/home/pi/DoorbellImages/%s.jpg' %label,'rb'), caption = label)
    MessageLoop(bot, handle).run_as_thread(timeout=10)
    sleep(10)

    decision = getID()

    if decision == 1:
        bot.sendMessage(chatID, 'Allowing Entry')
        GPIO.output(2, GPIO.LOW)
        return True

    elif decision == 2:
        bot.sendMessage(chatID, 'Declining Entry')
        GPIO.output(2, GPIO.LOW)
        return False

    elif decision == 3:
        bot.sendMessage(chatID, 'Message Sent')
        GPIO.output(2, GPIO.LOW)
        print str(command)
        return str(command)




####
## Main
####
