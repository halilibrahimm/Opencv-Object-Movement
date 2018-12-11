#!/usr/bin/env python
########################################################################                                                                  
# This example is for using the GoPiGo to move around and get the Latitude and Longitude coordinates and save them to a file
#
# http://www.dexterindustries.com/GoPiGo/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################

# Bu örnek, GoPiGo'yu hareket ettirmek ve Enlem ve Boylam koordinatlarını almak ve onları bir dosyaya kaydetmek için kullanmak içindir
#
from gopigo import *
import serial, time
import smbus #I2C protokolünü gerçekleştirmek için
import math
import RPi.GPIO as GPIO#gopigoyu içe aktarmak için
import struct
import sys
import ir_receiver_check #alıcı kontrolü

if ir_receiver_check.check_ir():
	print "Devam etmeden önce IR alıcısını devre dışı bırak"
	exit()

ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	# 9600 baud'da seri bağlantı portunu aç
ser.flush()#gönderme belleğini boşaltıyor

class GPS:
	# Kullanılan GPS modülü bir Grove GPS modülüdür http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
# Bkz. SIM28 NMEA teknik özellikleri dosyası http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]

	# GPS'den veri okuma
	def read(self):	
		while True:
			GPS.inp=ser.readline()#gpsi seri porttan okuyor
			if GPS.inp[:6] =='$GPGGA': # GGA verisi, 1 paket, ihtiyacımız olan tüm verilere sahip
				break
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))#Bazen birden çok GPS veri paketi akıma gelir. Verileri yalnızca son '$ GPGGA' görüldükten sonra alın
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ""
		GPS.GGA=GPS.inp.split(",")	#Akışı ayrı parçalara bölme
		return [GPS.GGA]
		
	#Bireysel öğelere verileri yerleştirin
	def vals(self):
		time=GPS.GGA[1]
		lat=GPS.GGA[2]
		lat_ns=GPS.GGA[3]
		long=GPS.GGA[4]
		long_ew=GPS.GGA[5]
		fix=GPS.GGA[6]
		sats=GPS.GGA[7]
		alt=GPS.GGA[9]
		return [time,fix,sats,alt,lat,lat_ns,long,long_ew]

g=GPS()
f=open("gps_data.csv",'w')	#Verileri kaydetmek için dosyayı açın
f.write("name,latitude,longitude\n")	#Başlığı dosyanın başına yazın
ind=0
while True:
	try:
		x=g.read()	#GPS'den oku
		[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()	#bireysel değerleri elde et
		print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
		s=str(t)+","+str(float(lat)/100)+","+str(float(long)/100)+"\n"	
		f.write(s)	#Dosyayı kaydet
		time.sleep(2)
	except IndexError:
		print "Unable to read"
	except KeyboardInterrupt:
		f.close()
		print "Exiting"
		sys.exit(0)
	
