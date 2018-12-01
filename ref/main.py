# coding: utf-8
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import RPi.GPIO as GPIO
import thread


# import self define python code
import DHT11
import RGBController as RGB
import Picture
import SendEmail


# ███████ ██    ██ ███    ██  ██████ ████████ ██  ██████  ███    ██ ███████
# ██      ██    ██ ████   ██ ██         ██    ██ ██    ██ ████   ██ ██
# █████   ██    ██ ██ ██  ██ ██         ██    ██ ██    ██ ██ ██  ██ ███████
# ██      ██    ██ ██  ██ ██ ██         ██    ██ ██    ██ ██  ██ ██      ██
# ██       ██████  ██   ████  ██████    ██    ██  ██████  ██   ████ ███████



#Custom MQTT message callback
def userRequest(client, userdata, message):

    global notify
    global currLight
    global lastTemp
    global lastHumi

    print('Msg Received')
    # print(message.payload)

    # handle the request from user
    msg = ''
    data = json.loads(message.payload)

    # t store temperature, h store humidity
    #temperature ,humidity = DHT11.getInfo(17)
    temperature = lastTemp
    humidity = lastHumi

    # get true false from aws publish message
    getTemperature = data['temperature']
    getHumidity = data['humidity']
    getNotify = data['notify']

    # user disable to notify function
    if getNotify != notify:
        # code to disable the notify function
        changeNotify()

    #
    if notify:
        if getTemperature:
            msg = "Temperature: " + str(temperature) + "\n"
        if getHumidity:
            msg += "Humidity: " + str(humidity)
    else:
        return

    pic_path = Picture.takePic(currLight)
    pic_path = Picture.drawOnPic(pic_path, msg)

    SendEmail.send("Here is the picture from Home", pic_path)


def changeNotify(ev = None):
	'''
	toggle notify variable
	ON -> blue light
	OFF -> red light
	'''
	global notify
	print('notify: ' + str(notify) + '->' + str(not notify))
	notify = not notify
	if notify == False:
		RGB.killLight()
		RGB.lightOn(RGB.rPin)
	else:
		RGB.killLight()
		RGB.lightOn(RGB.gPin)


def sendNotification(msg):
    # assemble the message which will be attched to the image
    msgOnPic = "Temperature: " + str(lastTemp) + "\nHumidity: " + str(lastHumi)
    picturePath = Picture.takePic(currLight)
    picturePath = Picture.drawOnPic(picturePath, msgOnPic)
    SendEmail.send(msg, picturePath)


    # ██ ███    ██ ██ ████████ ██  █████  ██      ██ ███████ ███████
    # ██ ████   ██ ██    ██    ██ ██   ██ ██      ██    ███  ██
    # ██ ██ ██  ██ ██    ██    ██ ███████ ██      ██   ███   █████
    # ██ ██  ██ ██ ██    ██    ██ ██   ██ ██      ██  ███    ██
    # ██ ██   ████ ██    ██    ██ ██   ██ ███████ ██ ███████ ███████


try:




	clientId = "anyID"
	host = "ajpw4dtxmu8kd.iot.us-east-2.amazonaws.com"
	port = 8883
	rootCAPath = "/home/pi/Desktop/Cert/vert.txt"
	privateKeyPath = "/home/pi/Desktop/Cert/private.key"
	certificatePath = "/home/pi/Desktop/Cert/cert.crt"
	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId) #clientId can be anything
	myAWSIoTMQTTClient.configureEndpoint(host, port) #host is your Pi’s AWS IoT Endpoint, port is 8883
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

	#AWSIoTMQTTClient connection configuration
	myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
	myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
	myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
	myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
	myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

	#Connect and subscribe to AWS IoT
	topic = "Test1"

	myAWSIoTMQTTClient.connect()
	myAWSIoTMQTTClient.subscribe(topic, 1, userRequest)

	# ----------------------main function----------------------

	# ███    ███  █████  ██ ███    ██
	# ████  ████ ██   ██ ██ ████   ██
	# ██ ████ ██ ███████ ██ ██ ██  ██
	# ██  ██  ██ ██   ██ ██ ██  ██ ██
	# ██      ██ ██   ██ ██ ██   ████


	# ----------------------Emails----------------------
	# Sends email to user if following condition meets
	# 1. passed certain time
	# 2. temperature or humidity grow or drop greater than threshold
	# 3. user demands the email from publishing message to aws


	# ----------------------Set up GPIO pins----------------------
	knockPin = 24           # indicate the knock sensor GPIO's pin
	DHT11Pin = 17           # indicate the DHT11 sensor GPIO's pin
	RGB.rPin = 27           # indicate the red light
	RGB.bPin = 22           # indicate the blue light
	RGB.gPin = 23           # indicate the green light

	# ----------------------Set up GPIO----------------------

	GPIO.setmode(GPIO.BCM)       # Numbers GPIOs by physical location
	GPIO.setwarnings(False)
	GPIO.setup(RGB.rPin, GPIO.OUT)
	GPIO.setup(RGB.gPin, GPIO.OUT)
	GPIO.setup(RGB.bPin, GPIO.OUT)
	GPIO.setup(knockPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.input(knockPin)

	# ----------------------Set up variables----------------------
	notify = True           # enable or disable send email function
	lastTemp = 0            # use to check the threshold
	lastHumi = 0            # use to check the threshold
	updateInterval = 1      # indicate update condition time (in seconds)
	deltaT = 10              # if changes of values greater than this, send email(for temperature)
	deltaH = 20             # if changes of values greater than this, send email(for humidity)

	count = 0
	delayWeight = 12        # means send email after time 12 * updateInterval

	currLight = RGB.gPin    # indicate green pin
	RGB.killLight()
	RGB.lightOn(currLight)

	    # start to detect the knock sensor
	GPIO.add_event_detect(knockPin, GPIO.FALLING, callback=changeNotify, bouncetime=1000) # wait for falling

	while True:

	    # update temperature and humidity (assume no error will occur)
	    lastTemp, lastHumi = DHT11.getInfo(DHT11Pin)
	#    if notify and count == delayWeight:
	#        # message to be included in the email
	#        msg = "Here is the picture from Home"
	#        sendNotification(msg)
	#        count = 0
	#    else:
	#        count += 1

	    # update condition after certain time
	    time.sleep(updateInterval)

	    # check condition
	    currTemp, currHumi = DHT11.getInfo(DHT11Pin)
	    if notify and (abs(currHumi-lastHumi) > deltaH or abs(currTemp-lastTemp) > deltaT):
	        # message to be included in the email
	        msg = "Sudden change in temperature or humidity detected!!"
	 	print(msg)
		sendNotification(msg)
	    print('Notify:'+str(notify))

	# reset the GPIO pins and RGB kill light
	RGB.killLight()
	GPIO.cleanup()
except KeyboardInterrupt:
	RGB.killLight()
	GPIO.cleanup()

##
