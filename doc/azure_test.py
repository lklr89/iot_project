# IoT Project Group08 ABC

from iothub_client import IoTHubClient, IoTHubTransportProvider, IoTHubMessage
import time
import serial
import sys
import datetime

CONNECTION_STRING = "HostName=iotprojecthub.azure-devices.net;DeviceId=Group08;SharedAccessKey=cVe0Z/aRyhebmdXIlKzuSaBR9YlNui+hprfaIYsI35A="
PROTOCOL = IoTHubTransportProvider.MQTT
ser = serial.Serial('/dev/ttyUSB0',9600)
logfile = open('tempdata.log', 'a+')


def send_confirmation_callback(message, result, user_context):
    print("Confirmation received for message with result = %s" % (result))


if __name__ == '__main__':
    client = IoTHubClient(CONNECTION_STRING, PROTOCOL)
    print("Message transmitted to IoT Hub")

    while True:
        # Capture timestamp
        timeCap = str (datetime.datetime.now())  
        # Read data from serial port
        read_serial = timeCap + ": " + ser.readline()
        # Convert into IoTHubMessage and send to Hub 
        message = IoTHubMessage(read_serial)
        client.send_event_async(message, send_confirmation_callback, None)
        # Log message
        logfile.write(read_serial)
        time.sleep(1)




