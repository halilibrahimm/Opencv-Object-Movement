#!/usr/bin/env python
#
'''
Install dependencies on the command line:
	sudo apt-get install python-lxml
	sudo pip install pykml



'''
# GrovePi Example for using the Grove GPS Module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#                                                           
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# Karan		 10 June 15		Updated the code to reflect the decimal GPS coordinates (contributed by rschmidt on the DI forums: http://www.dexterindustries.com/forum/?topic=gps-example-questions/#post-5668)
import serial, time
import smbus#(System Management Bus)  I2C Protokolünün bir alt kümesidir         
import math
import RPi.GPIO as GPIO# raspberry pi GPIO'YU kontrol etmek için bir sınıf sağlar
import struct
import sys
import ir_receiver_check

if ir_receiver_check.check_ir():
	print "Disable IR receiver before continuing"#Devam etmeden önce IR alıcısını devre dışı bırak yazdırır
	exit()
ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Open the serial port at 9600 baud #Seri portun hızını 9600 baud ayarla
ser.flush()#seri buffer temizleme

class GPS:
	#Kullanılan GPS modülü bir Grove GPS modülüdür http://www.seeedstudio.com/depot/Grove-GPS-p-959.html  #The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
	# Refeans: SIM28 NMEA teknik özellikleri dosyası http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip  # Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]

	#GPS'den verileri oku #Read data from the GPS
	def read(self):	
		while True:
			GPS.inp=ser.readline()#Seri porttan input alır
			if GPS.inp[:6] =='$GPGGA': # GGA verisi, paket 1, ihtiyacımız olan tüm verilere sahip # GGA data , packet 1, has all the data we need
				break
			time.sleep(0.1)     #0.1 saniye programı askıya al
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ""
		GPS.GGA=GPS.inp.split(",")	#GPS.inp degerini  parçalar  #without the cmd program will crach
		return [GPS.GGA]#line 57 de elde edilen değeri geri döndürür
		
	#Verileri ayrı ögelere bölme 	#Split the data into individual elements
	def vals(self):#yukarıdaki fonksiyondaki degerleri degiskene atıp geri dönderen fonksiyon
		time=GPS.GGA[1]
		lat=GPS.GGA[2]
		lat_ns=GPS.GGA[3]
		long=GPS.GGA[4]
		long_ew=GPS.GGA[5]
		fix=GPS.GGA[6]
		sats=GPS.GGA[7]
		alt=GPS.GGA[9]
		return [time,fix,sats,alt,lat,lat_ns,long,long_ew]
	
	# Ondalık degere dönüştürme # Convert to decimal degrees
	def decimal_degrees(self, raw_degrees):
		degrees = float(raw_degrees) // 100
		d = float(raw_degrees) % 100 / 60
		return degrees + d

g=GPS()
f=open("gps_data.csv",'w')	#Verileri log dosyasına kaydetmek üzere aç #Open file to log the data
f.write("name,latitude,longitude\n")	#Başlığı dosyanın başına yazın  #Write the header to the top of the file
ind=0


def read_GPS():
	try:
		x=g.read()	#GPS oku #Read from GPS
		[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()	#GPS degerlerini al #Get the individual values
		
		# ondalık degere dönüştür # Convert to decimal degrees
		lat = g.decimal_degrees(float(lat))
		if lat_ns == "S":#lat_ns degeri S ise lat=-lat yap
			lat = -lat

		long = g.decimal_degrees(float(long))# long degerini ondalık deger yap
		if long_ew == "W":#long_ew degeri W ise long=-long yap
			long = -long
			
		print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
		s=str(t)+","+str(float(lat)/100)+","+str(float(long)/100)+"\n"	
		f.write(s)	#dosyayı kaydet #Save to file
		# time.sleep(2)

	except IndexError:
		print "Unable to read"#eger hata olusursa ekrana mesaj ver
	except KeyboardInterrupt:
		f.close()#dosyayı kapat
		print "Exiting"#ekrana mesaj verir
		sys.exit(0)#sonlanır

def read_destination_from_file():
	#
	#
	return 0
	
def calculate_azimuth_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):#azimuth(yön tarifinin yatay bileşeni) hesaplama fonksiyon
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = 5.0,6.7,1.5
	x2,y2,z2 = 4.0,1.2,1.6
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)#mesafe hesabı
	print distance#mesafeyi yazdır
	# 5.5910642993977451
	plunge = math.degrees(math.asin((z2-z1)/distance))#atılım hesabı
	print plunge#degeri yazdır
	# 1.0248287567800018 # eger z2>z1 ise atılım aşağı dogru pozitifthe resulting dip_plunge is positive downward if z2 > z1
	azimuth = math.degrees(math.atan2((x2-x1),(y2-y1)))
	print azimuth
	# -169.69515353123398 # = 360 + azimuth = 190.30484646876602 or  180+ azimuth = 10.304846468766016 over the range of 0 to 360

