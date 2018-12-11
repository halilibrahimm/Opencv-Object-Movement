#!/usr/bin/env python
########################################################################                                                                  
# Bu örnek, en basit GPS Komut Dosyasıdır.It simply reads the
# raw output of the GPS sensor on the GoPiGo or GrovePi and prints it.  
#
# http://www.dexterindustries.com/GoPiGo/ 
# http://www.dexterindustries.com/GrovePi/                                                                
# History
# ------------------------------------------------
# Author     Date      		Comments
# John      2/25/2015		Initial Authoring
# 			                                                         
# These files have been made available online through a Creative Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)           
#
########################################################################


from gopigo import *
import serial, time
import smbus#(System Management Bus)  I2C Protokolünün bir alt kümesidir         
import math
import RPi.GPIO as GPIO# raspberry pi GPIO'YU kontrol etmek için bir sınıf sağlar
import struct
import sys
import ir_receiver_check

if ir_receiver_check.check_ir():
	print "Disable IR receiver before continuing"
	exit()

ser = serial.Serial('/dev/ttyAMA0',  9600, timeout = 0)	#Seri portun hızını 9600 baud ayarla #Open the serial port at 9600 baud
ser.flush()#seri buffer temizleme

def readlineCR():
    rv = ""
    while True:
        time.sleep(0.01)	#0.1 saniye programı askıya al # This is the critical part.  A small pause 
        					# burada çalışmaya devam eder # works really well here.
        ch = ser.read() #seri portu oku       
        rv += ch# okunan degeri rv ye ekle
        if ch=='\r' or ch=='':#eger okunan degerin sonuna gelindiyse rv yi dönder
            return rv

while True:
	#readlineCR()
	x=readlineCR()
	print x
	
#################################################################################################
#                                                                                               #
#	Çıktı aşağıdaki gibi görünmelidir. The output should look like something below.             #
#                                                                                               #
#                                                                                               #
#################################################################################################
'''







$GPGGA,001929.799,,,,,0,0,,,M,,M,,*4C

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPGSV,1,1,00*79

$GPRMC,001929.799,V,,,,,0.00,0.00,060180,,,N*46

$GPGGA,001930.799,,,,,0,0,,,M,,M,,*44

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPGSV,1,1,00*79

$GPRMC,001930.799,V,,,,,0.00,0.00,060180,,,N*4E

$GPGGA,001931.799,,,,,0,0,,,M,,M,,*45

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPGSV,1,1,00*79

$GPRMC,001931.799,V,,,,,0.00,0.00,060180,,,N*4F

$GPGGA,001932.799,,,,,0,0,,,M,,M,,*46

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPGSV,1,1,00*79

$GPRMC,001932.799,V,,,,,0.00,0.00,060180,,,N*4C

$GPGGA,001933.799,,,,,0,0,,,M,,M,,*47

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPGSV,1,1,00*79

$GPRMC,001933.799,V,,,,,0.00,0.00,060180,,,N*4D

$GPGGA,001934.799,,,,,0,0,,,M,,M,,*40

$GPGSA,A,1,,,,,,,,,,,,,,,*1E

$GPGSV,1,1,00*79

$GPRMC,001934.799,V,,,,,0.00,0.00,060180,,,N*4A

$GPGGA,001935.799,,,,,0,0,,,M,,M,,*41
'''