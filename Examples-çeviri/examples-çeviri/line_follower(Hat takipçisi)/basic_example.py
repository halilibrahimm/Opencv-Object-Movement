# hat sensörü ile basit örnek
from __future__ import print_function
from __future__ import division
from builtins import input


import line_sensor
import time

def get_sensorval(): #sensör değerini getir
	while True:
		val=line_sensor.read_sensor() #sensorden okudugumuz değeri  atıyoruz
		if val[0]!=-1:
			return val
		else:
			#Tamponu temizlemek ve gereksiz değerleri kaldırmak için bir kez daha okuyun
			val=line_sensor.read_sensor()
while True:
	l0,l1,l2,l3,l4=get_sensorval()
	print (l0,l1,l2,l3,l4)
	#time.sleep(.05)