def calculate_distance_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):#mesafe hesaplama fonksiyonu
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = 5.0,6.7,1.5
	x2,y2,z2 = 4.0,1.2,1.6
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)#mesafe hesabı
	print distance
	
def turn_to_destination():
	return 0

#!/usr/bin/env python
#
'''
Install dependencies on the command line:
	sudo apt-get install python-lxml
	sudo pip install pykml



'''
# GrovePi Example for using the Grove GPS Module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html?cPath=25_130
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://www.dexterindustries.com/forum/?forum=grovepi
#
# LICENSE: 
# These files have been made available online through a [Creative Commons Attribution-ShareAlike 3.0](http://creativecommons.org/licenses/by-sa/3.0/) license.
#                                                           
# History
# ------------------------------------------------
# Author     Date      		Comments
# Karan      21 Aug 14 		Initial Authoring
# Karan		 10 June 15		Updated the code to reflect the decimal GPS coordinates (contributed by rschmidt on the DI forums: http://www.dexterindustries.com/forum/?topic=gps-example-questions/#post-5668)
import serial, time
import smbus#(System Management Bus)  I2C Protokolünün bir alt kümesidir   
import math
import RPi.GPIO as GPIO# raspberry pi GPIO'YU kontrol etmek için bir sınıf sağlar
import struct
import sys

ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Seri portun hızını 9600 baud ayarla
ser.flush()#seri buffer temizleme

class GPS:
	#Kullanılan GPS modülü bir Grove GPS modülüdür http://www.seeedstudio.com/depot/Grove-GPS-p-959.html  #The GPS module used is a Grove GPS module http://www.seeedstudio.com/depot/Grove-GPS-p-959.html
	inp=[]
	# Refeans: SIM28 NMEA teknik özellikleri dosyası http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip  # Refer to SIM28 NMEA spec file http://www.seeedstudio.com/wiki/images/a/a0/SIM28_DATA_File.zip
	GGA=[]

	#GPS'den verileri oku  #Read data from the GPS
	def read(self):	
		while True:
			GPS.inp=ser.readline()#Seri porttan input alır
			if GPS.inp[:6] =='$GPGGA': # GGA verisi, paket 1, ihtiyacımız olan tüm verilere sahip  # GGA data , packet 1, has all the data we need
				break
			time.sleep(0.1)     #0.1 saniye programı askıya al #without the cmd program will crach
		try:
			ind=GPS.inp.index('$GPGGA',5,len(GPS.inp))	#Sometimes multiple GPS data packets come into the stream. Take the data only after the last '$GPGGA' is seen
			GPS.inp=GPS.inp[ind:]
		except ValueError:
			print ""
		GPS.GGA=GPS.inp.split(",")	#GPS.inp degerini  parçalar #Split the stream into individual parts
		return [GPS.GGA]#line 191 de elde edilen değeri geri döndürür
		
	#Verileri ayrı ögelere bölme #Split the data into individual elements
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
	
	# Ondalık degere dönüştürme  # Convert to decimal degrees
	def decimal_degrees(self, raw_degrees):
		degrees = float(raw_degrees) // 100
		d = float(raw_degrees) % 100 / 60
		return degrees + d

g=GPS()
f=open("gps_data.csv",'w')	#Verileri log dosyasına kaydetmek üzere aç #Open file to log the data
f.write("name,latitude,longitude\n")	#Başlığı dosyanın başına yazın  #Write the header to the top of the file
ind=0


