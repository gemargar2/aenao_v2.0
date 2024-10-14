import RPi.GPIO as GPIO
import time
import sys
import signal
import serial
from send_files import *
import multiprocessing

import csv
from datetime import datetime

GPIO.setmode(GPIO.BOARD)

DOOR_SENSOR_PIN_1 = 12
DOOR_SENSOR_PIN_2 = 18

samples = 50

GPIO.setup(DOOR_SENSOR_PIN_1, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(DOOR_SENSOR_PIN_2, GPIO.IN, pull_up_down = GPIO.PUD_UP)

counter = 0

csvFilePath = "aenao_data/log_files/throws.csv" # Overwrite one file

def getCounter():
	data = []
	row_index = 0
	with open(csvFilePath, "r", encoding="utf-8", errors="ignore") as scraped:
		reader = csv.reader(scraped, delimiter=',')
		for row in reader:
			if row:  # avoid blank lines
				row_index += 1
				columns = [row[0], row[1], row[2]]
				data.append(columns)
	print(f'Number of throws = {data[-1][0]}')
	return data[-1][0]

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

def userProcess():
	isOpen = False
	oldIsOpen = False
	valueOpen = 0
	valueClosed = readValue()
	diff = 0
	counter = 0
	with open(csvFilePath, newline='\n', mode='a') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		# writer.writerow(['counter', 'weight', 'timestamp'])
		timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
		writer.writerow([0, valueClosed, timestamp])
	
	while True:
		oldIsOpen = isOpen
		isOpen = GPIO.input(DOOR_SENSOR_PIN_1) | GPIO.input(DOOR_SENSOR_PIN_2)

		if (isOpen and (isOpen != oldIsOpen)):
			print("Door Open")
			valueOpen = readValue()
			print(valueOpen)
		elif (isOpen != oldIsOpen):
			print("Door Closed")
			time.sleep(10) # sleep for 10 seconds to avoid lid bounce
			valueClosed = readValue()
			print(valueClosed)
			diff = valueClosed-valueOpen
			counter = counter + 1
			print("Difference = " + str(diff))
			# Send values to db
			weight_request(diff, valueClosed, counter)
			# Write to csv
			with open(csvFilePath, newline='', mode='a') as csvfile:
				timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
				writer = csv.writer(csvfile, delimiter=',')
				writer.writerow([counter, valueClosed, timestamp])

		time.sleep(1)
