#!/usr/bin/env python
import RPi.GPIO as GPIO
import RGBController as rgb


KnockPin = 24
notify = True

def setup():
	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
	GPIO.setup(KnockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led

def swDND(ev = None):
	'''
	toggle notify variable
	ON -> blue light
	OFF -> red light
	'''
	global notify
	print('notify: ' + str(notify) + '->' + str(not notify))
	notify = not notify
	if notify == False:
		killLight()
		lightOn(rPin)
	else:
		killLight()
		lightOn(bPin)

def detectDND():
	GPIO.add_event_detect(KnockPin, GPIO.FALLING, callback=swDND, bouncetime=1000) # wait for falling
	while True:
		pass   # Don't do anything

def destroy():
	'''
	should be added to clear GPIO pins' setup
	'''
	GPIO.output(LedPin, GPIO.LOW)     # led off
	GPIO.cleanup()                     # Release resource

# if __name__ == '__main__':     # Program start from here
# 	setup()
# 	try:
# 		detectDND()
# 	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
# 		destroy()
