import sys
from time import sleep
import RPi.GPIO as GPIO

rPin = 27
gPin = 23
bPin = 22
LIGHTOFF = -1

def lightOn(pin):
#    print('light on')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    # !!!!Problem is here!!!!
    GPIO.output(pin, GPIO.HIGH)

def lightOff(pin):
 #   print('light off')
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def killLight():
    lightOff(rPin)
    lightOff(gPin)
    lightOff(bPin)

def blink(pin, sec = 1, currLight = LIGHTOFF):
    if currLight != LIGHTOFF:
        lightOff(currLight)
    for i in range(2*sec):
    	lightOn(pin)
    	sleep(0.5)
    	lightOff(pin)
    	sleep(0.5)
    lightOn(currLight)
