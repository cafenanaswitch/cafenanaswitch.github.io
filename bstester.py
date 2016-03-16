
#Import all the libraries
import threading, re, time, os
from time import strftime
from BeautifulSoup import BeautifulSoup
import RPi.GPIO as GPIO

htmlFile = "/home/pi/nanaswitch/cafenanaswitch.github.io/index.html"
with open(htmlFile, "r+") as f:
    originalhtml = f.read()
    soup = BeautifulSoup(originalhtml)
    div = soup.find('div', {'id': 'statusString'})
    div.string = "Testing!!!!!!" 
    f.close

newhtml = soup.prettify("utf-8")
with open(htmlFile, "wb") as outfile:
    outfile.write(newhtml)
    outfile.close
