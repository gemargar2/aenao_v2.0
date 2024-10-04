import requests
import json
from pandas import *
from datetime import datetime

import os
os.chdir("/home/raspberry/Desktop")

def vib_request():
	url = "https://ae3nao.iti.gr/api/maintenance"
	
	# Decide the two file paths according to your computer system
	csvFilePath = r'aenao_data/vibration/vib_sample.csv'

	# Decide the two file paths according to your computer system
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	new_filename = "aenao_data/vibration/vib_" + timestamp + ".csv" # Write different file
	old_filename = 'aenao_data/vibration/vib_sample.csv'
	command = "cp '" + old_filename + "' '" + new_filename + "'"
	os.system(command)

	# reading CSV file
	data = read_csv(csvFilePath)

	# converting column data to list
	x = data['x'].tolist()
	y = data['y'].tolist()
	z = data['z'].tolist()

	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

	payload = json.dumps({
	  "binID": "1",
	  "timestamp": timestamp,
	  "x": x,
	  "y": y,
	  "z": z
	})

	headers = {
	  'Content-Type': 'application/json'
	}

	try:
		response = requests.request("POST", url, headers=headers, data=payload)
		print(response.text)
		print("Success")
	except:
		print("Failed to connect with the endpoint")

def audio_request():
	url = "https://ae3nao.iti.gr/api/audio-file"
	
	# Decide the two file paths according to your computer system
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	new_filename = "aenao_data/sound/audio_" + timestamp + ".wav" # Write different file
	old_filename = 'aenao_data/sound/audio_sample.wav'
	command = "cp '" + old_filename + "' '" + new_filename + "'"
	os.system(command)
	
	payload = {}
	files=[('audio', (new_filename, open(new_filename, 'rb'), 'audio/wav'))]
	try:
		response = requests.request("POST", url, data=payload, files=files)
		print(response.text)
		# command = "rm '" + new_filename + "'"
		# os.system(command)
		print("Success")
	except:
		print("Failed to connect with the endpoint")

def amp_request():
	url = "https://ae3nao.iti.gr/api/current-file"
	
	# Decide the two file paths according to your computer system
	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	new_filename = "aenao_data/power/amp_" + timestamp + ".wav" # Write different file
	old_filename = 'aenao_data/power/amp_sample.wav'
	command = "cp '" + old_filename + "' '" + new_filename + "'"
	os.system(command)
	
	payload = {}
	files=[('current', (new_filename, open(new_filename, 'rb'), 'audio/wav'))]
	try:
		response = requests.request("POST", url, data=payload, files=files)
		print(response.text)
		#command = "rm '" + new_filename + "'"
		#os.system(command)
		print("Success")
	except:
		print("Failed to connect with the endpoint")

def weight_request(weight, total, counter):
	url_user = "https://ae3nao.iti.gr/api/userBin"

	timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	# Post to endpoint
	payload = json.dumps({
		"binID": "1",
		"userID": "564994897833",
		'timestamp': str(timestamp),
		"weight": str(weight),
		"metric_weight": "kg",
		"total_weight": str(total),
		"total_count": str(counter),
		"fill_level": "N/A",
		"fill_metric":"%"
	})
	
	headers = {
		'Content-Type': 'application/json'
	}
	try:
		#print(payload)
		#Post to endpoint
		response = requests.request("POST", url_user, headers=headers, data=payload)
		print(response.json())
		print("Success")
	except:
		print("Failed to connect with the endpoint")
		#print(weight, total, counter)

def global_request():
	vib_request()
	audio_request()
	amp_request()
