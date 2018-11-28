import RPi.GPIO as GPIO
import sys
sys.path.insert(0,'/home/pi/Desktop/PythonCode/DHT11_Python/')
import dht11

def getInfo(pin=17):
  # initialize GPIO
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BCM)

  # read data using pin 17
  instance = dht11.DHT11(pin)
  result = instance.read()
  while not result.is_valid():
    result = instance.read()
  return [result.temperature, result.humidity]
