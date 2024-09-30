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
general_sleep = 1

def sleep_mode(arg):
	print("Sleep")
	countdown = motor_sleep
	for i in range(1,arg):
		time.sleep(1)
		countdown -= 1
		print(str(countdown) + " seconds left")

def binProcess():
	while True:
		'''
		# creating processes
		p1 = multiprocessing.Process(target=record_sound, args=[1])
		p2 = multiprocessing.Process(target=record_vibration, args=[1])
		p3 = multiprocessing.Process(target=record_current, args=[1])
		# starting processes
		p1.start()
		p2.start()
		p3.start()
		# wait until both processes finish
		p1.join()
		p2.join()
		p3.join()
		'''
		global_request()
		# Read value from weight sensor
		weight = readValue()
		counter = getCounter()
		# Send an overall report
		# validation_mode(weight, counter)
		time.sleep(motor_sleep)

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
	main()


