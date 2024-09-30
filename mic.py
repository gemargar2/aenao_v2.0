# python -m pip install pyaudio
import os
import time
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import sys
from datetime import datetime

'''
import os
os.chdir("/home/raspberry/Desktop")
'''

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FRAMES_PER_BUFFER = 512
index = 0 # check device index first

pa = pyaudio.PyAudio()

def record_sound(seconds):
	stream = pa.open(
		format=FORMAT,
		channels=CHANNELS,
		rate=RATE,
		input=True,
		input_device_index = index,
		frames_per_buffer=FRAMES_PER_BUFFER
	)
	print('start recording sound')

	# seconds = 1 # 10 seconds
	frames = []
	second_tracking = 0
	second_count = 0

	for i in range(0, int(RATE/FRAMES_PER_BUFFER*seconds)):
		data = stream.read(FRAMES_PER_BUFFER)
		frames.append(data)
		second_tracking += 1
		if second_tracking == RATE/FRAMES_PER_BUFFER:
			second_count += 1
			second_tracking = 0
			print(f'Time Left: {seconds - second_count} seconds')
	
	stream.stop_stream()
	stream.close()
	pa.terminate()
	print('stop recording sound')

	filename = "aenao_data/sound/audio_sample.wav" # Overwrite one file
	# filename = "data/audio_sample_" + sys.argv[1] + ".wav" # Write different file

	obj = wave.open(filename, 'wb')
	obj.setnchannels(CHANNELS)
	obj.setsampwidth(pa.get_sample_size(FORMAT))
	obj.setframerate(RATE)
	obj.writeframes(b''.join(frames))
	obj.close()
