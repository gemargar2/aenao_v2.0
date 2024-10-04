import csv
import serial
import time
from datetime import datetime

import os
os.chdir("/home/raspberry/Desktop")

csvFilePath = "aenao_data/vibration/vib_sample.csv" # Overwrite one file
csvFilePath2 = "aenao_data/vibration/vib_sample2.csv" # Overwrite one file
data = []

def record_vibration(seconds):
	#Open a serial port that is connected to an Arduino
	ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
	ser.flushInput()

	print('start recording vibrations')
	start = time.time()
	# Read 10 lines to avoid uart trash in the first lines
	for i in range(5):
		# Read in data from Serial until \n (new line) received
		ser_bytes = ser.readline()

	# Sampling rate is 1344kHz
	for i in range(200*seconds):
		#Read in data from Serial until \n (new line) received
		ser_bytes = ser.readline()

		#Convert received bytes to text format
		decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode())
		#print(decoded_bytes)

		#Write received data to CSV file
		data.append([decoded_bytes])

	end = time.time()
	print('stop recording vibrations')
	print(f'time elapsed: {end-start}')
	
	with open(csvFilePath, newline='', mode='w') as file:
		writer = csv.writer(file, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
		writer.writerow(['x', 'y', 'z'])
		writer.writerows(data)

	with open(csvFilePath2, newline='', mode='w') as file2:
		writer2 = csv.writer(file2, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
		writer2.writerows(data)
	# Close port and CSV file to exit
	ser.close()
	file.close()
	file2.close()
