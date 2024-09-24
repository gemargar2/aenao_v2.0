# parse csv containing
import math
import statistics
import csv

def std_xyz_fun():
	std_xyz = [0]*3
	std_baseline = [0]*3
	std_baseline[0] = 0.01
	std_baseline[1] = 0.01
	std_baseline[2] = 0.01
	sample_x = []
	sample_y = []
	sample_z = []
	
	filename = "/home/raspberry/Desktop/aenao_data/vibration/vib_sample_1.csv"

	with open(filename) as csv_file:
		reader = csv.reader(csv_file)
		for row in reader:
			sample_x.append(float(row[0]))
			sample_y.append(float(row[1]))
			sample_z.append(float(row[2]))

	std_xyz[0] = statistics.stdev(sample_x)
	std_xyz[1] = statistics.stdev(sample_y)
	std_xyz[2] = statistics.stdev(sample_z)

	'''
	print("x std: %.6f" % std_xyz[0])
	print("y std: %.6f" % std_xyz[1])
	print("z std: %.6f" % std_xyz[2])
	'''
	
	for i in range(3):
		std_xyz[i] = (std_xyz[i]-std_baseline[i])/std_baseline[i]*100
	
	'''
	print("x std: %.2f%%" % std_xyz[0])
	print("y std: %.2f%%" % std_xyz[1])
	print("z std: %.2f%%" % std_xyz[2])
	'''

	return std_xyz