def read_GPS():
	try:
		x=g.read()	#GPS oku #Read from GPS
		[t,fix,sats,alt,lat,lat_ns,long,long_ew]=g.vals()	#.degerleri al #Get the individual values
		
		# ondalık degere dönştürme # Convert to decimal degrees
		lat = g.decimal_degrees(float(lat))
		if lat_ns == "S":#lat_ns degeri S ise lat=-lat yap
			lat = -lat

		long = g.decimal_degrees(float(long))# long degerini ondalık deger yap
		if long_ew == "W":#long_ew degeri W ise long=-long yap
			long = -long
			
		print "Time:",t,"Fix status:",fix,"Sats in view:",sats,"Altitude",alt,"Lat:",lat,lat_ns,"Long:",long,long_ew
		s=str(t)+","+str(float(lat)/100)+","+str(float(long)/100)+"\n"	
		f.write(s)	#dosyayı kaydet #Save to file
		# time.sleep(2)

	except IndexError:
		print "Unable to read"
	except KeyboardInterrupt:
		f.close()
		print "Exiting"
		sys.exit(0)

def read_destination_from_file():
	#
	#
	return 0
	
def calculate_azimuth_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):#azimuth(yön tarifinin yatay bileşeni) hesaplama fonksiyon
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = gps_coord_lat,gps_coord_lon,0
	x2,y2,z2 = gps_target_coord_lat,gps_target_coord_lon,0
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)#mesafe hesaplama
	#mesafeyi yazdır
	# 5.5910642993977451
	plunge = math.degrees(math.asin((z2-z1)/distance))
	#atılımı yazdır
	# 1.0248287567800018 # eger z2>z1 ise atılım aşağı dogru pozitifthe resulting dip_plunge is positive downward if z2 > z1
	azimuth = math.degrees(math.atan2((x2-x1),(y2-y1)))
	print azimuth
	# -169.69515353123398 # = 360 + azimuth = 190.30484646876602 or  180+ azimuth = 10.304846468766016 over the range of 0 to 360

def calculate_distance_to_destination(gps_coord_lat, gps_coord_lon, gps_target_coord_lat, gps_target_coord_lon):#mesafeyi hesaplama fonksiyonu
	# Calculations were found here:  http://gis.stackexchange.com/questions/108547/how-to-calculate-distance-azimuth-and-dip-from-two-xyz-coordinates
	x1,y1,z1 = gps_coord_lat,gps_coord_lon,0
	x2,y2,z2 = gps_target_coord_lat,gps_target_coord_lon,0
	distance = math.sqrt((x2-x1)**2+(y2-y1)**2+(z2 -z1)**2)#mesafeyi hesapla
	print distance#mesafeyi yazdır
	
def turn_to_destination():
	return 0

#Hedef CSV yi aç.#Open the CSV of Destinations.
destinations = [10, 9, 8, 7, 6, 5]

for each in destinations:
	print each
	x1,y1,z1 = 5.0,6.7,1.5
	x2,y2,z2 = 4.0,1.2,1.6
	calculate_azimuth_to_destination(x1,y1,x2,y2)
	calculate_distance_to_destination(x1,y1,x2,y2)
	# Hedefler için Dosya Oku
	# Her Hedef için:
	# 1. Hedefe olan Azimuth hesaplayın.
	# 2. Hedefe olan mesafeyi hesaplayın.
	# 3. Hedefe olan mesafe <3m iken
	
	# a. Hedefe olan Azimuth hesaplayın.
	# b. Hedefe olan mesafeyi hesapla.
	# c. Hedefe dön.
	# d. Hedefe kadar koş.
	# e. 5 saniye bekle
	
	# Read File for destinations
	# For each Destination: 
	# 1. Calculate Azimuth to destination.
	# 2. Calculate distance to destination.  
	# 3. While distance to destination < 3m
	
	#	a. Calculate Azimuth to destination.
	#	b. Calculate distance to destination.  
	#	c. Turn to destination.
	#	d. Run to destination.
	#	e. Wait 5 seconds.  