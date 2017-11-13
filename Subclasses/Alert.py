"""
Author: Anthony Makepeace
File: Alert
"""

####
## Import libraries
####
import telepot
import time
from telepot.loop import MessageLoop

####
## Initialisation of Pins
####
bot = telepot.Bot('471263091:AAEFiEIp0Sd_ud0I0G7ARHzIsTE56TMmm2Y')
chatID = 489826446

id = 0
####
## Functions
####
def handle(msg):
    command = msg['text']

    print 'Got command: %s' % command

    if command == '/yes':
        bot.sendMessage(chatID, 'Yes Selected')
        id = 1
        print('True')

    elif command == '/no':
        bot.sendMessage(chatID, 'No Selected')
        id = 2
        print('False')

def SendAlert():
    bot.sendMessage(chatID, 'Someone is at your door! \n Reply /yes or /no')
    bot.sendPhoto(chatID, open('Subclasses/image.jpg','rb'), caption ='test')
    MessageLoop(bot, handle).run_as_thread(timeout=5)
    time.sleep(5)
    return id

####
## Main
####
