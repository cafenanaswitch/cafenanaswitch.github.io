# Python code for Nanaswitch project
# Checks status of switch and updates github page accordingly

# David Verdi
# 3/15/2016
# Code based off a similar project by DIY Tryin
# https://www.youtube.com/watch?v=ZszlVVY1LXo

#Import all the libraries
import threading, re, time, os
from time import strftime
from BeautifulSoup import BeautifulSoup
import RPi.GPIO as GPIO

#Setup GPIO Pins
GPIO.setmode(GPIO.BCM)

# Switch Pin is HIGH when cafe open
# Switch Pin is LOW when cafe closed
GPIO.setup(17, GPIO.IN)

#LED Pins
GPIO.setup(23, GPIO.IN) #Green LED
GPIO.setup(24, GPIO.IN) #Red LED

#Set refresh period to 1 second
pollTime = 3

# cafestatus 1 when cafe open
# cafestatus 0 when cafe closed
# cafestatus 2 to initialize
cafestatus = 2

htmlFile = "/home/pi/nanaswitch/cafenanaswitch.github.io/index.html"

def checkStatus():
    # Will call f() again in pollTime seconds
    threading.Timer(pollTime, checkStatus).start()
    
    if(GPIO.input(17)):
        # Cafe is open
        if (cafestatus != 1):
            GPIO.output(24, GPIO.LOW)
            GPIO.output(23, GPIO.HIGH)
            cafestatus = 1
            updateHTML(1)

    elif( !(GPIO.input(17))):
        # Cafe is closed
        if (cafestatus != 0):
            GPIO.output(24, GPIO.HIGH)
            GPIO.output(23, GPIO.LOW)
            cafestatus = 0
            updateHTML(0)
            
def updateHTML(statuscode):
    # Updates HTML file and pushes it to github.io page
    if(statuscode == 1):
        replacestring = "Cafe Nana is currently OPEN! =) \n Switch last updated at " + strftime("%H:%M:%S  %Y-%m-%d")
    elif(statuscode == 0):
        replacestring = "Cafe Nana is now CLOSED. =( \n Switch last updated at " + strftime("%H:%M:%S  %Y-%m-%d")

    with open(htmlFile, "r+") as f:
        originalhtml = f.read()
        soup = BeautifulSoup(originalhtml)
        div = soup.find('div', {'id': 'statusString'})
        div.string = replacestring
        f.close

    newhtml = soup.prettify("utf-8")
    with open(htmlFile, "wb") as outfile:
        outfile.write(newhtml)
        outfile.close

    # stage, commit, and push changes to github:
    os.system('/home/pi/nanaswitch/cafenanaswitch.github.io/gitpusher.sh')

checkStatus()

