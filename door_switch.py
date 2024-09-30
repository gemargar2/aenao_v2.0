import RPi.GPIO as GPIO
import time
import sys
import signal
import serial
from send_files import *

GPIO.setmode(GPIO.BOARD)

DOOR_SENSOR_PIN_1 = 12
DOOR_SENSOR_PIN_2 = 18

samples = 50


GPIO.setup(DOOR_SENSOR_PIN_1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(DOOR_SENSOR_PIN_2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

counter = 0

def readValue():
	# measurement value
	value = 0
	#Open a serial port that is connected to an Arduino
	ser = serial.Serial(port='/dev/ttyACM1', baudrate=115200)
	ser.flushInput()

	for i in range(samples):
		# Read in data from Serial until \n (new line) received
		ser_bytes = ser.readline()
		# print(ser_bytes)

	for i in range(samples):
		# Read in data from Serial until \n (new line) received
		ser_bytes = ser.readline()
		# Convert received bytes to text format
		decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode())
		# print(decoded_bytes)
		value += float(decoded_bytes)

	# Close serial port
	ser.close()
	# Average measurements
	value = value//samples

	# Write received data to variable
	return value

def getCounter():
	return counter

def userProcess():
	isOpen = False
	oldIsOpen = False
	valueOpen = 0
	valueClosed = 0
	diff = 0
	
	while True:
		oldIsOpen = isOpen
		isOpen = GPIO.input(DOOR_SENSOR_PIN_1) | GPIO.input(DOOR_SENSOR_PIN_2)

		if (isOpen and (isOpen != oldIsOpen)):
			print("Door Open")
			valueOpen = readValue()
			print(valueOpen)
		elif (isOpen != oldIsOpen):
			print("Door Closed")
			valueClosed = readValue()
			print(valueClosed)
			diff = valueClosed-valueOpen
			counter = counter + 1
			print("Difference = " + str(diff))
			weight_request(diff, valueClosed, counter)

		time.sleep(1)

#userProcess()