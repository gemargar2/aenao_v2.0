#!/usr/bin/env python

import time
import subprocess
import multiprocessing
import sys
from datetime import datetime

from mic import *
from amps import *
from accel2 import *
from send_files import *

from Vibes_validation import *
from Sound_validation import *
from bin_status import *
from door_switch import *

motor_sleep = 15 # 15 minutes
record_time = 10 # 10 seconds

csvFilePath = "aenao_data/log_files/status.csv" # Overwrite one file

def log_sleep(arg):
	# ------------------- Logging part ----------------------	
	try:
		record_current(1) # record 1 second of current
		weight = readValue()
		power = rms_calc("aenao_data/power/amp_sample.wav")
		with open(csvFilePath, newline='\n', mode='a') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			# writer.writerow(['power', 'weight', 'timestamp'])
			timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
			writer.writerow([int(power), weight, timestamp])
	except:
		print("Can't reach sensors")
		

def binProcess():
	while True:
		# ------------------- Predictive maintenance part ----------------------
		# creating processes
		p1 = multiprocessing.Process(target=record_sound, args=[record_time])
		p2 = multiprocessing.Process(target=record_vibration, args=[record_time])
		p3 = multiprocessing.Process(target=record_current, args=[record_time])
		# starting processes
		p1.start()
		p2.start()
		p3.start()
		# wait until both processes finish
		p1.join()
		p2.join()
		p3.join()
		# Send data to db
		global_request()
		count = getCounter()
		weight = readValue() 
		# Send an overall report
		validation_mode(weight, count)
		time.sleep(15*60)

def main():
	# creating processes
	p4 = multiprocessing.Process(target=binProcess)
	p5 = multiprocessing.Process(target=userProcess)
	# starting processes
	p4.start()
	p5.start()
	# wait until both processes finish
	p4.join()
	p5.join()

if __name__ == "__main__":
	while True:
		userProcess()


