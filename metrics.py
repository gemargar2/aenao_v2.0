import wave
import contextlib
import audioop

import math
import statistics as stats
from pandas import *
import csv

def rms_calc(fname):
    ratio = 20 # Voltage to Current ratio (characteristic of the amp clamp)
    voltage = 220 # Voltage RMS value
    with contextlib.closing(wave.open(fname,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        width = f.getsampwidth()
        channel = f.getnchannels()
        size = width*channel
        # f.rewind()
        wav = f.readframes(f.getnframes())
        # print(duration)

    rms_value = voltage * ratio * audioop.rms(wav, 2) / 32768
    
    return rms_value

def std_calc(csvFilePath):
    std_xyz = [0]*3
    std_baseline = 0.01
    
    # reading CSV file
    data = read_csv(csvFilePath)
    # converting column data to list
    x = data['x'].tolist()
    y = data['y'].tolist()
    z = data['z'].tolist()
    
    std_xyz[0] = stats.stdev(x)
    std_xyz[1] = stats.stdev(y)
    std_xyz[2] = stats.stdev(z)
    '''
    print("x std: %.6f" % std_xyz[0])
    print("y std: %.6f" % std_xyz[1])
    print("z std: %.6f" % std_xyz[2])
    '''
    std_xyz = [(std_xyz[i]/std_baseline*100) for i in range(3)]
    '''
    print("x std: %.2f%%" % std_xyz[0])
    print("y std: %.2f%%" % std_xyz[1])
    print("z std: %.2f%%" % std_xyz[2])
    '''
    return std_xyz