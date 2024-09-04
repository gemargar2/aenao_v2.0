# python -m pip install pyaudio
import pyaudio
import wave
import matplotlib.pyplot as plt
import numpy as np
import sys
from wav2csv import *

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
FRAMES_PER_BUFFER = 512
index = 1 # check device index first

pa = pyaudio.PyAudio()

'''
info = pa.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
for i in range(0, numdevices):
	if (pa.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
		name = pa.get_device_info_by_host_api_device_index(0, i).get('name')
		#print("Input Device id ", i, " - ", name)
		if (name == "USB Audio Device: - (hw:0,0)"):
			index = i	
'''

stream = pa.open(
	format=FORMAT,
	channels=CHANNELS,
	rate=RATE,
	input=True,
	input_device_index = index,
	frames_per_buffer=FRAMES_PER_BUFFER
)

print('start recording')

seconds = 10 # 10 seconds
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

filename = "data/amps_sample.wav" # Overwrite one file
# filename = "data/amps_sample_" + sys.argv[1] + ".wav" # Write different file

obj = wave.open(filename, 'wb')
obj.setnchannels(CHANNELS)
obj.setsampwidth(pa.get_sample_size(FORMAT))
obj.setframerate(RATE)
obj.writeframes(b''.join(frames))
obj.close()

convert()