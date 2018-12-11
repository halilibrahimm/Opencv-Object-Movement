#!/usr/bin/env python
# This example is to control the LED's connected to the analog and digital ports of the GoPiGo

from gopigo import *
import time

#Pin numarasını anolog port A0 olarak alınmak üzere degisene atandı #Pin number for the grove analog port A0
analog_pin=15

#Pin numarası digital port D11 ayarlanmak üzere degiskene atandı #Pin number for the grove digital port D11
digital_pin=10

#Portlar çıkış olarak ayarlandı #Setting the port to output
pinMode(analog_pin,"OUTPUT")
pinMode(digital_pin,"OUTPUT")
while True:
	print "ON"
	digitalWrite(analog_pin,1)#anolog pin High yapıldı
	digitalWrite(digital_pin,1)#digital pin High yapıldı
	time.sleep(.5)#0.5 saniye bekleme
	
	print "OFF"
	digitalWrite(analog_pin,0)#anolog pin Low yapıldı
	digitalWrite(digital_pin,0)#digital pin Low yapıldı
	time.sleep(.5)#0.5 saniye bekleme
