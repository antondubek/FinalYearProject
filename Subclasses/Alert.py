"""
Author: Anthony Makepeace
File: Alert
"""

####
## Import libraries
####
import os
#import telegram
import telepot
from time import sleep
import picamera
from datetime import datetime
from telepot.loop import MessageLoop

####
## Initialisation
####
#bot = telegram.Bot(token='471263091:AAEFiEIp0Sd_ud0I0G7ARHzIsTE56TMmm2Y')
bot = telepot.Bot(token='471263091:AAEFiEIp0Sd_ud0I0G7ARHzIsTE56TMmm2Y')
chatID = 489826446


id = False
####
## Functions
####

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

def startLiveStream():
    os.system("cd /home/pi/RPi_Cam_Web_Interface ; ./start.sh")

def stopLiveStream():
    os.system("cd /home/pi/RPi_Cam_Web_Interface ; ./stop.sh")


def handle(msg):
    global id

    command = msg['text']

    print 'Got command: %s' % command

    if command.lower() == 'yes':
        bot.sendMessage(chatID, 'Yes Selected')
        id = True
        return

    elif command.lower() == 'no':
        bot.sendMessage(chatID, 'No Selected')
        id = False
        return

    else:
        bot.sendMessage(chatID, 'Sorry that command is not recognised please reply "yes" or "no"')
        return

def getID():
    return id


def SendAlert():
    label = takePicture()
    os.system("cd /home/pi/RPi_Cam_Web_Interface ; ./start.sh")
    bot.sendMessage(chatID, 'Someone is at your door! \n Reply yes or no \n View Stream @ http://raspberrypi3.local/html/index.php')
    bot.sendPhoto(chatID, open('/home/pi/DoorbellImages/%s.jpg' %label,'rb'), caption = label)
    MessageLoop(bot, handle).run_as_thread(timeout=10)
    sleep(10)

    '''updates = bot.get_updates()

    messages = [u.message.text for u in updates]
    print messages[-1]


    if messages[-1] == 'yes':
        print ('True')
        return True

    else:
        print ('False')
        return False'''

    decision = getID()

    if decision == True:
        bot.sendMessage(chatID, 'Allowing Entry')

    elif decision == False:
        bot.sendMessage(chatID, 'Declining Entry')

    return decision

####
## Main
####
