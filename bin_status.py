#!/usr/bin/env python

import time
import subprocess
import sys

from Sound_validation import *
from Vibes_validation import *
from datetime import datetime
from metrics import *

import requests
import json

url_motor = "https://ae3nao.iti.gr/api/bins"
# url_user = "https://ae3nao.iti.gr/api/userBin"

headers = {
  'Content-Type': 'application/json'
}

motor_sleep = 30

a = [0]*3
power = 0
audio_decision = "NOT OK"
vibes_decision = "NOT OK"

def validation_mode(weight, count):
	print("Motor Operation Validation")
	# Here goes Stelios' validation script
	print("Validating sound")
	#audio_decision = run_sound_validation()
	time.sleep(1)

	# Here goes Stelios' validation script
	print("Validating vibrations")
	#vibes_decision = run_vibes_validation()
	a = std_calc("aenao_data/vibration/vib_sample.csv")
	time.sleep(1)

	# Here goes Stelios' validation script
	print("Validating current")
	power = rms_calc("aenao_data/power/amp_sample.wav")
	time.sleep(1)

	# Motor data
	timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

	payload = json.dumps({
		'binID': 1,
		'timestamp': timestamp,
		'metrics': [
			{
				'type': 'Audio',
				'status': audio_decision
			},
			{
				'type': 'Vibrations',
				'status': vibes_decision,
				'x': int(a[0]),
				'y': int(a[1]),
				'z': int(a[2]),
				'metric': '%'
			},
			{
				'type': 'Power',
				'value': int(power),
				'metric': 'W'
			}
		],
		"total_weight": weight,
		"total_count": count
	})
	print(payload)
	
	try:
		print("Success")
		# Post to endpoint
		response = requests.request("POST", url_motor, headers=headers, data=payload)
		print(response.json())
	except:
		print("Failed to connect with the endpoint")

'''
while(1):
	validation_mode()
	time.sleep(60)
'''
