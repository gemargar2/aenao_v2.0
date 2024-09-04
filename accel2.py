import csv
import serial
from datetime import datetime

seconds = 1 # 10 seconds
csvFilePath = "data/vib_sample.csv" # Overwrite one file

#Open a csv file and set it up to receive comma delimited input
file = open(csvFilePath, newline='', mode='w') # open in write mode (delete previous recordings)
writer = csv.writer(file, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)
writer.writerow(['x', 'y', 'z'])
file = open(csvFilePath, newline='', mode='a') # reopen in append mode (write in same file)
writer = csv.writer(file, delimiter=",", escapechar=' ', quoting=csv.QUOTE_NONE)

#Open a serial port that is connected to an Arduino
ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200)
ser.flushInput()

# Read 10 lines to avoid uart trash in the first lines
for i in range(10):
    # Read in data from Serial until \n (new line) received
    ser_bytes = ser.readline()

# Sampling rate is 1344kHz
for i in range(1344*seconds):
    #Read in data from Serial until \n (new line) received
    ser_bytes = ser.readline()
    
    #Convert received bytes to text format
    decoded_bytes = (ser_bytes[0:len(ser_bytes)-2].decode())
    #print(decoded_bytes)

    #Write received data to CSV file
    writer.writerow([decoded_bytes])

# Close port and CSV file to exit
ser.close()
file.close()
