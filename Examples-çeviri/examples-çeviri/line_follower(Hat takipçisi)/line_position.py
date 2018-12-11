
# Dexter Industries line sensor basic example
#
# This example shows a basic example of how to read sensor data from the line sensor.

from __future__ import print_function
from __future__ import division
from builtins import input

import line_sensor
import time

line_pos=[0]*5
white_line=line_sensor.get_white_line()
black_line=line_sensor.get_black_line()
range_sensor= line_sensor.get_range()
threshold=[a+b/2 for a,b in zip(white_line,range_sensor)]

while True:
	raw_vals=line_sensor.get_sensorval()
	for i in range(5):
		if raw_vals[i]>threshold[i]:
			line_pos[i]=1
		else:
			line_pos[i]=0
	print(line_pos)
	

