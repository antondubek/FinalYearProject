"""
Author: Anthony Makepeace
File: Alert
"""

####
## Import libraries
####
import sys
import httplib, urllib
sys.path.append('/home/pi/Pushover')
import PushoverCred

####
## Initialisation of Pins
####

####
## Functions
####
def pushNotification():
    conn = httplib.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": "a2dxu27tsra4gvh7m6kbd6pw8kdjuj",  # Insert app token here
        "user": "uf7i29tzpimm6bk9ram3p2ejujzb26",   # Insert user token here
        "html": "1",                                # 1 for HTML, 0 to disable
        "title": "Doorbell!",                       # Title of the message
        "message": "<b>Front Door</b> Someone is at your Door!",       # Content of the message
        "url": "http://google.com",                 # Link to be included in message
        "url_title": "View live stream",            # Text for the link
        "sound": "siren",                           # Define the sound played
      }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()
####
## Main
####
