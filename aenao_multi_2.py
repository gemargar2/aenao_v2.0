#!/usr/bin/env python

import time
import subprocess
import multiprocessing
import sys
from datetime import datetime
# from door_switch import *
from mic import *
from amps import *
from accel2 import *
from send_files import *

motor_sleep = 15 # 15 minutes
general_sleep = 1

def sleep_mode(arg):
	print("Sleep")
	countdown = motor_sleep
	for i in range(1,arg):
		time.sleep(1)
		countdown -= 1
		print(str(countdown) + " seconds left")

def user_mode():
	subprocess.run(["python", "door_switch.py", str(counter)])
	#weight_request()

def bin_mode():
	subprocess.run(["python", "bin_status.py", str(counter)])
	#weight_request()

def main():
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

if __name__ == "__main__":
	main()


