#  Read data from serial port

import serial

ser = serial.Serial('/dev/ttyUSB0',9600)

while True:

    read_serial=ser.readline()
    print read_serial
