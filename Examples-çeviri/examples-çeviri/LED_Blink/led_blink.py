#!/usr/bin/env python
# This example is to control the LED's on a GoPiGo

from gopigo import *
import sys
import time

while True:
	print "ON"
	led_on(LED_L)#soldaki ledi yak
	led_on(LED_R)#sağdaki ledi yak
	time.sleep(.5)#0.5 saniye bekleme
	
	print "OFF"
	led_off(LED_L)#soldaki ledi sondur
	led_off(LED_R)#sağdaki ledi sondur
	time.sleep(.5)#0.5 saniye bekleme
