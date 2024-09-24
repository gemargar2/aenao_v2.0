#!/usr/bin/env python

import time
import subprocess
import multiprocessing
import sys
from datetime import datetime
from send_files import *

motor_sleep = 15*60 # 15 minutes
general_sleep = 1

def sleep_mode(arg):
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

def sound_mode():
	print("Recording sound")
	subprocess.run(["python", "mic.py", str(counter)])
	audio_request()
	sleep_mode(motor_sleep)

def vibration_mode():
	print("Recording vibrations")
	subprocess.run(["python", "accel2.py", str(counter)])
	vib_request()
	sleep_mode(motor_sleep)

def amps_mode():
	print("Recording current")
	subprocess.run(["python", "amps.py", str(counter)])
	#amp_request()
	sleep_mode(motor_sleep)

def main():
	global counter
	while True:
		# creating processes
		p1 = multiprocessing.Process(target=sound_mode)
		p2 = multiprocessing.Process(target=vibration_mode)
		#p3 = multiprocessing.Process(target=amps_mode)
		#p4 = multiprocessing.Process(target=user_mode)
		#p5 = multiprocessing.Process(target=validation_mode)
		# starting processes
		p1.start()
		p2.start()
		#p3.start()
		#p4.start()
		#p5.start()
		# wait until process 1 is finished
		p1.join()
		p2.join()
		#p3.join()
		#p4.join()
		#p5.join()
		# increment counter used for file naming

if __name__ == "__main__":
	try:
		main()
	finally:
		print("--------------")
		print("GPIO.cleanup()")
		print("--------------")
		GPIO.cleanup()

	sys.exit()


